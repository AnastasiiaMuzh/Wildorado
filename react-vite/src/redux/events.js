import { csrfFetch } from "./csrf";

// ---------- ACTION TYPES ----------
const GET_ALL_EVENTS = 'events/GET_ALL_EVENTS';
const GET_EVENT_DETAIL = 'events/GET_EVENT_DETAIL';
const GET_CURRENT_USER_EVENTS = 'events/GET_CURRENT_USER_EVENTS';
const CREATE_EVENT = 'events/CREATE_EVENT';
const UPDATE_EVENT = 'events/UPDATE_EVENT';
const DELETE_EVENT = 'events/DELETE_EVENT';
const JOIN_EVENT = 'events/JOIN_EVENT';
const LEAVE_EVENT = 'events/LEAVE_EVENT';
const CREATE_COMMENT = 'events/CREATE_COMMENT';
const DELETE_COMMENT = 'events/DELETE_COMMENT';

// --- ACTION CREATORS ---
const getAllEvents = (events) => ({
    type: GET_ALL_EVENTS,
    payload: events,
  });
  
const getEventDetail = (event) => ({
type: GET_EVENT_DETAIL,
payload: event,
});

const getCurrentUserEvents = (events) => ({
type: GET_CURRENT_USER_EVENTS,
payload: events,
});

const createEvent = (event) => ({
type: CREATE_EVENT,
payload: event,
});

const updateEvent = (event) => ({
type: UPDATE_EVENT,
payload: event,
});

const deleteEvent = (eventId) => ({
type: DELETE_EVENT,
payload: eventId,
});

const joinEvent = (eventId) => ({
type: JOIN_EVENT,
payload: eventId,
});

const leaveEvent = (eventId) => ({
type: LEAVE_EVENT,
payload: eventId,
});

const createComment = (comment) => ({
type: CREATE_COMMENT,
payload: comment,
})

const deleteComment = (commentId) => ({
    type: DELETE_COMMENT,
    payload: commentId,
  });

// --- THUNKS ---
  
// Get all events
export const thunkGetAllEvents = () => async (dispatch) => {
    const res = await fetch('/api/events/');
    if (res.ok) {
        const data = await res.json();
        dispatch(getAllEvents(data.events));
        return data.events;
    }
};

// Discussion (message)
export const thunkGetEventDetail = (eventId) => async (dispatch) => {
    const res = await fetch(`/api/events/${eventId}`);
    if (res.ok) {
        const data = await res.json();
        dispatch(getEventDetail(data.event));
        return data.event;
    }
};

// Get MY events
export const thunkGetCurrentUserEvents = () => async (dispatch) => {
    const res = await csrfFetch('/api/events/current');
    if (res.ok) {
        const data = await res.json();
        dispatch(getCurrentUserEvents(data.events || []));
        return data.events;
    }
};

// Create event
export const thunkCreateEvent = (payload) => async (dispatch) => {
    try{
        const res = await csrfFetch('/api/events/new', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload),
        });
        const data = await res.json();
        if (!res.ok) {
            const error = new Error(data.message || 'Failed to create event');
            error.res = { data };
            throw error;
        }
        dispatch(createEvent(data));
        return data;
    } catch (error) {
        throw error;
    }
};

// Update event
export const thunkUpdateEvent = (eventId, payload) => async (dispatch) => {
    const res = await csrfFetch(`/api/events/${eventId}`, {
        method: 'PUT',
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
    });

    if (!res.ok) {
        const data = await res.json();
        throw new Error(data.message || 'Failed to update event');
    }
    const data = await res.json();
    dispatch(updateEvent(data));
    return data;
};

// Delete event
export const thunkDeleteEvent = (eventId) => async (dispatch) => {
    const res = await csrfFetch(`/api/events/${eventId}`, {
        method: 'DELETE',
    });

    if (!res.ok) {
        const data = await res.json();
        throw new Error(data.message || 'Failed to delete event');
    }

    dispatch(deleteEvent(eventId));
};

//Join event
export const thunkJoinEvent = (eventId) => async (dispatch) => {
    const res = await csrfFetch(`/api/events/${eventId}/join`, {
        method: 'POST',
    });

    if (!res.ok) {
        const data = await res.json();
        throw new Error(data.message || 'Failed to join event');
        }

    dispatch(joinEvent(eventId));
    return res.json();
};

// Leave event
export const thunkLeaveEvent = (eventId) => async (dispatch) => {
    const res = await csrfFetch(`/api/events/${eventId}/leave`, {
    method: 'DELETE',
    });

    if (!res.ok) {
        const data = await res.json();
        throw new Error(data.message || 'Failed to leave event');
    }

    dispatch(leaveEvent(eventId));
    return res.json();
};

//Create massage
export const thunkCreateComment = (eventId, message) => async (dispatch) => {
    const res = await csrfFetch(`/api/events/${eventId}/comments`, {
        method: 'POST',
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message }),
    });
    if (!res.ok) {
        const errorData = await res.json();
        throw new Error(errorData.message || 'Failed to create comment');
    }
    const data = await res.json();
    dispatch(createComment(data));
    return data;
};

//Delete message
export const thunkDeleteComment = (eventId, commentId) => async (dispatch) => {
    const res = await csrfFetch(`/api/events/${eventId}/comments/${commentId}`,{
        method: 'DELETE', 
    });
    if (!res.ok) {
        const errData = await res.json();
    }
    const data = await res.json()
    dispatch(deleteComment(commentId))
    return data;
}
  
  
// --- INITIAL STATE ---
const initialState = {allEvents: [],currentUserEvents: [], eventDetail: null,};

// --- REDUCER ---
const eventsReducer = (state = initialState, action) => {
    switch (action.type) {
        case GET_ALL_EVENTS:
            return { ...state, allEvents: action.payload };

        case GET_EVENT_DETAIL:
            return { ...state, eventDetail: action.payload };

    // case GET_CURRENT_USER_EVENTS:
    //     return { ...state, currentUserEvents: action.payload };

        case GET_CURRENT_USER_EVENTS:
            return { ...state, currentUserEvents: action.payload };

        case CREATE_EVENT:
            return { ...state, allEvents: [...state.allEvents, action.payload], currentUserEvents: [...state.currentUserEvents, action.payload] };

        case UPDATE_EVENT:
            return {
            ...state,
            allEvents: state.allEvents.map((event) => (event.id === action.payload.id ? action.payload : event)),
            currentUserEvents: state.currentUserEvents.map((event) => (event.id === action.payload.id ? action.payload : event)),
            eventDetail: state.eventDetail?.id === action.payload.id ? action.payload : state.eventDetail,
            };

        case DELETE_EVENT:
            return {
            ...state,
            allEvents: state.allEvents.filter((event) => event.id !== action.payload),
            currentUserEvents: state.currentUserEvents.filter((event) => event.id !== action.payload),
            eventDetail: state.eventDetail?.id === action.payload ? null : state.eventDetail,
            };

        case JOIN_EVENT:
            if (state.eventDetail && state.eventDetail.id === action.payload) {
            return {
                ...state,
                eventDetail: {
                ...state.eventDetail,
                participants: [...(state.eventDetail.participants || []), { id: 'currentUser', username: 'You' }], // Позже замени на реальный userId и username
                },
            };
            }
            return state;

        case LEAVE_EVENT:
            if (state.eventDetail && state.eventDetail.id === action.payload) {
            return {
                ...state,
                eventDetail: {
                ...state.eventDetail,
                participants: state.eventDetail.participants.filter((p) => p.id !== 'currentUser'), // Позже замени на реальный userId
                },
            };
            }

        case CREATE_COMMENT: {
            const newComment = action.payload; // { id, eventId, userId, message, createdAt, ... }
            // Если у нас загружен eventDetail, и его id совпадает с newComment.eventId
            if (state.eventDetail && state.eventDetail.id === newComment.eventId) {
                return {
                    ...state,
                    eventDetail: {
                        ...state.eventDetail,
                        comments: [...(state.eventDetail.comments || []), newComment],
                    },
                };
            }
            return state;
        }

        case DELETE_COMMENT: {
            if (state.eventDetail && state.eventDetail.comments) {
              return {
                ...state,
                eventDetail: {
                  ...state.eventDetail,
                  comments: state.eventDetail.comments.filter(
                    (comment) => comment.id !== action.payload
                  ),
                },
              };
            }
            return state;
          }
        
        

    default:
        return state;

    }
};

export default eventsReducer;