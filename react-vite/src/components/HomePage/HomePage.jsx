import { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { thunkCategories } from "../../redux/categories";
import { Link } from "react-router-dom";

const HomePage = () => {
  const dispatch = useDispatch();
  const categories = useSelector((state) => state.categories.allCategories);

  console.log("Categories from Redux:", categories); 

  useEffect(() => {
    dispatch(thunkCategories());
  }, [dispatch]);

  if (!categories || categories.length === 0) {
    return <div>Loading categories...</div>;
  }

  return (
    <div>
      <h1>Welcome to Wildorado!</h1>
      <p>Choose a category:</p>
      <ul>
        {categories.map((cat) => (
          <li key={cat.id}>
            <Link to={`/categories/${cat.id}`} style={{ textDecoration: "none", fontSize: "18px" }}>
              {cat.name}
            </Link>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default HomePage;
