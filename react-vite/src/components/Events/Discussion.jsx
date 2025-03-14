import { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { useParams } from 'react-router-dom';
import moment from 'moment';
import { FaUserFriends, FaRegCalendarAlt, FaUserAlt } from "react-icons/fa";
import { thunkGetEventDetail, thunkCreateComment, thunkDeleteComment } from '../../redux/events';

const DiscussionPage = ({comment, eventsId}) => {
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

    if (!event) return <div>Loading event details...</div>;

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

    return (
        <div className="event-detail-container">
           
        <header className="event-header">
            <h1>{event.title}</h1>
            <p className="event-date"><FaRegCalendarAlt /> {moment(event.date).format("ddd, MMM D, YYYY")}</p>
            <h2 className="event-description">{event.description}</h2>
            <h3 className="event-participants"> <FaUserFriends /> Participants: {event.participants?.length}/{event.maxParticipants}</h3>
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
                      <FaUserAlt className="message-avatar-default" />
                    )}
                  <strong> {comment.username}</strong>
                  <span className="message-date">
                    {moment(comment.createdAt).format("MMM D, YYYY [at] h:mm A")}
                  </span>
                  {comment.userId === currentUser?.id && (
                    <button
                      onClick={() => handleDelete(comment.id)}
                      className="message-delete-btn"
                    >
                      Delete
                    </button>
                  )}
                </div>
                <p className="message">{comment.message}</p>
              </div>
            ))}
          </ul>
            ) : (
            <p>No messages yet. Be the first live a message!</p>
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
