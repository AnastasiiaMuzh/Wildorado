// src/components/Reviews/EditReviewModal.js
import { useState } from "react";
import { useDispatch } from "react-redux";
import { useDropzone } from 'react-dropzone';
import { useModal } from "../../context/Modal";
import { thunkUpdateReview } from "../../redux/reviews";
import { thunkGetLocationDetails } from "../../redux/locations";
import './Reviews.css'


function EditReviewModal({ review, locationId, onEditSuccess }) {
  const dispatch = useDispatch();
  const { closeModal } = useModal();

  const [stars, setStars] = useState(review?.stars || 0);
  const [text, setText] = useState(review?.text || "");
  const [imageUrl, setImageUrl] = useState(review?.image?.url || "");
  const [errors, setErrors] = useState([]);

  //DROPZONE to upload an image
  const { getRootProps, getInputProps } = useDropzone({
    onDrop: acceptedFiles => {
      const file = acceptedFiles[0];
      if (file) {
        const url = URL.createObjectURL(file); // Локальный preview
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

    if (!imageUrl.trim() && review?.image?.url) {
      payload.deleteImage = true;
    }

    try {
      const res = await dispatch(thunkUpdateReview(review.id, payload));
      if (res?.errors) {
        setErrors(res.errors);
      } else {
        await dispatch(thunkGetLocationDetails(locationId));
        if (onEditSuccess) onEditSuccess();
        closeModal();
      }
    } catch (err) {
      setErrors(["Something went wrong"]);
    }
  };

  return (
    <div className="edit-review-container">
      <h2>Edit your Review</h2>
      <form onSubmit={handleSubmit} className="edit-review-form">

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
          className={errors.includes("Review text is required") ? "input-error" : ""}
        />
        {errors.includes("Review text is required") && (
          <p className="field-error">Review text is required</p>
        )}

        <label>Image URL (optional):</label>
        <input
          type="text"
          value={imageUrl}
          onChange={(e) => setImageUrl(e.target.value)}
          placeholder="https://example.com/image.jpg"
        />


        <label>Upload new image (optional):</label>

        <div {...getRootProps()} className="dropzone">
          <input {...getInputProps()} />
          <p>Or drag & drop an image here</p>
        </div>

        {imageUrl && (        
          <div className="image-preview">
            <img src={imageUrl} alt="preview" style={{ maxWidth: '200px' }} />
            <button
              type="button"
              className="delete-image-btn"
              onClick={() => setImageUrl("")}
              title="Remove image"
            >
              ❌
            </button>
          </div>
        )}

        {errors.map((err, i) => <p key={i} className="field-error">{err}</p>)}

        <button type="submit">
          Save Changes
        </button>
      </form>
    </div>
  );
}

export default EditReviewModal;
