import EventForm from "./EventForm";
import { thunkCreateEvent } from "../../redux/events";
import { useDispatch } from "react-redux";
import { useSearchParams } from "react-router-dom";
import { useModal } from "../../context/Modal";

const CreateEventFormModal = () => {
    const [searchParams] = useSearchParams(); 
    const dispatch = useDispatch();
    const locationId = searchParams.get("locationId"); 
    const { closeModal } = useModal();

    const handleCreate = async (formData) => {
        try {
            const result = await dispatch(thunkCreateEvent({ ...formData, locationId }));
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
