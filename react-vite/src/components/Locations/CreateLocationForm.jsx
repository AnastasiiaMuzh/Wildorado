import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useDispatch } from "react-redux";
import { thunkCreateLocation } from "../../redux/locations";
import "./CreateLocationForm.css";

const categoryNames = {
  1: "Hiking",
  2: "Rafting",
  3: "Camping",
  4: "Climbing",
  5: "Snow Sports",
  6: "ATV/Bikes",
};

const categoryFields = {
  1: ["name", "city", "description", "elevation", "difficulty", "distance", "bestSeason"],
  2: ["name", "city", "description", "riverClass", "distance"],
  3: ["name", "city", "description", "maxTents", "fireAllowed", "lake", "distance"],
  4: ["name", "city", "description", "routeType", "difficulty", "elevation", "distance"],
  5: ["name", "city", "description", "bestSeason", "elevation", "distance"],
  6: ["name", "city", "description", "terrainType", "distance", "elevation"],
};

const enumOptions = {
  difficulty: ["Easy", "Medium", "Hard"],
  riverClass: ["I", "II", "III", "IV", "V"],
  routeType: ["Trad", "Sport"],
  terrainType: ["Dirt", "Rocky", "Forest", "Mixed"],
  fireAllowed: ["Yes", "No"],
  lake: ["Yes", "No"],
};

const CreateLocationForm = ( {existingLocation }) => {
  const navigate = useNavigate();
  const dispatch = useDispatch();

  const [selectedCategory, setSelectedCategory] = useState("");
  const [formData, setFormData] = useState({ images: ["", "", "", ""] });
  const [errors, setErrors] = useState({});
  const [successMessage, setSuccessMessage] = useState("");

  useEffect(() => {
    
  })

  const handleCategoryChange = (e) => {
    setSelectedCategory(Number(e.target.value));
    setFormData({ ...formData, categoryId: Number(e.target.value) });
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
    if (errors[name]) setErrors({ ...errors, [name]: "" });
  };

  const handleImageUrlChange = (index, e) => {
    const images = [...formData.images];
    images[index] = e.target.value;
    setFormData({ ...formData, images });
    if (errors.images) setErrors({ ...errors, images: "" });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const newErrors = {};

    if (!selectedCategory) newErrors.general = "Select a category.";

    // const requiredFields = categoryFields[selectedCategory] || [];
    // requiredFields.forEach((field) => {
    //   if (!formData[field]) newErrors[field] = `Field ${field} is required.`;
    // });

    ["distance", "elevation"].forEach((field) => {
        if (formData[field] !== undefined) {
            const value = parseFloat(formData[field]);
            if (Number.isNaN(value) || value <= 0) {
                newErrors[field] = `${field} must be a number greater than 0.`;
        }    }
    });

    const imageUrls = formData.images;

    if (imageUrls.some((url) => !url)) {
      newErrors.images = "All image fields must be filled.";
    } else if (new Set(imageUrls).size !== imageUrls.length) {
      newErrors.images = "All image URLs must be unique.";
    } else if (!imageUrls.every((url) => url.match(/\.(png|jpe?g)$/i))) {
      newErrors.images = "Images must be in .png, .jpg, or .jpeg format.";
    }

    if (Object.keys(newErrors).length) {
      return setErrors(newErrors);
    }

    const payload = {
      ...formData,
      distance: parseFloat(formData.distance),
      elevation: formData.elevation ? parseFloat(formData.elevation) : null,
      images: formData.images.map((url, i) => ({ url, preview: i === 0 })),
    };

    try {
      const newLoc = await dispatch(thunkCreateLocation(payload));
      setSuccessMessage("✅ Location created!");
      setTimeout(() => navigate(`/locations/${newLoc.id}`), 1500);
    } catch (err) {
      const mesErr = await err.json()
      console.error(mesErr)
      console.error(err.message)
      setErrors({ general: mesErr.message });
    }
  };

  return (
    <div className="create-location-form">
      <h2>Create a New Location</h2>
      <p>Important: All submitted information and photos must be accurate and truthful.
      Any false or misleading information may result in the removal of the location and could lead to account suspension or deletion.</p>
      {errors.general && <p className="error">{errors.general}</p>}
      {successMessage && <p className="success-message">{successMessage}</p>}

      <select value={selectedCategory} onChange={handleCategoryChange}>
        <option value="">-- Choose Category --</option>
        {Object.entries(categoryNames).map(([key, name]) => (
          <option key={key} value={key}>{name}</option>
        ))}
      </select>

      {selectedCategory && (
        <form onSubmit={handleSubmit}>
          {categoryFields[selectedCategory].map((field) => (
            <div key={field} className="form-group">
              <label>{field}</label>
              {enumOptions[field] ? (
                <select name={field} onChange={handleChange} required>
                  <option value="">Select {field}</option>
                  {enumOptions[field].map((opt) => (
                    <option key={opt} value={opt}>{opt}</option>
                  ))}
                </select>
              ) : (
                <input
                  type="text"
                  name={field}
                  value={formData[field] || ""}
                  onChange={handleChange}
                  required
                />
              )}
              {errors[field] && <p className="error">{errors[field]}</p>}
            </div>
          ))}

          <h3>Images</h3>
          {formData.images.map((img, i) => (
            <div key={i}>
              <input
                type="text"
                placeholder={i === 0 ? "Preview Image URL (.jpg/.png)" : "Image URL (.jpg/.png)"}
                value={img}
                onChange={(e) => handleImageUrlChange(i, e)}
              />
            </div>
          ))}
          {errors.images && <p className="error">{errors.images}</p>}

          <button type="submit">Create Location</button>
        </form>
      )}
    </div>
  );
};

export default CreateLocationForm;