// ---------- ACTION TYPES ----------
const LOAD_REVIEWS = 'reviews/LOAD';
const ADD_REVIEW = 'reviews/ADD';
const UPDATE_REVIEW = 'reviews/UPDATE';
const DELETE_REVIEW = 'reviews/DELETE';


// ---------- ACTION CREATORS ----------
const loadReviews = (reviews) => ({
    type: LOAD_REVIEWS,
    reviews
})

const addReview = (review) => ({
    type: ADD_REVIEW,
    review
})

const updateReview = (review) => ({
    type: UPDATE_REVIEW,
    review
})

const deleteReview = (reviewId) => ({
    type: DELETE_REVIEW,
    reviewId
})


// ---------- THUNKS ----------
export const thunkGetReviews = (locationId) => async (dispatch) => {
    const res = await fetch(`/api/reviews/locations/${locationId}`);
    if (res.ok) {
      const data = await res.json();
      dispatch(loadReviews(data));
    }
  };


  export const thunkCreateReview = (locationId, payload) => async (dispatch) => {
    const res = await fetch(`/api/reviews/locations/${locationId}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    });
    if (res.ok) {
        const newReview = await res.json();
        dispatch(addReview(newReview));
        return newReview;
    }
};



export const thunkUpdateReview = (reviewId, payload) => async (dispatch) => {
    const res = await fetch(`/api/reviews/${reviewId}`, {
        method: 'PUT',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(payload)
    });
    if (res.ok) {
        const update = await res.json();
        dispatch(updateReview(update));
        return update;
    }
};


export const thunkDeleteReview = (reviewId) => async (dispatch) => {
    const res = await fetch(`/api/reviews/${reviewId}`, {
      method: "DELETE"
    });
    if (res.ok) {
      dispatch(deleteReview(reviewId));
    }
  };


// ---------- REDUCER ----------
const initialState = {};

export default function reviewsReducer(state = initialState, action) {
  switch (action.type) {
    case LOAD_REVIEWS:
      const newState = {};
      action.reviews.forEach(review => {
        newState[review.id] = review;
      });
      return newState;
    case ADD_REVIEW:
      return { ...state, [action.review.id]: action.review };
    case UPDATE_REVIEW:
      return { ...state, [action.review.id]: action.review };
    case DELETE_REVIEW:
      const nextState = { ...state };
      delete nextState[action.reviewId];
      return nextState;
    default:
      return state;
  }
}

