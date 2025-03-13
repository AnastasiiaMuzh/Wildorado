import { createBrowserRouter } from 'react-router-dom';
import LoginFormPage from '../components/LoginFormPage';
import SignupFormPage from '../components/SignupFormPage';
import HomePage from '../components/HomePage/HomePage';
import Category from '../components/Category/Category'
import LocationPage from '../components/Locations/LocationsPage';
import LocationDetailsPage from '../components/Locations/LocationDetailsPage';
// import CreateLocations from '../components/Locations/CreateLocationForm';
import ManageLocations from '../components/ManageLocations/ManageLocations';
// import UpdateLocationForm from '../components/ManageLocations/UpdateLocation';
import CreateLocationForm from '../components/LocationForm/CreateLocationForm';
import UpdateLocationForm from '../components/LocationForm/UpdateLocationForm';
import EventsPage from '../components/Events/Events';

import Layout from './Layout';



export const router = createBrowserRouter([
  {
    element: <Layout />,
    children: [
      {
        path: "/",
        element: < HomePage />,
      },
      {
        path: "/categories/:id",
        element: <Category />
      },
      {
        path: "login",
        element: <LoginFormPage />,
      },
      {
        path: "signup",
        element: <SignupFormPage />,
      },
      {
        path: "/locations",
        element: <LocationPage />,
      },
      {
        path: "/locations/:id",
        element: <LocationDetailsPage />,
      },
      {
        path: "/locations/new",
        element: <CreateLocationForm />,
      },
      {
        path: "/locations/current",
        element: <ManageLocations />,
      },
      {
        path: "/locations/:locationId/edit",
        element: <UpdateLocationForm />,
      },
      {
        path: "/events",
        element: <EventsPage />,
      },
      
      
    ],
  },
]);