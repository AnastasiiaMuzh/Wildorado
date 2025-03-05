import { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { thunkCategories } from "../../redux/categories";
import { Link } from "react-router-dom";
import "./HomePage.css";
import Carousel from "./Carousel";

const HomePage = () => {
  const dispatch = useDispatch();
  const categories = useSelector((state) => state.categories.allCategories);

  const categoriesImg = {
    Hiking: "/images/hiking.png",
    Rafting: "/images/rafting.png",
    Camping: "/images/camping.png",
    Climbing: "/images/climbing.png",
    "Snow Sports": "/images/snow_sports.png",
    "ATV/Bikes": "/images/atv_bikes.png",
  };

  useEffect(() => {
    dispatch(thunkCategories());
  }, [dispatch]);

  if (!categories || categories.length === 0) {
    return <div>Loading categories...</div>;
  }

  return (
    <div className="home-container">
      {/* <div className="fot-img"> */}
        {/* <h1>Explore the best outdoor adventures</h1> */}
      {/* </div> */}
      <Carousel />

      <div className="category-container">
        {/* <p>Choose a category:</p> */}
        <ul className="category-list">
        {categories.map((category) => (
            <li key={category.id} className="category-item">
              <Link to={`/categories/${category.id}`} className="category-link">
              <img
                  src={categoriesImg[category.name] || "/images/default.png"}
                  alt={category.name}
                  className="category-icon"
                />
                <span>{category.name}</span>
              </Link>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default HomePage;
