import { useEffect, useState } from "react";
import { Outlet } from "react-router-dom";
import { useDispatch } from "react-redux";
import { ModalProvider, Modal } from "../context/Modal";
import { thunkAuthenticate } from "../redux/session";
import Navigation from "../components/Navigation/Navigation";
import { useLocation } from "react-router-dom";


export default function Layout() {
  const dispatch = useDispatch();
  const [isLoaded, setIsLoaded] = useState(false);
  const location = useLocation(); // Получаем текущий путь

  useEffect(() => {
    dispatch(thunkAuthenticate()).then(() => setIsLoaded(true));
  }, [dispatch]);

  const isHomePage = location.pathname === "/";

  return (
    <>
      <ModalProvider>
        <Navigation />
        <div className={`page-content ${isHomePage ? "home-page" : ""}`}>
        {isLoaded && <Outlet />}
        </div>
        <Modal />
      </ModalProvider>
    </>
  );
}
