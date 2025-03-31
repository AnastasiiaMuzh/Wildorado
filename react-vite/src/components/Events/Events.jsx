import { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { NavLink } from "react-router-dom";
import { thunkGetAllEvents, thunkJoinEvent, thunkLeaveEvent } from "../../redux/events";
import { FaUserFriends, FaRegCalendarAlt, FaMapMarkerAlt, FaSearch, FaSignOutAlt, FaComments  } from "react-icons/fa";
import './Events.css'

const EventsPage = () => {
  const dispatch = useDispatch();
  
  const events = useSelector((state) => state.events.allEvents);
  const currentUser = useSelector((state) => state.session.user); 

  useEffect(() => {
    dispatch(thunkGetAllEvents());
  }, [dispatch]);

  if (!events) return <div>Loading events...</div>;


  const handleJoin = async (eventId) => {
    try {
      await dispatch(thunkJoinEvent(eventId));
      await dispatch(thunkGetAllEvents());
    } catch (error) {
      alert(error.message);
    }
  };

  const handleLeave = async (eventId) => {
    try {
      await dispatch(thunkLeaveEvent(eventId));
      await dispatch(thunkGetAllEvents());
    } catch (error) {
      alert(error.message);
    }
  };

  return (
    <div className="events-page">
      <div className="event-loc-list">
        {events.map((event) => {
          const isFull = event.maxParticipants && event.participantCount >= event.maxParticipants;
          const isJoined = event.isCurrentUserParticipant;
  
          return (
            <div key={event.id} className="event-item">
              <h2 className="event-title">{event.title}</h2>
              {/* Контейнер заголовка и информации */}
              <div className="event-header-info">
                
                <p className="event-date">
                  <FaRegCalendarAlt />{" "}
                  {new Date(event.date).toLocaleString("en-US", {
                    weekday: "short",
                    year: "numeric",
                    month: "short",
                    day: "numeric",
                  })}
                </p>
                <p className="event-participants">
                  <FaUserFriends /> {event.participantCount}/{event.maxParticipants} participants
                </p>
                {event.location && (
                  <div className="event-location-info">
                    <p>
                      <FaMapMarkerAlt /> {event.location.name}, {event.location.city}
                    </p>
                    <p className="event-details-link">
                      <FaSearch />
                      <NavLink to={`/locations/${event.locationId}`} >
                        Details Location
                      </NavLink>
                    </p>
                  </div>
                )}
              </div>
  
              {/* Контейнер изображения */}
              {event.location?.previewImage && (
                <div className="event-image-container">
                  <img src={event.location.previewImage} alt={event.location.name} />
                </div>
              )}
  
              {/* Кнопки управления */}
              <div className="event-page-links">
                {!currentUser ? (
                  <p style={{ color: "red" }}>
                    To participate in events, you must be registered.
                  </p>
                ) : isJoined ? (
                  <>
                    <NavLink
                      to="#"
                      onClick={(e) => {
                        e.preventDefault();
                        handleLeave(event.id);
                      }}
                    >
                      <FaSignOutAlt style={{marginRight: "8px"}} />
                      <span>Leave Event</span>
                    </NavLink>
                    <NavLink to={`/events/${event.id}`} >
                    <FaComments style={{ marginRight: "8px" }} />
                    <span>Discussion</span>
                    </NavLink>
                  </>
                ) : isFull ? (
                  <p style={{ color: "red" }}>Event is full</p>
                ) : (
                  <NavLink
                    to="#"
                    onClick={(e) => {
                      e.preventDefault();
                      handleJoin(event.id);
                    }}
                  >
                    Join this Event
                  </NavLink>
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
  
}  

export default EventsPage;