import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { categoryNames, categoryFields, enumOptions } from "./LocationForm.utils";


const LocationForm = ({initialData, onSubmit, submitButtonText,   disableCategory = false}) => {
  const navigate = useNavigate();
  const [selectedCategory, setSelectedCategory] = useState(initialData.categoryId || "");
  const [formData, setFormData] = useState(initialData);
  const [errors, setErrors] = useState({});
  const [successMessage, setSuccessMessage] = useState("");


  const handleCategoryChange = (e) => {
    const newCat = Number(e.target.value);
    setSelectedCategory(newCat);
    setFormData((prev) => ({ ...prev, categoryId: newCat }));
  };


  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
    if (errors[name]) {
      setErrors((prevErr) => ({ ...prevErr, [name]: "" }));
    }
  };

  // Изменение картинок
  const handleImageUrlChange = (index, e) => {
    const images = [...formData.images];
    images[index] = e.target.value;
    setFormData((prev) => ({ ...prev, images }));
    if (errors.images) {
      setErrors((prevErr) => ({ ...prevErr, images: "" }));
    }
  };


  const validate = () => {
    const newErrors = {};
    if (!selectedCategory) {
      newErrors.general = "Select a category.";
    }
    // distance, elevation > 0?
    ["distance", "elevation"].forEach((field) => {
      if (formData[field]) {
        const val = parseFloat(formData[field]);
        if (Number.isNaN(val) || val <= 0) {
          newErrors[field] = `${field} must be a number > 0.`;
        }
      }
    });


    const nonEmptyImages = formData.images.filter((url) => url !== "");
    if (nonEmptyImages.length === 0) {
      newErrors.images = "At least one image is required.";
    } else if (new Set(nonEmptyImages).size !== nonEmptyImages.length) {
      newErrors.images = "All image URLs must be unique.";
    } else if (!nonEmptyImages.every((url) => /\.(png|jpe?g)$/i.test(url))) {
      newErrors.images = "Images must end with .png/.jpg/.jpeg";
    }

    return newErrors;
  };


  const handleSubmit = async (e) => {
    e.preventDefault();
    const newErrors = validate();
    if (Object.keys(newErrors).length) {
      setErrors(newErrors);
      return;
    }

    // Собираем payload по нужным полям
    const relevantFields = categoryFields[selectedCategory] || [];
    const payload = { categoryId: selectedCategory };

    relevantFields.forEach((field) => {
      switch (field) {
        case "distance":
          payload.distance = parseFloat(formData.distance) || 0;
          break;
        case "elevation":
          payload.elevation = formData.elevation
            ? parseFloat(formData.elevation)
            : null;
          break;
        case "fireAllowed":
          payload.fireAllowed = formData.fireAllowed === "Yes";
          break;
        case "lake":
          payload.lake = formData.lake === "Yes";
          break;
        case "maxTents":
          payload.maxTents = formData.maxTents
            ? parseInt(formData.maxTents, 10)
            : null;
          break;
          case "riverClass":
          payload.riverClass = formData.riverClass;
          break;  
        default:
          payload[field] = formData[field];
          break;
      }
    });

    // Add img
    payload.images = formData.images
      .filter((url) => url !== "")
      .map((url, i) => ({ url, preview: i === 0 }));

    // Обрезаем name/city
    if (payload.name) payload.name = payload.name.trim();
    if (payload.city) payload.city = payload.city.trim();

    console.log("SUBMIT payload:", payload);

  
  try {
    const result = await onSubmit(payload); // вызываем переданный проп
    if (result) {
      setSuccessMessage(`${submitButtonText} successful!`);
      setTimeout(() => navigate(`/locations/${result.id}`), 1000);
    } else {
      setErrors({ general: "Operation failed." });
    }
  } catch (err) {
    console.error("Submission error:", err);
    let errorMessage = err.message || "Error during submission";
    // Если err имеет метод json (например, это Response), попробуем получить сообщение из него:
    if (err.json) {
      try {
        const errData = await err.json();
        if (errData && errData.message) {
          errorMessage = errData.message;
        }
      } catch (jsonErr) {
        console.error("Error parsing error response:", jsonErr);
      }
    }
    setErrors({ general: errorMessage });
  }
}

  return (
    <div className="create-location-form">
      <h2>{submitButtonText}</h2>
      <p>
        Important: All submitted information and photos must be accurate and truthful.
        Any false or misleading information may result in removal or account suspension.
      </p>
      {errors.general && <p className="error">{errors.general}</p>}
      {successMessage && <p className="success-message">{successMessage}</p>}

      <label>Category:</label>
      <select
        value={selectedCategory || ""}
        onChange={handleCategoryChange}
        disabled={disableCategory}
      >
        <option value="">-- Choose Category --</option>
        {Object.entries(categoryNames).map(([key, val]) => (
          <option key={key} value={key}>
            {val}
          </option>
        ))}
      </select>

      {selectedCategory && (
        <form onSubmit={handleSubmit}>
          {categoryFields[selectedCategory].map((field) => (
            <div key={field} className="form-group">
              <label>{field}</label>
              {enumOptions[field] ? (
                <select
                  name={field}
                  value={formData[field] || ""}
                  onChange={handleChange}
                  required
                >
                  <option value="">Select {field}</option>
                  {enumOptions[field].map((opt) => (
                    <option key={opt} value={opt}>
                      {opt}
                    </option>
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
          {formData.images.map((imgUrl, i) => (
            <div key={i}>
              <input
                type="text"
                placeholder={
                  i === 0
                    ? "Preview Image URL (.jpg/.png)"
                    : "Image URL (.jpg/.png)"
                }
                value={imgUrl}
                onChange={(e) => handleImageUrlChange(i, e)}
              />
            </div>
          ))}
          {errors.images && <p className="error">{errors.images}</p>}

          <button type="submit">{submitButtonText}</button>
        </form>
      )}
    </div>
  );
};

export default LocationForm;

