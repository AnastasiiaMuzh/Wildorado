import { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { thunkGetLocationDetails } from "../../redux/locations"; 
import { useParams } from "react-router-dom";
import { thunkCategory } from "../../redux/categories";
import OpenModalButton from '../OpenModalButton/OpenModalButton';
import CreateEventFormModal from "../EventForm/CreateEventForm";
import './LocationsDetailsPage.css';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';

  
const LocationDetailsPage = () => { //ubrala locationId iz ()
    const dispatch = useDispatch();
    const { id } = useParams(); //ID from URL
    const user = useSelector((state) => state.session.user);
    const location = useSelector((state) => state.locations.locationDetail);
    const categoryData = useSelector((state) => state.categories.currentCategory);
    
    const [currentSlide, setCurrentSlide] = useState(0);
    const [coordinates, setCoordinates] = useState(null);


    useEffect(() => {
        dispatch(thunkGetLocationDetails(id)).then((location) => {
            if (location?.categoryId) {
                dispatch(thunkCategory(location.categoryId));
            }
        });
    }, [dispatch, id]);


    useEffect(() => {
        setCoordinates(null); // 1. Сброс координат, чтобы убрать старую карту
      }, [location?.id]); // реагируем на смену location


    useEffect(() => {
        const fetchCoordinates = async () => {
            const query = encodeURIComponent(`${location.name}, ${location.city}, Colorado, USA`); //assemble the search string: location name + city + state + country
            const res = await fetch(
                `https://nominatim.openstreetmap.org/search?q=${query}&format=json`,
                {
                  headers: {
                    "User-Agent": "YourAppName/1.0 (your_email@example.com)"
                  }
                }
              );
              
            const data = await res.json();

            if (data && data.length > 0) {
                setCoordinates([parseFloat(data[0].lat), parseFloat(data[0].lon)]);
            } else {
                setCoordinates([39.5501, -105.7821]);
            }
        };
        if (location?.name && location?.city) {
            fetchCoordinates();
        }
    }, [location]);


    const images = location?.images || [];

    const nextSlide = () => {
        setCurrentSlide((prev) => (prev + 1) % images.length);
    };

    const prevSlide = () => {
        setCurrentSlide((prev) => (prev - 1 + images.length) % images.length);
    };

    if (!location || !categoryData) {
        return <p>Loading...</p>;
    }

    return (
        <div className="location-detail-main">
            <div className="details-left">
                <div className="details-header">
                    <h1 className="location-title">{location.name}</h1>
                    
                </div>
                
                <div className="location-city-rating">
                    <p>📍 {location.city}</p>
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
                <div className="about-details">
                    <h2>About {location.name}:</h2>
                    <p>{location.description}</p>
                </div>
                    
                <div className="reviews-loc-details">
                    <h2>REVIEWS</h2>
                </div>
            </div>
            <div className="details-right">
            <div className="trip-plan">   
                    <h2>Plan Your Trip</h2>
                    <p>Organize a {categoryData.category.name} event or join others planning to visit {location.name}.</p>
                    
                    {user ? (
                        <OpenModalButton 
                          buttonText="Create Event"
                          modalComponent={<CreateEventFormModal locationId={location.id}/>}
                        />
                        // <button onClick={() => navigate(`/events/new?locationId=${id}`)}>
                        //     Create Event
                        // </button>
                    ) : (
                        <p style={{ color: "red", fontWeight: "bold" }}>
                            To create your own event, please log in to your account.
                        </p>
                    )}
                </div> 
                <div className="map-loc">
                {coordinates && (
                    <MapContainer
                        key={coordinates?.join(',')}
                        center={coordinates}
                        zoom={12}
                        className="leaflet-container"
                        >
                            <TileLayer
                            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                            attribution='&copy; OpenStreetMap contributors'
                            />
                            <Marker position={coordinates}>
                                <Popup>
                                    {location.name} <br /> 📍 {location.city}
                                </Popup>
                            </Marker>
                    </MapContainer>
                    )}
                </div>
            </div>

        </div>

    );
};

export default LocationDetailsPage;

{/* <MapContainer> — контейнер с картой. Мы ставим центр карты на найденные координаты.
<TileLayer> — слой с изображениями карты (в данном случае — OpenStreetMap).
<Marker> — маркер на карте.
<Popup> — всплывающее окно при клике на маркер (пишем название и город). */}

