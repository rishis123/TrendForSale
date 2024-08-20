import Banner from "./Banner";
import FeatureProduct from "./FeatureProduct";
import ScrollToTopOnMount from "../template/ScrollToTopOnMount";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { Link } from "react-router-dom";
import { useEffect, useState } from 'react';
import axios from 'axios';

// Below function fetches metadata from backend server, which must be up and running. Dummy function.

function Landing() {

  const [data, setData] = useState(null);
  useEffect(() => {
    const fetchData = async () => {
      try {
        const url = process.env.REACT_APP_API_URL + "/metadata"
        const response = await axios.get(url);
        setData(response.data);
      } catch (error) {
        console.log(error);
        console.log("Error");
      }
    };

    fetchData();
  }, []);

  return (
    <>
      <ScrollToTopOnMount />
      <Banner />
      <div className="d-flex flex-column bg-white py-4">
        <h1 className="text-center px-5"> Trend For Sale </h1>
        <p className="text-center px-5">
          Browse through my AI-generated shirts -- orders fulfilled by Shopify.
        </p>
        <div className="d-flex justify-content-center">
          <Link to="/products" className="btn btn-primary" replace>
            Browse products
          </Link>
        </div>

        <div>
          {data ? (
            <div>Data: {JSON.stringify(data)}</div>
          ) : (
            <div>Loading...</div>
          )}
        </div>

      </div>
      <h2 className="text-muted text-center mt-4 mb-3">New Arrivals</h2>
      <div className="container pb-5 px-lg-5">
        <div className="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4 px-md-5">
          {Array.from({ length: 6 }, (_, i) => {
            return <FeatureProduct key={i} />;
          })}
        </div>
      </div>
      <div className="d-flex flex-column bg-white py-4">
        <h5 className="text-center mb-3">Follow us on</h5>
        <div className="d-flex justify-content-center">
          <a href="https://www.linkedin.com/in/rishi-shah123/" className="me-3">
            <FontAwesomeIcon icon={["fab", "linkedin"]} size="2x" />
          </a>
          <a href="https://www.instagram.com/irishhash123/">
            <FontAwesomeIcon icon={["fab", "instagram"]} size="2x" />
          </a>
          <a href="https://github.com/rishis123" className="ms-3">
            <FontAwesomeIcon icon={["fab", "github"]} size="2x" />
          </a>
        </div>
      </div>
    </>
  );
}

export default Landing;
