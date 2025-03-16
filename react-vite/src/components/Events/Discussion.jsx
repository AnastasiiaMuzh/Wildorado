import { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { useParams } from 'react-router-dom';
import moment from 'moment';
import { FaTrash } from "react-icons/fa";
import { FaUserFriends, FaRegCalendarAlt} from "react-icons/fa";
import { thunkGetEventDetail, thunkCreateComment, thunkDeleteComment } from '../../redux/events';

const DiscussionPage = () => {
    const dispatch = useDispatch();
    const { eventId } = useParams();
    const [commentText, setCommentText] = useState("");
    const event = useSelector((state) => state.events.eventDetail);
    const currentUser = useSelector((state) => state.session.user);


    useEffect(() => {
        if (eventId) {
        dispatch(thunkGetEventDetail(eventId));
        }
    }, [dispatch, eventId]);

    

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
                                    {comment.avatar && (
                                        <img 
                                            src={comment.avatar} 
                                            alt="User avatar" 
                                            className="message-avatar" 
                                        />
                                    )}
                                    <strong>{comment.username}</strong>
                                </div>

                                <div className="message-content">
                                    <p className="message">{comment.message}</p>
                                    <span className="message-date">
                                        {moment(comment.createdAt).local().fromNow()}
                                        {comment.userId === currentUser?.id && (
                                            <button
                                                onClick={() => handleDelete(comment.id)}
                                                className="message-delete-btn"
                                            >
                                                <FaTrash />
                                            </button>
                                        )}
                                    </span>
                                </div>
                            </div>
                        ))}
                    </ul>
                ) : (
                    <p className="no-messages">No messages yet. Be the first to leave a message!</p>
                )}
            </div>

            {/* ✅ Теперь форма для комментариев ВСЕГДА отображается */}
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