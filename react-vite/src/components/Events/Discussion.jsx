import { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { useParams } from 'react-router-dom';
import moment from 'moment';
import { FaTrash, FaRegEdit } from "react-icons/fa";
import { FaUserFriends, FaRegCalendarAlt} from "react-icons/fa";
import { thunkGetEventDetail, thunkCreateComment, thunkDeleteComment, thunkUpdateComment } from '../../redux/events';
import "./Discussion.css"

const DiscussionPage = () => {
    const dispatch = useDispatch();
    const { eventId } = useParams();
    const [commentText, setCommentText] = useState("");
    const [editingCommentId, setEditingCommentId] = useState(null);
    const [editedMessage, setEditedMessage] = useState("");
    const event = useSelector((state) => state.events.eventDetail);
    const currentUser = useSelector((state) => state.session.user);


    useEffect(() => {
        if (eventId) {
        dispatch(thunkGetEventDetail(eventId));
        }
    }, [dispatch, eventId]);


    const startEditing = (comment) => {
         console.log("CLICKED EDIT:", comment);
        setEditingCommentId(comment.id);
        setEditedMessage(comment.message);
      };  
      
      
    const handleCommentSubmit = async (e) => {
            e.preventDefault();
            if (!commentText.trim()) return;
            try {
            await dispatch(thunkCreateComment(event.id, commentText));
            await dispatch(thunkGetEventDetail(event.id))
            setCommentText("");
            } catch (error) {
            console.err(error.message);
            }
        };
        
    const handleDelete = async (commentId) => {
        try {
          await dispatch(thunkDeleteComment(eventId, commentId));
        }catch (error) {
          console.err(error.message);
        }
    }

    const handleUpdate = async () => {
        try {
          await dispatch(thunkUpdateComment(eventId, editingCommentId, editedMessage));
          setEditingCommentId(null);
          setEditedMessage("");
          await dispatch(thunkGetEventDetail(eventId)); // обновим комментарии
        } catch (err) {
          console.error(err.message);
        }
      };
      

    moment.updateLocale("en", {
      relativeTime: {
        future: "%s", 
        past: (input) => input === "Yesterday" ? input : `${input} ago`,
        s: "few seconds",
        ss: "%d seconds",
        m: "minute",
        mm: "%d minutes",
        h: "hour",
        hh: "%d hours",
        d: "Yesterday",
        dd: "%d days",
        M: "month",
        MM: "%d months",
        y: "a year",
        yy: "%d years"
      }
    });

    if (!event) return <div>Loading event details...</div>;

    return (
        <div className="event-detail-container">
            <header className="event-header">
                <h1>{event.title}</h1>
                <h3 className="event-participants"> <FaUserFriends /> Participants: {event.participants?.length}/{event.maxParticipants}</h3>
                <p className="event-date"><FaRegCalendarAlt /> {moment(event.date).format("ddd, MMM D, YYYY")}</p>
                {event.creator && (
                    <div className="event-creator">
                        {event.creator.avatar && (
                            <img 
                                src={event.creator.avatar} 
                                alt={event.creator.username} 
                                className="creator-avatar"
                            />
                        )}
                        <p>Created by: <strong>{event.creator.username}</strong></p>
                    </div>
                )}

                {event.location?.previewImage && (
                    <img 
                        src={event.location.previewImage} 
                        alt={event.location.name} 
                        className="event-preview-image" 
                    />
                )}
                <h2 className="event-description">{event.description}</h2>
            </header>

            <hr />

            <div className="message-container">
                <h2>Discussion</h2>

                {event.comments && event.comments.length > 0 ? (
                    <ul className="message-list">
                        {event.comments.map((comment) => (
                            <div key={comment.id} className="message-item">
                                <div className="message-header">
                                    {comment.avatar ? (
                                        <img 
                                            src={comment.avatar} 
                                            alt="User avatar" 
                                            className="message-avatar" 
                                        />
                                    ) : (
                                        <div className="message-avatar-placeholder">
                                        {comment.username}
                                      </div>
                                    )}
                                </div>
                                                                                        
                                <div className="message-content">
                                    
                                    {editingCommentId === comment.id ? (
                                        
                                        <div className="edit-form">
                                            <input
                                            value={editedMessage}
                                            onChange={(e) => setEditedMessage(e.target.value)}
                                            className="edit-input"
                                            />
                                            <div className='save-cancel-control'>
                                                <button onClick={() => setEditingCommentId(null)} className="cancel-btn">Cancel</button>
                                                <button onClick={handleUpdate} className="save-btn">Save</button>
                                            </div>
                                        </div>
                                    ) : (
                                        <p className="message">{comment.message}</p>

                                    )}
                                    <span className="message-date">
                                    {moment(comment.createdAt).local().fromNow()}
                                    </span>

                                    {comment.userId === currentUser?.id && (
                                        <div className="comment-controls">
                                            <button className="comment-edit-btn" onClick={() => startEditing(comment)} title="Edit your message">
                                                <FaRegEdit />
                                            </button>
                                            <button className="message-delete-btn" onClick={() => handleDelete(comment.id)}>
                                                <FaTrash />
                                            </button>
                                        </div>
                                    )}                               
                            </div>
                        </div>
                    ))}
                    </ul>                   
                ) : (
                    <p className="no-messages">No messages yet. Be the first to leave a message!</p>
                )}
                </div>

                <form onSubmit={handleCommentSubmit} className="message-form">
                    <input
                        value={commentText}
                        onChange={(e) => setCommentText(e.target.value)}
                        placeholder="Write your message..."
                        className="message-input"
                    />
                    <button type="submit" className="message-send-btn">
                        Send
                    </button>
                </form>
            </div>
    );
};

export default DiscussionPage;