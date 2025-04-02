import { useEffect} from "react";
import { useDispatch, useSelector } from "react-redux";
import { useNavigate } from "react-router-dom";
import { thunkGetCurrentUserEvents} from "../../redux/events";
import { FaEdit, FaTrash, FaComments } from "react-icons/fa";
import OpenModalButton from '../OpenModalButton/OpenModalButton';
import DeleteEventModal from "./DeleteEventModal";
import UpdateEventFormModal from "../EventForm/UpdateEventForm";
import "./ManageEvent.css";



const ManageEvents = () => {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const userEvents = useSelector((state) => state.events.currentUserEvents);
  const goToAllEvents = () => navigate("/events");
 

  useEffect(() => {
    dispatch(thunkGetCurrentUserEvents());
  }, [dispatch]);


  // const handleEdit = (eventId) => navigate(`/events/${eventId}/edit`);
  const handleDiscussion = (eventId) => navigate(`/events/${eventId}`);


  return (
    <section className="manage-events-main">
      <h1 className="manage-your-event">Manage Your Events</h1>

      {userEvents.length > 0 ? (
        <ul className="event-list">
          {userEvents.map((event) => (
            <article key={event.id} className="event-card-manage">
              <h3 className="event-title-manage">
                <span className="event-title-link" onClick={goToAllEvents}>
                  {event.title}
                </span>
              </h3>
              <div className="event-meta-manage">
                <p >📍 {event.location?.name}, {event.location?.city}</p>
                <p>🗓 {new Date(event.date).toLocaleDateString()}</p>
                <p>👥 {event.maxParticipants || 0} Participants</p>
              </div>
              {/* Изображение локации */}
              <img 
                src={event.location?.previewImage || "https://via.placeholder.com/300"} 
                alt={event.location?.name || "No Image"} 
                className="event-img-manage"
              />
              <p className="event-description-manage">📝 {event.description || "No description available"}</p> 

              <div className="event-btn-manage">
              <OpenModalButton
                buttonText={
                  <span>
                    <FaEdit /> Edit
                  </span>
                }
                modalComponent={<UpdateEventFormModal eventId={event.id} />}
                className="edit-btn-manage"
                />

                <OpenModalButton
                  buttonText={
                    <span>
                      <FaTrash /> Delete
                    </span>
                  }
                  modalComponent={<DeleteEventModal eventId={event.id} />}
                  className="delete-btn-manage"
                />
                <button className="discussion-btn-manage" onClick={() => handleDiscussion(event.id)}>
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
