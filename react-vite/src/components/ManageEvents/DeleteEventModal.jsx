import { useModal } from '../../context/Modal';
import { useDispatch } from 'react-redux';
import { thunkDeleteEvent, thunkGetCurrentUserEvents } from '../../redux/events';

const DeleteEventModal = ({ eventId }) => {
    const { closeModal } = useModal();
    const dispatch = useDispatch();

    const handleDelete = async () => {
        await dispatch(thunkDeleteEvent(eventId));
        await dispatch(thunkGetCurrentUserEvents()); // ✅ Обновляем список
        closeModal();
    };

    return (
        <div className='delete-event-modal'>
            <h1 className='modal-header'>Confirm Delete</h1>
            <p>Are you sure you want to delete this event?</p>
            <div className='modal-actions'>
                <button onClick={handleDelete} className='delete-btn'>Yes (Delete Event)</button>
                <button onClick={closeModal} className='cancel-btn'>No (Keep Event)</button>
            </div>
        </div>
    );
};

export default DeleteEventModal;
