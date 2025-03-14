import { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { useNavigate, NavLink } from "react-router-dom";
import { thunkGetAllEvents, thunkJoinEvent, thunkLeaveEvent } from "../../redux/events";
import { FaUserFriends, FaRegCalendarAlt, FaMapMarkerAlt } from "react-icons/fa";

const EventsPage = () => {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  
  const events = useSelector((state) => state.events.allEvents);
  const locations = useSelector((state) => state.locations.allLocations);
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
      <h1>Active Events – Join Now!</h1>

      <div className="event-loc-list">
        {events.map((event) => {
          const isFull = event.maxParticipants && event.participantCount >= event.maxParticipants;
          const isJoined = event.isCurrentUserParticipant;
          return (
            <div key={event.id} className="event-item">
              <h2>{event.title}</h2>

              <p>
                <FaRegCalendarAlt />{" "}
                {new Date(event.date).toLocaleString("en-US", {
                  weekday: "short",
                  year: "numeric",
                  month: "short",
                  day: "numeric",
                })}
              </p>

              <div className="event-page-info">
                <p>
                  <FaUserFriends /> {event.participantCount}/{event.maxParticipants} participants
                </p>

                {event.location && (
                  <>
                    <p>
                      <FaMapMarkerAlt /> {event.location.name}, {event.location.city}
                    </p>
                    <p>
                      <NavLink to={`/locations/${event.locationId}`} state={{ from: "events" }}>
                        Details Location
                      </NavLink>
                    </p>
                  </>
                )}
              </div>

              {event.location?.previewImage && (
                <img
                  src={event.location.previewImage}
                  alt={event.location.name}
                  style={{
                    width: "50%",
                    height: "400px",
                    objectFit: "cover",
                    borderRadius: "10px",
                    marginTop: "10px",
                  }}
                />
              )}

              <div className="event-page-links" style={{ marginTop: "1rem" }}>
                {isJoined ? (
                  <>
                    <NavLink
                      to="#"
                      onClick={(e) => {
                        e.preventDefault();
                        handleLeave(event.id);
                      }}
                    >
                      Leave Event
                    </NavLink>

                    <NavLink
                      to={`/events/${event.id}`}
                      style={{ marginLeft: "1rem" }}
                    >
                      Discussion
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
};

export default EventsPage;