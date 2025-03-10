import { useEffect, useState, useRef } from "react";
import { NavLink, useNavigate, useLocation } from "react-router-dom";
import { useSelector } from "react-redux";
import ProfileButton from "./ProfileButton";
import Calendar from "react-calendar"; 
import "react-calendar/dist/Calendar.css"; 
import "./Navigation.css"; 
import { csrfFetch } from "../../redux/csrf";

const Navigation = () => {
  
  const navigate = useNavigate();
  const location = useLocation(); 
  const user = useSelector((state) => state.session.user);
  const [searchQuery, setSearchQuery] = useState("");
  const [showCalendar, setShowCalendar] = useState(false); 
  const [currentDate, setCurrentDate] = useState("");
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  const calendarRef = useRef(null);
  const profileRef = useRef(null);

  const isHomePage = location.pathname === "/";

  // Закрытие попапов при клике вне их области
  useEffect(() => {
    function handleClickOutside(event) {
      if (calendarRef.current && !calendarRef.current.contains(event.target)) {
        setShowCalendar(false);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, []);


  useEffect(() => {
    const today = new Date().toLocaleDateString("en-US", {
      weekday: "short",
      day: "2-digit",
      month: "short",
    });
    setCurrentDate(today);
  }, []);


  const toggleMobileMenu = () => {
    setIsMobileMenuOpen(!isMobileMenuOpen);
  };
  

  const handleSearch = async (e) => {
    e.preventDefault();
    const query = searchQuery.trim();
    if (!query) return;
    try {
        const res = await csrfFetch(`/api/locations?search=${query}&page=1&perPage=12`);
        if (res.ok) {
          // Если запрос успешный, перенаправляем на страницу поиска
          navigate(`/locations?search=${query}`);
        } else {
            // Если сервер вернул 404 
          alert("No results found. Please try again!");
        }
    } catch (error) {
      console.error("Error searching locations:", error);
      alert("Something went wrong. Please try again.");
    }
    setSearchQuery(""); // Очищаем строку поиска после запроса
  };

  return (
    <nav className={`navbar ${isHomePage ? "transparent-navbar" : "solid-navbar"}`}>
      <div className="navbar-container">
        <NavLink to="/" className="logo">
          <img 
            src="/images/logo.png" 
            alt="Wildorado Logo" 
            className={`logo-img ${isHomePage ? 'logo-home' : 'logo-other'}`} 
          />
        </NavLink>

        <form onSubmit={handleSearch} className="search-form">
          <button type="submit" className="search-button">🔍</button>
          <input
            type="text"
            placeholder="Search category, city, mountains ..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="search-input"
          />
        </form>

        <button 
          className="mobile-menu-toggle" 
          onClick={toggleMobileMenu}
        >
          {isMobileMenuOpen ? '✕' : '☰'}
        </button>

        <div className={`nav-links ${isMobileMenuOpen ? 'mobile-open' : ''}`}>
          <NavLink to="/locations" className='nav-link'>LOCATION</NavLink>
          <NavLink to="/events" className='nav-link'>EVENT</NavLink>
          <NavLink to="/community" className='nav-link'>COMMUNITY</NavLink>
          <NavLink to="/contact" className='nav-link'>CONTACT</NavLink>
          {user && (
          <NavLink to="/locations/new" className='nav-link'>POST</NavLink>
          )}

          <div className="dropdown-container" ref={calendarRef}>
            <button 
              onClick={() => setShowCalendar(!showCalendar)} 
              className="calendar-button"
            >
              {currentDate}
            </button>
            
            {showCalendar && (
              <div className="calendar-popup-container">
                <Calendar className="calendar-popup" />
              </div>
            )}
          </div>

          <div className="profile-container" ref={profileRef}>
            <ProfileButton />
          </div>
        </div>
      </div>
    </nav>
  );
}

export default Navigation;