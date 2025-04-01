import { useModal } from '../../context/Modal';
import { useDispatch } from 'react-redux';
import { thunkDeleteLocation } from '../../redux/locations';
import "./DeleteLocationModal.css"

const DeleteLocationModal = ({ locationId, onDelete }) => {
    const { closeModal } = useModal();
    const dispatch = useDispatch();

    const handleDelete = async () =>{
        await dispatch(thunkDeleteLocation(locationId));
        await onDelete();
        closeModal();
    }

    const handleCancel = async () => {
        closeModal();
    }

    return (
        <div className='del-loc-container'>
            <h1 className='del-loc-header'>Confirm Delete</h1>

            <div className="confirm-del-loc">
                <h4>Are you sure want to remove your location?</h4>
            </div>

            <div className='action-btn'>
                <button onClick={handleDelete} className='yes'>Yes (Delete Location)</button>
                <button onClick={handleCancel} className='no'>No (Keep Location)</button>
            </div>


        </div>
    )

}
export default DeleteLocationModal;