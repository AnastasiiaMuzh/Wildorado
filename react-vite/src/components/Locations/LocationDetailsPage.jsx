import { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { thunkGetLocationDetails } from "../../redux/locations"; 
import { useParams, useNavigate } from "react-router-dom";
import { thunkCategory } from "../../redux/categories";
import './LocationsDetailsPage.css'


const LocationDetailsPage = () => { //ubrala locationId iz ()
    const dispatch = useDispatch();
    const navigate = useNavigate();
    const { id } = useParams(); //ID from URL
    const user = useSelector((state) => state.session.user);
    const location = useSelector((state) => state.locations.locationDetail);
    const categoryData = useSelector((state) => state.categories.currentCategory);
    
    const [currentSlide, setCurrentSlide] = useState(0);

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

    const images = location?.images || [];

    const nextSlide = () => {
        setCurrentSlide((prev) => (prev + 1) % images.length);
    };

    const prevSlide = () => {
        setCurrentSlide((prev) => (prev - 1 + images.length) % images.length);
    };



    return (
        <div className="location-detail">
            <div className="details-header">
                <h1 className="location-title">{location.name}</h1>
                <p className="location-city">📍 {location.city}</p>
                <div className="location-rating">
                    <span className="star">★</span> {location.avgRating} ({location.reviewCount} reviews)
                </div>
            </div>
            {images.length > 0 && (
                <div className="carousel-container-details">
                    <button className="carousel-arrow left" onClick={prevSlide}>❮</button>
                    <img key={images[currentSlide].id} src={images[currentSlide].url} alt="Location" className="carousel-image"/>
                    <button className="carousel-arrow right" onClick={nextSlide}>❯</button>
                </div>
            )}

            <div className="details-filter">
            <div className="details-grid">
                {Object.entries(location.categorySpecific || {}).map(([key, value]) => (
                    <div key={key} className="details-box">
                        <strong>{key.replace(/([A-Z])/g, " $1").trim()}:</strong>
                        <span>{typeof value === "boolean" ? (value ? "Yes" : "No") : value}</span>
                    </div>
                ))}
            </div>

            </div>
            {/* {location?.images?.map(img => (
                <img key={img.id} src={img.url} alt="Location" style={{ width: "150px", height: "100px", objectFit: "cover" }}/>
            ))} */}
            <h2>About {location.name}</h2>
            <p>{location.description}</p>
            
            <div className="trip-plan">   
                <h2>Plan Your Trip</h2>
                <p>Organize a {categoryData.category.name} event or join others planning to visit {location.name}.</p>
                
                {user ? (
                    <button onClick={() => navigate(`/events/new?locationId=${id}`)}>
                        Create Event
                    </button>
                ) : (
                    <p style={{ color: "red", fontWeight: "bold" }}>
                        To create your own event, please log in to your account.
                    </p>
                )}
            </div> 

            <div className="reviews-locDetails">
                <h2>REVIEWS</h2>

            </div>
        </div>

    );
};

export default LocationDetailsPage;

