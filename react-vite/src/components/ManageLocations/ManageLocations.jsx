import { useState, useEffect } from 'react';
import { FaEdit, FaTrash } from "react-icons/fa";
import { Link } from "react-router-dom";
import { useNavigate } from "react-router-dom";
import { csrfFetch } from '../../redux/csrf';
import OpenModalButton from '../OpenModalButton/OpenModalButton';
import DeleteLocationModal from './DeleteLocationModal';


const ManageLocations = () => {
  const [locations, setLocations] = useState([]); 
  const [isLoading, setIsLoading] = useState(true); 
  const [error, setError] = useState(null); 
  const navigate = useNavigate();

  const handleEdit = (locationId) => {
    navigate(`/locations/${locationId}/edit`);
  };

  const handleDelete = (locationId) => {
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
      console.error("LOOK USER LOCATION->", data)
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
    <div className='manage-loc-container'>
      
      <h2>Manage Your Locations</h2>
      
      {locations.length > 0 ? (
        <div className='manage-loc-info'>
          <ul>
            <div className='manage-log-info'></div>
            {locations.map((location) => (
              <li key={location.id}>
                <img src={location.imageUrl} alt={location.name} /> 
                <h3>{location.name}</h3>
                <p>📍 {location.city}</p>
                <p>★ {location.avgRating} ({location.reviewCount} reviews)</p>

                <div className='manage-loc-btn'>
                  <button className="edit-btn" onClick={() => handleEdit(location.id)}>
                    <FaEdit className="icon" />
                  </button>
                  <OpenModalButton
                    buttonText={<FaTrash className='icon-trash'/>}
                    modalComponent={<DeleteLocationModal locationId={location.id} onDelete={fetchUserLocations}/>}
                  />
                  {/* <button className="delete-btn" onClick={() => handleDelete(location.id)}>
                    <FaTrash className="icon" />
                  </button> */}
                </div>
              </li>
            ))}
          </ul>
          <div className='manage-loc-btn'>


          </div>
      </div>
      
      ) : (
        <p>You currently have no created locations.<br />  
          To create a new location, please <Link to="/locations/new">click here</Link>.</p>
      )}
    </div>
  );
};

export default ManageLocations;

//esli ya zagrujau locacii cherez redux (location), to dannie teryauytsya, po etomy sdelala derectivno na backend!