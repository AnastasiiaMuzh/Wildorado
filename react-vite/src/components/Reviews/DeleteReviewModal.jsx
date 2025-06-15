import { useDispatch } from "react-redux";
import { useModal } from "../../context/Modal";
import { thunkDeleteReview } from "../../redux/reviews";
import "./Reviews.css";

const DeleteReviewModal = ({ reviewId, onDeleteSuccess }) => {
  const dispatch = useDispatch();
  const { closeModal } = useModal();

  const handleDelete = async () => {
    await dispatch(thunkDeleteReview(reviewId));
    if (onDeleteSuccess) onDeleteSuccess();
    closeModal();
  };

 return (

    <div className="delete-review-modal">
    <h2>Confirm Deletion</h2>
    <p>Are you sure you want to delete this review?</p>

    <div className="delete-review-buttons">
        <button className="cancel-rev-btn" onClick={closeModal}>Cancel</button>
        <button className="confirm-rev-btn" onClick={handleDelete}>Delete</button>
    </div>
    </div>
    
  );
};

export default DeleteReviewModal;