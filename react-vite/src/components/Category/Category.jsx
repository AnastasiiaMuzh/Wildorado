import { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { useParams, useNavigate} from "react-router-dom";
import { thunkCategory } from "../../redux/categories";
import "../Locations/LocationsPage.css";
import "./Category.css"


const CategoryDetailPage = () => {
  const { id } = useParams(); 
  const dispatch = useDispatch();
  const categoryData = useSelector((state) => state.categories.currentCategory);
  const navigate = useNavigate();
  

  
  useEffect(() => {
    dispatch(thunkCategory(id));
  }, [dispatch, id]);

  if (!categoryData) return <div>Loading category details...</div>;


  return (
    <div className="locations-page"> {/* Этот класс позволит применять стили */}
      <h1 className="cat-cat">{categoryData.category.name} Locations</h1>
      <ul className="locations-list">
        {categoryData.locations.map((location) => (
          <li key={location.id} className="location-item-loc" onClick={() => navigate (`/locations/${location.id}`)}>
            <img
              src={location.imageUrl}
              alt={location.name}
              className="location-image-loc"
            />
            <div>
              <h3>{location.name}</h3>
              <div className="category-description">
                <p>📍 City: {location.city}</p>
                <p>★ {location.avgRating} ({location.reviewCount} reviews)</p>
              </div>
            </div>
          </li>
        ))}
      </ul>
    </div>
);
}

export default CategoryDetailPage;
