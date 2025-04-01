import { useState, useEffect } from 'react';
import { FaEdit, FaTrash } from "react-icons/fa";
import { Link, useNavigate } from "react-router-dom";
import { csrfFetch } from '../../redux/csrf';
import OpenModalButton from '../OpenModalButton/OpenModalButton';
import DeleteLocationModal from './DeleteLocationModal';
import "./ManageLocations.css"
import { useModal } from "../../context/Modal";
import UpdateLocationFormModal from '../LocationForm/UpdateLocationForm';

const ManageLocations = () => {
  const [locations, setLocations] = useState([]); 
  const [isLoading, setIsLoading] = useState(true); 
  const [error, setError] = useState(null); 
  const { closeModal } = useModal();
  const navigate = useNavigate();

  const handleEdit = (locationId) => {
    navigate(`/locations/${locationId}/edit`);
  };

  const handleLocClick = (locationId) => {
    navigate(`/locations/${locationId}`);
  };

  //loading current user locations
  const fetchUserLocations = async () => {
    try {
      const response = await csrfFetch('/api/locations/current');
      if (!response.ok) {
        throw new Error('Failed to fetch locations');
      }
      const data = await response.json();
      // console.error("LOOK USER LOCATION->", data)
      setLocations(data.Locations || []); // Обновляем состояние с локациями (// Сохраняем только локации текущего пользователя)
    } catch (err) {
      setError(err.message); // ошибкa, если что-то пошло не так
    } finally {
      setIsLoading(false); // Завершаем загрузку
    }
  };

  // Загружаем локации при монтировании компонента
  useEffect(() => {
    fetchUserLocations();
  }, []);


  if (isLoading) return <p>Loading...</p>;
  if (error) return <p>Error: {error}</p>;


  return (
    <div className="manage-loc-container">
      <h2>My Locations</h2>
      
      {locations.length > 0 ? (
        <div className="manage-loc-grid">
          {locations.map((location) => (
            <div key={location.id} className="location-card">
              <div className="location-card-image" onClick={() => handleLocClick(location.id)}>
                <img src={location.imageUrl} alt={location.name} />
              </div>
            
              <div className="location-card-content">
                <div className="my-location-header">
                  <h3>{location.name}</h3>
                  <p className="location-city">
                    <span className="location-pin">📍</span> {location.city}
                  </p>
                </div>
                
                <div className="location-footer">
                  <div className="location-rating">
                    {[1, 2, 3, 4, 5].map((star) => {
                      const hasRating = location.avgRating > 0 && location.reviewCount > 0;
                      const rating = location.avgRating;

                      if (!hasRating) {
                        return (
                          <span key={star} className="star empty">
                            ★
                          </span>
                        );
                      }

                      const isFilled = star <= Math.floor(rating);
                      const isHalf = star === Math.ceil(rating) && (rating % 1 >= 0.3);

                      let starClass = "star";
                      if (isFilled) {
                        starClass += " filled";
                      } else if (isHalf) {
                        starClass += " half";
                      } else {
                        // "empty" star that comes after the filled ones
                        // with "the existing" rating-> unfilled (not to be confused with .empty)
                        starClass += " unfilled";
                      }

                      return (
                        <span key={star} className={starClass}>
                          ★
                        </span>
                      );
                    })}

                    <span className="rating-text">
                      {location.avgRating > 0 && location.reviewCount > 0 
                        ? `${location.avgRating.toFixed(1)} (${location.reviewCount} reviews)` 
                        : 'No reviews yet'}
                    </span>
                  </div>
                  
                  <div className="location-card-actions">
                  <OpenModalButton
                    buttonText={<FaEdit className="icon" />}
                    modalComponent={
                      <UpdateLocationFormModal 
                        locationId={location.id} 
                        onUpdate={fetchUserLocations}
                      />
                    }
                    onButtonClick={(e) => {
                      if (e?.stopPropagation) e.stopPropagation();
                      if (e?.preventDefault) e.preventDefault();
                    }}
                  />

                    <OpenModalButton
                      buttonText={<FaTrash className="icon-trash" />}
                      modalComponent={
                        <DeleteLocationModal 
                          locationId={location.id} 
                          onDelete={fetchUserLocations}
                        />
                      }
                      onButtonClick={(e) => {
                        e.stopPropagation();
                        e.preventDefault();
                      }}
                    />
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="empty-locations">
          <p>You currently have no created locations.</p>
          <Link to="/locations/new" className="create-location-link">Create a new location</Link>
        </div>
      )}
    </div>
  );
}
export default ManageLocations;