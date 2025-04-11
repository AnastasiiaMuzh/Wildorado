import { useState } from "react";
import { useDispatch } from "react-redux";
import { thunkCreateReview } from "../../redux/reviews";
import { thunkGetLocationDetails } from "../../redux/locations";
import { useDropzone } from 'react-dropzone';
import './Reviews.css';

const CreateReview = ({ locationId, onSuccess }) => {
  const dispatch = useDispatch();
  const [stars, setStars] = useState(0);
  const [text, setText] = useState("");
  const [imageUrl, setImageUrl] = useState("");
  const [errors, setErrors] = useState([]);
  

  //DROPZONE to upload an image
  const { getRootProps, getInputProps } = useDropzone({
    onDrop: acceptedFiles => {
      const file = acceptedFiles[0];
      if (file) {
        const url = URL.createObjectURL(file); // локальный preview
        setImageUrl(url);
      }
    }
  });


  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrors([]);

    if (!text.trim()) {
      setErrors(["Review text is required"]);
      return;
    }

    const payload = {
      stars,
      text,
      imageUrl: imageUrl.trim() || null
    };

    try {
      const res = await dispatch(thunkCreateReview(locationId, payload));
      if (res?.errors) {
        setErrors(res.errors);
      } else {
        await dispatch(thunkGetLocationDetails(locationId));
        setStars(0);
        setText("");
        setImageUrl("");
        if (onSuccess) onSuccess();
      }
    } catch (err) {
      setErrors(["Something went wrong"]);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="review-form">
      <h2>Leave a Review</h2>

      <label>Rating:</label>
      <div className="star-rating">
        {[1, 2, 3, 4, 5].map((num) => (
            <span
            key={num}
            className={num <= stars ? "star filled" : "star empty"}
            onClick={() => setStars(num)}
            >
                ★
            </span>
        ))}
        </div>

        <label>Review:</label>
        <textarea
            value={text}
            onChange={(e) => setText(e.target.value)}
            rows={4}
            placeholder="Write your thoughts..."
            className={errors.includes("Review text is required") ? "input-error" : ""}
        />
        {errors.includes("Review text is required") && (
            <p className="field-error">Review text is required</p>
        )}

        <label>Paste image URL (optional):</label>
        <input
            type="text"
            value={imageUrl}
            onChange={(e) => setImageUrl(e.target.value)}
            placeholder="https://example.com/image.jpg"
        />

        <div {...getRootProps()} className="dropzone">
            <input {...getInputProps()} />
            <p>Or drag & drop an image here</p>
        </div>

        {imageUrl && (
            <div className="image-preview">
            <img src={imageUrl} alt="preview" style={{ maxWidth: '200px' }} />
            </div>
        )}

        <button className="submit-review" type="submit">Submit</button>
        </form>
  );
};

export default CreateReview;
