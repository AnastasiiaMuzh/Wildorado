import {
  legacy_createStore as createStore,
  applyMiddleware,
  compose,
  combineReducers,
} from "redux";
import thunk from "redux-thunk";
import sessionReducer from "./session";
import categoriesReducer from "./categories";
import locationsReducer from "./locations";
import eventsReducer from "./events";
import reviewsReducer from "./reviews";


const rootReducer = combineReducers({
  session: sessionReducer,
  categories: categoriesReducer,
  locations: locationsReducer,
  events: eventsReducer,
  reviews: reviewsReducer,
  
});

let enhancer;
if (import.meta.env.MODE === "production") {
  enhancer = applyMiddleware(thunk);
} else {
  const logger = (await import("redux-logger")).default;
  const composeEnhancers =
    window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__ || compose;
  enhancer = composeEnhancers(applyMiddleware(thunk, logger));
}

const configureStore = (preloadedState) => {
  return createStore(rootReducer, preloadedState, enhancer);
};

export default configureStore;
