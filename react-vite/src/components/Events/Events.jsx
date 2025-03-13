import { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { useNavigate, NavLink } from "react-router-dom";
import { thunkGetAllEvents } from "../../redux/events";
import { thunkGetAllLocations } from "../../redux/locations";
import { FaUserFriends, FaRegCalendarAlt, FaMapMarkerAlt } from "react-icons/fa";

const EventsPage = () => {
    const dispatch = useDispatch();
    const navigate = useNavigate();
    
    const events = useSelector((state) => state.events.allEvents);
    const locations = useSelector((state) => state.locations.allLocations);
    
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        setLoading(true);
        Promise.all([
            dispatch(thunkGetAllEvents()),
            dispatch(thunkGetAllLocations("?page=1&perPage=100")),
        ])
        .catch((error) => setError(error.message))
        .finally(() => setLoading(false));
    }, [dispatch]);

    if (loading) return <div>Loading events...</div>;
    if (error) return <div>Error: {error}</div>;

    // events.forEach(event => {
    //     const locationForEvent = locations.find(loc => loc.id === event.locationId);
    //     console.log(`Location for event (${event.title}):`, locationForEvent);
    // });

    return (
      <div className="events-page">
        <h1>Active Events – Join Now!</h1>

        <div className="event-loc-list">
        {events.map(event => {
          const locationForEvent = locations.find(loc => loc.id === event.locationId);
          const previewImage = locationForEvent?.imageUrl;

          return (
            <div key={event.id} className="event-item">
              <h2>{event.title}</h2>
              
              <p>
                <FaRegCalendarAlt />{" "}
                {new Date(event.date).toLocaleString('en-US', {
                  weekday: 'short', 
                  year: 'numeric', 
                  month: 'short', 
                  day: 'numeric', 
              })}
            </p>
            <div className="event-page-info">
            <p><FaUserFriends /> {event.participantCount}/{event.maxParticipants} participants</p>
            {locationForEvent && (
                <>
                <p><FaMapMarkerAlt /> {locationForEvent.name}, {locationForEvent.city}</p> 
                <p><NavLink to={`/locations/${locationForEvent.id}`}>Details Location</NavLink></p>
               </>
            )}
            </div>

            {previewImage && (
              <img
                src={previewImage}
                alt={locationForEvent.name}
                style={{
                  width: '50%',
                  height: '400px',
                  objectFit: 'cover',
                  borderRadius: '10px',
                  marginTop: '10px'
                }}
              />
            )}
            <div className="event-page-links">
            <p><NavLink to={'/<int:event_id>/comments'}>Discussion</NavLink></p>
            <p><NavLink to={`/events/${event.id}`}>Details Event</NavLink></p>
            </div>
          </div>
        )})}

        </div>
      </div>
    );
}

export default EventsPage;
