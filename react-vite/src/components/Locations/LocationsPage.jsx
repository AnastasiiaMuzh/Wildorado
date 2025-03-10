import { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { useLocation, useNavigate } from "react-router-dom"; // Для чтения query-параметров
import { thunkGetAllLocations } from "../../redux/locations"; 
import "./LocationsPage.css";


const LocationsPage = () => {
    const dispatch = useDispatch();
    const locations = useSelector((state) => state.locations.allLocations); // Локации из Redux
    const navigate = useNavigate();
    const [currentPage, setCurrentPage] = useState(1); 
    const [totalPages, setTotalPages] = useState(1); 

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


      return (
        <div className="locations-page">
        <h1>All Locations</h1>

        <div className="locations-list">
            {locations.map((location) => (
            <div key={location.id} className="location-item" onClick={() => navigate (`/locations/${location.id}`)} >
                <img src={location.imageUrl} alt={location.name} style={{ width: "150px", height: "100px", objectFit: "cover" }}/>
                <h3>{location.name}</h3>
                <p>City: {location.city}</p>
                <p>★ {location.avgRating} ({location.reviewCount} reviews)</p>
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
