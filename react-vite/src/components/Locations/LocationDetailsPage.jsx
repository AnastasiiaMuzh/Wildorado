import { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { thunkGetLocationDetails } from "../../redux/locations"; 
import "./LocationsDetailsPage.css";
import { useParams, Link } from "react-router-dom";
import { thunkCategory } from "../../redux/categories";

const LocationDetailsPage = (locationId) => {
    const dispatch = useDispatch();
    const { id } = useParams(); //ID from URL
    // console.log("Location ID from URL: ", id);
    const location = useSelector((state) => state.locations.locationDetail);
    const categoryData = useSelector((state) => state.categories.currentCategory);

    useEffect(() => {
        dispatch(thunkGetLocationDetails(id)).then((location) => {
            if (location?.categoryId) {
                dispatch(thunkCategory(location.categoryId));
            }
        });
    }, [dispatch, id]);

    if (!location || !categoryData) {
        return <p>Loading...</p>;
    }


    return (
        <div className="location-detail">
            {/* <Link to="/locations" className="back-link">
                ← Back to Locations
            </Link> */}

            <h1>{location.name}</h1>
            <p>📍
            {location.city}</p>
            <p>★ {location.avgRating} ({location.reviewCount} reviews)</p>
            
            {location?.images?.map(img => (
                <img key={img.id} src={img.url} alt="Location" style={{ width: "150px", height: "100px", objectFit: "cover" }}/>
            ))}
            <h2>About {location.name}</h2>
            <p>{location.description}</p>
            <ul>
                {Object.entries(location.categorySpecific || {}).map(([key, value]) => (
                    <li key={key}>
                        <strong>{key}: </strong> 
                        {typeof value === "boolean" ? (value ? "Yes" : "No") : value}
                    </li>
                ))}
            </ul>

            <h2>Plan Your Trip</h2>
            <p>Organize a {categoryData.category.name} event or join others planning to visit {location.name}.</p>
            <button>Create Event</button>

            <div className="reviews-locDetails">
                <h2>REVIEWS</h2>

            </div>
        </div>

    );
};

export default LocationDetailsPage;

