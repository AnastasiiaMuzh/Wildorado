import { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { useParams, useNavigate} from "react-router-dom";
import { thunkCategory } from "../../redux/categories";

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
    <div>
      <h1>{categoryData.category.name}  Location</h1>
      <ul>
        {categoryData.locations.map((location) => (
          <li key={location.id} className="location-details" onClick={() => navigate (`/locations/${location.id}`)}>
            <img
              src={location.imageUrl}
              alt={location.name}
              style={{ width: "150px", height: "100px", objectFit: "cover" }}

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
};

export default CategoryDetailPage;
