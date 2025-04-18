import EventForm from "./EventForm";
import { thunkCreateEvent } from "../../redux/events";
import { useDispatch } from "react-redux";
import { useModal } from "../../context/Modal";
import "./EventFormModal.css";

const CreateEventFormModal = ({ locationId }) => {
    const dispatch = useDispatch();

    const { closeModal } = useModal();

    const handleCreate = async (formData) => {
        try {
            const result = await dispatch(thunkCreateEvent({ ...formData, locationId }));
            if (result) {
                setTimeout(() => {
                    closeModal(); // закрыть модалку через 1.5 секунды
                }, 1500);
            }
            return result;
        } catch (error) {
            console.error("Error creating event:", error);
            throw error;
        }
    };

    return (
        <div className="event-form-container">
        {/* <h1>Create Event</h1> */}
        <EventForm
            initialData={{ title: "", description: "", maxParticipants: "", date: "" }}
            onSubmit={handleCreate}
            submitButtonText="Create Event"
        />
    </div>
    )

}
export default CreateEventFormModal;
