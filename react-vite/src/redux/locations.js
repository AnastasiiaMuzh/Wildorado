import { csrfFetch } from "./csrf";

// ---------- ACTION TYPES ----------
const GET_ALL_LOCATIONS = "locations/GET_ALL_LOCATIONS";
const GET_LOCATION_DETAILS = "locations/GET_DETAILS_LOCATION";
const CREATE_LOCATION = "locations/CREATE_LOCATION";
const UPDATE_LOCATION = "locations/UPDATE_LOCATION";
const DELETE_LOCATION = "locations/DELETE_LOCATION";

// ---------- ACTION CREATORS ----------
const getLocations = (locationsArray) => ({
  type: GET_ALL_LOCATIONS,
  payload: locationsArray,
});

const getLocationDetails = (locationData) => ({
  type: GET_LOCATION_DETAILS,
  payload: locationData,
});

const createLocation = (locationData) => ({
  type: CREATE_LOCATION,
  payload: locationData,
});

const updateLocation = (locationData) => ({
  type: UPDATE_LOCATION,
  payload: locationData,
});

const deleteLocation = (locationId) => ({
  type: DELETE_LOCATION,
  payload: locationId,
});

// ---------- THUNKS ----------
//Get all locations
export const thunkGetAllLocations = (queryParams="") => async (dispatch) => {
  const res = await csrfFetch(`/api/locations${queryParams}`);
  if (!res.ok) {
    console.error("Error fetching locations")
    return null;
  }
  const data = await res.json();
  dispatch(getLocations(data.Locations || [])); 
    return data;
};

// Get a specific location by ID
export const thunkGetLocationDetails = (locationId) => async (dispatch) => {
  const res = await csrfFetch(`/api/locations/${locationId}`);
  if (!res.ok) {
    console.error("Error fetching location details");
    return null;
  }
  const data = await res.json();
  dispatch(getLocationDetails(data)); 
    return data; // Возвращаем данные для использования в компоненте
};


export const thunkCreateLocation = (locationData) => async (dispatch) => {
  try {
    const res = await csrfFetch('/api/locations/new', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(locationData),
    });
    
    const data = await res.json();
    if (!res.ok) {
      // This properly throws an error with the response data
      const error = new Error(data.message || 'Failed to create location');
      error.res = { data };
      throw error;
    }
    
    dispatch(createLocation(data));
    return data;
  } catch (error) {
    // Make sure to rethrow the error so the component can catch it
    throw error;
  }
};


//Update an existing location
export const thunkUpdateLocation = (locationId, locationData) => async (dispatch) => {
  const res = await csrfFetch(`/api/locations/${locationId}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(locationData),
  });
  if (!res.ok) {
    console.error("Error updating location")
    return null;
  }
  const data = await res.json();
  dispatch(updateLocation(data));
    return data;
};


// Delete a location
export const thunkDeleteLocation = (locationId) => async (dispatch) => {
  const res = await csrfFetch(`/api/locations/${locationId}`, {
    method: "DELETE",
  });
  if (!res.ok) {
    console.error("Error deleting location")
    return null;
  }
    dispatch(deleteLocation(locationId));
};

// ---------- REDUCER ----------
//Если пользователь переходит на другую страницу или закрывает детали локации, можем сбросить locationDetail в null, чтобы освободить память и избежать ошибок.
const initialState = { allLocations: [], locationDetail: null };

const locationsReducer = (state = initialState, action) => {
  switch (action.type) {
    case GET_ALL_LOCATIONS:
      return { ...state, allLocations: action.payload }; 
    case GET_LOCATION_DETAILS:
      return { ...state, locationDetail: action.payload };
    case CREATE_LOCATION:
      return { ...state, allLocations: [...state.allLocations, action.payload] };
    case UPDATE_LOCATION:
      return {
        ...state,
        allLocations: state.allLocations.map((loc) =>loc.id === action.payload.id ? action.payload : loc),
        locationDetail:
          state.locationDetail?.id === action.payload.id ? action.payload : state.locationDetail,
      };
    case DELETE_LOCATION:
      return {
        ...state,
        allLocations: state.allLocations.filter((loc) => loc.id !== action.payload),
        locationDetail:
          state.locationDetail?.id === action.payload ? null : state.locationDetail,
      };
    default:
      return state;
  }
}

export default locationsReducer;