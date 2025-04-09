import { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { thunkGetReviews } from "../../redux/reviews";

const Reviews = ({ locationId }) => {
    const dispatch = useDispatch();

    const reviewsObj = useSelector((state) => state.reviews);
    const reviews = Object.values(reviewsObj); //convert to array for map
    const sessionUser = useSelector(state => state.session.user);

    useEffect(() => {
        dispatch(thunkGetReviews(locationId))
    },[dispatch, locationId]);

    return (
        <div className="reviews-container">

            <h2>REVIEWS</h2>
          
            {(!reviews || reviews.length === 0) && <p>No reviews yet.</p>}
            {reviews?.map(review => (
                <div key={review.id} className="review-item">
                <div className="review-header">
                    <strong>{review.user?.username}</strong>
                    <div className="review-stars">
                        {[1, 2, 3, 4, 5].map((num) => (
                            <span key={num}>
                            {num <= review.stars ? '⭐' : '☆'}
                            </span>
                        ))}
                    </div>

                </div>
                <p>{review.text}</p>
                {review.image && <img src={review.image.url} alt="review" />}
                
                {review.user?.id === sessionUser?.id && (
                    <div className="review-actions">
                    {/* Кнопки редактирования и удаления */}
                    </div>
                )}
                </div>
            ))}
        </div>
      );
      
};

export default Reviews;