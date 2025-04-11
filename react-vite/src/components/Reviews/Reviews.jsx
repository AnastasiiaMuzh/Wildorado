import { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { thunkGetReviews } from "../../redux/reviews";
import CreateReview from "./CreateReview";
import './Reviews.css'
import { FaEdit, FaTrash } from "react-icons/fa";
import { useModal } from "../../context/Modal";
import OpenModalButton from "../OpenModalButton";
import EditReviewModal from "./EditReviewModal";
import DeleteReviewModal from "./DeleteReviewModal";


const Reviews = ({ locationId }) => {
    const dispatch = useDispatch();
    const { openModal } = useModal(); 
    const reviewsObj = useSelector((state) => state.reviews);
    const reviews = Object.values(reviewsObj); //convert to array for map
    const sessionUser = useSelector(state => state.session.user);
    const location = useSelector(state => state.locations.locationDetail);

    const [formVisible, setFormVisible] = useState(true);

    const isOwner = location?.owner?.id === sessionUser?.id;
    const alreadyReviewed = reviews.some(review => review.user?.id === sessionUser?.id);

    useEffect(() => {
        dispatch(thunkGetReviews(locationId));
      }, [dispatch, locationId]);
    
    useEffect(() => {
    if (isOwner || alreadyReviewed) {
        setFormVisible(false);
    } else {
        setFormVisible(true);
    }
    }, [isOwner, alreadyReviewed]);


    return (
        <div className="reviews-container">
            <h2>REVIEWS</h2>

            {sessionUser && formVisible && (
                <CreateReview locationId={locationId} onSuccess={() => setFormVisible(false)} />
            )}

            {reviews.length === 0 && <p>No reviews yet.</p>}
         
            {reviews.map(review => (
                <div key={review.id} className="review-item">
                <div className="review-header">
                    <strong>{review.user?.username}</strong>
                    <div className="review-stars">
                        {[1, 2, 3, 4, 5].map((num) => (
                            <span key={num} className={num > review.stars ? 'star empty' : 'star filled'}>
                                {num <= review.stars ? '⭐' : '☆'}
                            </span>                          
                        ))}
                    </div>
                </div>
                <p>{review.text}</p>
                {review.image && <img src={review.image.url} alt="review" />}
                
                {review.user?.id === sessionUser?.id && (
                    <div className="review-actions">
                        <OpenModalButton
                        buttonText={<FaEdit className="green-icon" />}
                        modalComponent={
                            <EditReviewModal
                            review={review}
                            locationId={locationId}
                            /> 
                        }
                        // Чтобы не переходить на другую страницу при клике, если нужно
                        // onButtonClick={(e) => {
                        // e.stopPropagation();
                        // e.preventDefault();
                        // }}
                        />
                        <OpenModalButton
                        buttonText={<FaTrash className="red-icon" />}
                        modalComponent={
                            <DeleteReviewModal
                            reviewId={review.id}
                            locationId={locationId}
                            />
                        }
                        // onButtonClick={(e) => {
                        //     e.stopPropagation();
                        //     e.preventDefault();
                        // }}
                        />

                    </div>
                )}
                </div>
            ))}
            
        </div>
      );
      
};

export default Reviews;