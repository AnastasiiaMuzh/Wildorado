import { useModal } from '../../context/Modal';
import { useDispatch } from 'react-redux';
import { thunkDeleteEvent, thunkGetCurrentUserEvents } from '../../redux/events';

const DeleteEventModal = ({ eventId }) => {
    const { closeModal } = useModal();
    const dispatch = useDispatch();

    const handleDelete = async () => {
        await dispatch(thunkDeleteEvent(eventId));
        await dispatch(thunkGetCurrentUserEvents()); 
        closeModal();
    };

    return (
        <div className='del-loc-container'>
            <h1 className='del-loc-header'>Confirm Delete</h1>
            <p>Are you sure you want to delete this event?</p>
            <div className='action-btn'>
                <button onClick={handleDelete} className='yes'>Yes (Delete Event)</button>
                <button onClick={closeModal} className='no'>No (Keep Event)</button>
            </div>
        </div>
    );
};

export default DeleteEventModal;
