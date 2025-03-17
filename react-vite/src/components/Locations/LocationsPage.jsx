import { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { useLocation, useNavigate } from "react-router-dom"; // Для чтения query-параметров
import { thunkGetAllLocations } from "../../redux/locations"; 
import "./LocationsPage.css";
import Slider from "react-slick";
import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";



const LocationsPage = () => {
    const dispatch = useDispatch();
    const locations = useSelector((state) => state.locations.allLocations); // Локации из Redux
    const navigate = useNavigate();
    const [currentPage, setCurrentPage] = useState(1); 
    const [totalPages, setTotalPages] = useState(1); 
    const images = [
        "/images/loc1.png",
        "/images/loc2.png",
        "/images/lo3.png",
      ];

    const location = useLocation();  // даёт доступ к адресной строке браузера.
    const queryParams = new URLSearchParams(location.search);   // Читает параметры из URL
    const searchQuery = queryParams.get("search") || "";       // Поисковый запрос
    const category = queryParams.get("category") || null;
    

    useEffect(() => {
        const params = new URLSearchParams();
        
        if (searchQuery) params.set("search", searchQuery);
        if (category) params.set("category", category);
        params.set("page", currentPage);
        params.set("perPage", 12);

        dispatch(thunkGetAllLocations(`?${params.toString()}`)).then((data) => {
            if(!data) {
                return alert("Failed to load locations.Please try again!")
            }
            if (data?.Pagination) {
                setTotalPages(data.Pagination.totalPages);
            }
          });
    }, [ dispatch, currentPage, searchQuery, category ]);

    const sliderSettings = {
        dots: true,
        infinite: true,
        speed: 500,
        slidesToShow: 1,
        slidesToScroll: 1,
        autoplay: true,
        autoplaySpeed: 3000,
    };


      return (
       <div className="locations-page">
        {/* <h1>Find your outside </h1> */}
        <div className="carousel-container-loc">
                <Slider {...sliderSettings}>
                    {images.map((img, index) => (
                        <div key={index} className="carousel-slide-loc">
                            <img src={img} alt={`Slide ${index}`} className="carousel-image-loc" />
                            <div className="carousel-text-loc">
                            <h1 className="special-heading">Find your outside here ...</h1>
                            </div>
                        </div>
                    ))}
                </Slider>
            </div>
        <div className="locations-list">
            {locations.map((location) => (
            <div key={location.id} className="location-item-loc" onClick={() => navigate (`/locations/${location.id}`)} >
                <img src={location.imageUrl} alt={location.name} />
                <div className="location-header">
                    <h3>{location.name}</h3> 
                    {/* <div className="location-rating">
                    <span className="star">★</span> {location.avgRating} ({location.reviewCount} reviews)
                    </div> */}
                </div>
                <div className="location-info">
                <p>City: {location.city}</p>
                <div className="location-rating">
                    <span className="star">★</span> {location.avgRating} ({location.reviewCount} reviews)
                </div>
               </div>
            </div>
            ))}
        </div>

        <div className="pagination">
            {Array.from({ length: totalPages }, (_, i) => (
            <button
                key={i + 1}
                onClick={() => setCurrentPage(i + 1)}
                className={currentPage === i + 1 ? "active" : ""}
            >
                {i + 1}
            </button>
            ))}
        </div>
        </div>  
    );
    };

    export default LocationsPage;
