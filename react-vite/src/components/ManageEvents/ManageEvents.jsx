import { useEffect} from "react";
import { useDispatch, useSelector } from "react-redux";
import { useNavigate } from "react-router-dom";
import { thunkGetCurrentUserEvents} from "../../redux/events";
import { FaEdit, FaTrash, FaComments } from "react-icons/fa";
import OpenModalButton from '../OpenModalButton/OpenModalButton';
import DeleteEventModal from "./DeleteEventModal";
import "./ManageEvent.css";


const ManageEvents = () => {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const userEvents = useSelector((state) => state.events.currentUserEvents);
 

  useEffect(() => {
    dispatch(thunkGetCurrentUserEvents());
  }, [dispatch]);


  const handleEdit = (eventId) => navigate(`/events/${eventId}/edit`);
  const handleDiscussion = (eventId) => navigate(`/events/${eventId}`);


  return (
    <section className="manage-events">
      <h2>Manage Your Events</h2>

      {userEvents.length > 0 ? (
        <ul className="event-list">
          {userEvents.map((event) => (
            <article key={event.id} className="event-card">
              {/* Изображение локации */}
              <img 
                src={event.location?.previewImage || "https://via.placeholder.com/300"} 
                alt={event.location?.name || "No Image"} 
                className="event-image"
              />

              <div className="event-info">
                <h3>{event.title}</h3>
                <p>📍 {event.location?.name}, {event.location?.city}</p>
                <p>🗓 {new Date(event.date).toLocaleDateString()}</p>
                <p>📝 {event.description || "No description available"}</p> 
                <p>👥 {event.maxParticipants || 0} Participants</p>
              </div>

              <div className="event-actions">
                <button className="edit-btn" onClick={() => handleEdit(event.id)}>
                  <FaEdit /> Edit
                </button>
                <OpenModalButton
                  buttonText={
                    <span>
                      <FaTrash /> Delete
                    </span>
                  }
                  modalComponent={<DeleteEventModal eventId={event.id} />}
                  className="delete-btn"
                />
                <button className="discussion-btn" onClick={() => handleDiscussion(event.id)}>
                  <FaComments /> Discussion
                </button>
              </div>
            </article>
          ))}
        </ul>
      ) : (
        <p>You haven&apos;t created any events yet. <br />
          <a href="/events/new" className="create-event-link">Create a new event</a>
        </p>
      )}
    </section>
  );
};

export default ManageEvents;
