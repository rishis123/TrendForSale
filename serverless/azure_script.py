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


class CronScript:

    """
    Returns a list of top [num_trends] trends from Google Trends.
    Using pytrends library for extracting trending searches.
    """
    def query_trends(self, num_trends):
        pytrends = TrendReq()
        df = pytrends.trending_searches(pn='united_states')
        trends_list = df.head(num_trends)[0].tolist() #Sole column labelled "0" - converted to list instead
        return trends_list

    """
    Filters a list of trends by the following labels 'Sports', 'Entertainment', 'Travel', 'Pets', 'Disaster/Danger', 
    'Miscellaneous', 'Politics', 'Health', 'Economy'. Only keeping trends in first 4 categories for merchandise.
    Using Bart-large transformer model @ Facebook. 

    #NEXT UP: https://soumilshah1995.blogspot.com/2021/04/simple-machine-learning-model-to.html. INCORPORATIVE NAIVE BAYES CLASSIFIER AND 
    ONLY SELECT TRENDS WITH CONSENSUS FILTERING
    """
    def filter_trends(self, trend_list):
        classifier = pipeline("zero-shot-classification",
                      model="facebook/bart-large-mnli")
        candidate_labels = ['Disaster/Danger', 'Sports', 'Entertainment', 'Politics', 'Health', 'Economy', 'Travel', 'Pets', 'Miscellaneous']
        filtered_trends = [] 

        for trend in trend_list:
            result = classifier(trend, candidate_labels) 
            
            max_score_index = result['scores'].index(max(result['scores']))
            max_confidence_label = result['labels'][max_score_index]
        
            if max_confidence_label in ['Sports', 'Entertainment', 'Travel', 'Pets']:
                filtered_trends.append(trend)

        return filtered_trends #List of (every trend, associated max label)

    def save_image(self, image_url: str, prompt: str):
        """
        Takes a generated image and saves it in /generated directory. [image_url] is the url of image to donwload.
        [prompt] is the name of the prompt, used to name the saved image. E.g., "lebron_james.webp"
        """
        try:
            response = requests.get(image_url, stream=True)
            if response.status_code == 200:
                path = Path.cwd() / "generated"  
                path.mkdir(parents=True, exist_ok=True)  # Create the /generated directory if it doesn't exist, where image will be saved
                save_path = path / f"{prompt}.webp" #Still save as webp file as before, just with specific prompt named
                with open(save_path, 'wb') as file:
                    file.write(response.content) #write to file
                print(f"Image saved successfully to {save_path}")
            else:
                print(f"Failed to download image. Status code: {response.status_code}")
        except requests.RequestException as e:
            print(f"Error downloading image: {e}")


    """
    Using Craiyon API wrapper to generate an image from a trend-name. Adding suffix "sketch" for prompt to combat inaccuracies with faces, specific features.
    Documentation @ FireHead90544/craiyon.py on Github
    """
    def generate(self, prompt: str):
        retries = 5
        generator = Craiyon()  # Instantiate the API wrapper
        while retries > 0:
            try:
                result = generator.generate(prompt + "sketch")
                print(result.description)  # Description about the generated images - Delete after testing
                first_image_url = result.images[0]  # Access, Save the first image URL
                self.save_image(first_image_url, prompt)  
                break #only save the first image that saves
            except HTTPError as e:
                if e.response.status_code == 405: #Common API error - unclear reason why
                    print(f"Received 405 error: {e}")
                    print("Retrying...")
                    retries -= 1
                    time.sleep(5)  # Wait for 5 seconds before retrying
                else:
                    raise  # Re-raise other HTTP errors


    def main(self):

        fetch_trends = self.query_trends(20)
        print("Original Trends:", fetch_trends)
        print("-----")
        filter_trends = self.filter_trends(fetch_trends)
        print("Filtered Trends: ", filter_trends) 
        #NEXT UP: FURTHER FILTER BY WHICH IS LIKELY TO CONTINUE DEVELOPING BASED ON BIWEEKLY TIME SERIES DATA AND PROPHET

        for trend in filter_trends: #Remember filter_trends is tuple with 3 items
            self.generate(trend)


if __name__ == "__main__":
    script = CronScript() #make instance of CronScript class - and call main method
    script.main()

