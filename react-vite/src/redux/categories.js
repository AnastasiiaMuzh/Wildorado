import { csrfFetch } from "./csrf";

// ---------- ACTION TYPES ----------
const GET_CATEGORIES = "categories/GET_CATEGORIES";
const GET_CATEGORY_DETAILS = "categories/GET_CATEGORY_DETAILS";

// ---------- ACTION CREATORS ----------
const getCategories = (categoriesArray) => ({
  type: GET_CATEGORIES,
  payload: categoriesArray,
});

const getCategory = (categoryData) => ({
  type: GET_CATEGORY_DETAILS ,
  payload: categoryData,
});

// ---------- THUNKS ----------
// Get all categories
export const thunkCategories = () => async (dispatch) => {
  const res = await csrfFetch("/api/categories/");
  if (res.ok) {
    const data = await res.json();
    console.log("Fetched categories:", data.categories);

    dispatch(getCategories(data.categories));
  } else {
    console.error("Error loading categories");
  }
};

// Get a specific category and its places
export const thunkCategory = (categoryId) => async (dispatch) => {
  const res = await csrfFetch(`/api/categories/${categoryId}`);
  if (res.ok) {
    const data = await res.json();
    dispatch(getCategory(data));
  } else {
    console.error("Error loading categories");
  }
};

// ---------- REDUCER ----------
const initialState = { allCategories: [], currentCategory: null };

export default function categoriesReducer(state = initialState, action) {
  switch (action.type) {
    case GET_CATEGORIES:
      return { ...state, allCategories: action.payload };
    case GET_CATEGORY_DETAILS:
      return { ...state, currentCategory: action.payload };
    default:
      return state;
  }
}
