import { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { useNavigate} from "react-router-dom";
import EventForm from "./EventForm";
import { thunkGetEventDetail, thunkUpdateEvent, thunkGetCurrentUserEvents } from "../../redux/events";
import { useModal } from "../../context/Modal";
import "./EventFormModal.css";

// Utility to format existing date/time for <input type="datetime-local" />
const formatDateForInput = (dateString) => {
  if (!dateString) return "";
  const date = new Date(dateString);
  const offsetDate = new Date(date.getTime() - date.getTimezoneOffset() * 60000);
  return offsetDate.toISOString().slice(0, 16);
};

const UpdateEventFormModal = ({ eventId }) => {
  // const { eventId } = useParams();
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const event = useSelector((state) => state.events.eventDetail);
  const { closeModal } = useModal();


  useEffect(() => {
    if (!event || event.id !== +eventId) {
    dispatch(thunkGetEventDetail(eventId));
    }
  }, [dispatch, event, eventId]); //dobavila [event]


  const handleUpdate = async (formData) => {
    const payload = { 
      ...formData, 
      date: new Date(formData.date).toISOString() 
    };
    try {
      await dispatch(thunkUpdateEvent(eventId, payload));
      await dispatch(thunkGetCurrentUserEvents());
      closeModal();
      navigate("/events/current");
    } catch (err) {
      console.error("Update error:", err);
    }
  };
  
  if (!event) return <p>Loading...</p>;

  return (
    <div>
      <h1>Edit Event</h1>
      <EventForm
        initialData={{
          title: event.title,
          description: event.description,
          maxParticipants: event.maxParticipants,
          date: formatDateForInput(event.date),
        }}
        onSubmit={handleUpdate}
        submitButtonText="Update Your Event"
      />
    </div>
  );
};

export default UpdateEventFormModal;

