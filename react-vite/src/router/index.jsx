import { createBrowserRouter } from 'react-router-dom';
import LoginFormPage from '../components/LoginFormPage';
import SignupFormPage from '../components/SignupFormPage';
import HomePage from '../components/HomePage/HomePage';
import Category from '../components/Category/Category'
import LocationPage from '../components/Locations/LocationsPage';
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
    ],
  },
]);