import pandas as pd                        
from pytrends.request import TrendReq 
from transformers import pipeline
from datetime import datetime, timedelta
from craiyon import Craiyon
from craiyon.templates import GeneratedImages
import requests
import time
from requests.exceptions import HTTPError
from pathlib import Path
import os
from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient



class CronScript:


    def __init__(self):
        """
        One-time instantation of BlobServiceClient, env information check
        """

        #Get container information
        load_dotenv() 
        self.access_key = os.environ.get("AZURE_STORAGE_CONNECTION_STRING") 
        print(f"Connection String: {self.access_key}")
        self.container_name = os.environ.get("CONTAINER_NAME")
        print(f"Container name: {self.container_name}")


        #Checks for problem with .env file
        if not self.access_key or not self.container_name:
            raise ValueError("Azure Storage connection string or container name not found in environment variables.")

        try:
            #make instance of BlobServiceClient (needed to read and write from containers)
            self.blob_service_client = BlobServiceClient.from_connection_string(self.access_key)
        except Exception as e:
            print("Got this far")

        #Container client reads from the particular container we have made.
        self.container_client = self.blob_service_client.get_container_client(self.container_name)


    def delete_blobs(self):
        """
        Deletes every pre-existing blob in container for biweekly updates (to prevent excessive storage or duplicates)
        """
        try: 
            blob_list = self.container_client.list_blobs() #Can incorporate additional metadata, or filter by particular names
            for blob in blob_list:
                self.container_client.delete_blob(blob, delete_snapshots="include") #Delete snapshots as well in order to fully delete blob
        except Exception as e:
            print("Problem with deleting blobs")


    def query_trends(self, num_trends):
        """
        Returns a list of top [num_trends] trends from Google Trends.
        Using pytrends library for extracting trending searches.
        """
        pytrends = TrendReq()
        df = pytrends.trending_searches(pn='united_states')
        trends_list = df.head(num_trends)[0].tolist() #Sole column labelled "0" - converted to list instead
        return trends_list

  
    def filter_trends(self, trend_list, bart_threshold=0.5):
        """
            Filters a list of trends by the following labels 'Politics', 'Entertainment', 'Sports', 'Miscellaneous'. 
            Keeping non-miscellaneous trends (further filtered through Naive Bayes Classifier separately). Using Bart-large transformer model @ Facebook. 

            #NEXT UP: https://soumilshah1995.blogspot.com/2021/04/simple-machine-learning-model-to.html. INCORPORATIVE NAIVE BAYES CLASSIFIER AND 
            ONLY SELECT TRENDS WITH CONSENSUS FILTERING

            default bart_threshold = 0.5 means that level of likelihood needed for addition to filtered list
        """ 
        classifier = pipeline("zero-shot-classification",
                      model="facebook/bart-large-mnli")
        candidate_labels = ['Politics', 'Entertainment', 'Sports', 'Miscellaneous']
        filtered_trends = [] 

        for trend in trend_list:
            bart_result = classifier(trend, candidate_labels) 
            max_score_index = bart_result['scores'].index(max(bart_result['scores'])) #we pick the largest associated score from the bart model.
            max_confidence_label = bart_result['labels'][max_score_index] #this is the name associated with the above index

            if max_confidence_label != "Miscellaneous" and bart_result['scores'][max_score_index] >= bart_threshold: #we set default threshold to 0.5 above (prevent weak choices from being selected.)
                filtered_trends.append(trend)

        return filtered_trends

    def upload_to_blob(self, image_url: str, prompt: str):
        """
        Takes a generated image and saves it to blob in Azure container. Named for trend.

        Return url of image in Blob storage afterwards
        """

        try:       
            response = requests.get(image_url, stream=True)
            if response.status_code == 200:
                #Can successfully access image -- now upload to blob using the container client defined in init

                #First need blob client, named after the prompt itself
                blob_client = self.blob_service_client.get_blob_client(container=self.container_name, blob=prompt)

                #Then, upload from url (because craiyon defaults to url -- better than saving locally)
                blob_client.upload_blob_from_url(image_url)
                return blob_client.url

            else:
                print(f"Failed to access image. Status code: {response.status_code}")
                return None
        except requests.RequestException as e:
            #Ambiguous exception, aside from failure Status code.
            print(f"Error accessing image: {e}")
            return None


    """
    Using Craiyon API wrapper to generate an image from a trend-name. Adding suffix "sketch" for prompt to combat inaccuracies with faces, specific features.
    Documentation @ FireHead90544/craiyon.py on Github

    Return url of image in Blob storage afterwards.

    """
    def generate(self, prompt: str):
        retries = 5
        generator = Craiyon()  # Instantiate the API wrapper


        while retries > 0: #If 
            try:
                result = generator.generate(prompt + "sketch")
                print(result.images)
                first_image_url = result.images[0]  # Access, Save the first image URL (don't want too many images)

                #Directly upload the image to the container, will make blob named after prompt
                output_url = self.upload_to_blob(first_image_url, prompt)  
                return output_url

                break 
            except ValueError as e: #includes JSONDecodeError
                print(f"JSON decode error: {e}")
                retries -= 1
                time.sleep(5)  # Wait for 5 seconds before retrying

            except HTTPError as e:
                if e.response.status_code == 405:  # Specific API error handling
                    print(f"Retrying with 405 error: {e}...")
                    retries -= 1
                    time.sleep(5)  # Wait for 5 seconds before retrying
                else:
                    print(f"HTTP error occurred: {e}")
                    raise  # Re-raise other HTTP errors

            except Exception as e:
                print(f"Unexpected error: {e}")
                raise  # Re-raise any other unexpected errors
        
        if retries == 0:
            print("Out of retries for generation -- check problem")


    def main(self):

        fetch_trends = self.query_trends(20)
        print("Original Trends:", fetch_trends)
        print("-----")
        filter_trends = self.filter_trends(fetch_trends)
        print("Filtered Trends: ", filter_trends) 
        #NEXT UP: FURTHER FILTER BY WHICH IS LIKELY TO CONTINUE DEVELOPING BASED ON BIWEEKLY TIME SERIES DATA AND PROPHET
        list_of_urls = []
        for trend in filter_trends:  
            output_url = self.generate(trend)
            list_of_urls.append(output_url)
        print(list_of_urls)
        


if __name__ == "__main__":
    script = CronScript() #make instance of CronScript class - and call main method
    script.main()

