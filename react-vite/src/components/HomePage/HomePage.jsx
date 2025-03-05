import React, { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { thunkCategories } from "../../redux/categories";
import { Link } from "react-router-dom";
import "./HomePage.css";

const HomePage = () => {
  const dispatch = useDispatch();
  const categories = useSelector((state) => state.categories.allCategories);

  useEffect(() => {
    dispatch(thunkCategories());
  }, [dispatch]);

  if (!categories || categories.length === 0) {
    return <div>Loading categories...</div>;
  }

  return (
    <div className="home-container">
      <div className="fot-img">
        {/* <h1>Explore the best outdoor adventures</h1> */}
      </div>

      <div className="category-container">
        <p>Choose a category:</p>
        <ul>
          {categories.map((category) => (
            <li key={category.id}>
              <Link
                to={`/categories/${category.id}`}
                style={{ textDecoration: "none", fontSize: "18px" }}
              >
                {category.name}
              </Link>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default HomePage;
