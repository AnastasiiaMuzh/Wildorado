'use client';
import { useState } from "react";

export default function NotificationsPage() {
    const [activeFilter, setActiveFilter] = useState("ALL");
    const [darkMode, setDarkMode] = useState(false); // Toggle for dark mode
    
    // Fake data for notifications
    const notifications = [
        {
            id: 1,
            type: "INTERVIEWS",
            title: "Interview Scheduled: TechCorp",
            description: "Your technical interview for the Senior Software Engineer position has been confirmed for March 17, 2025, at 11:00 AM PST.",
            time: "2 hours ago",
            icon: "calendar",
            color: "#7c3aed", // Purple for interviews
            actions: [
                { label: "PREPARE WITH AI", primary: true },
                { label: "VIEW DETAILS", primary: false }
            ]
        },
        {
            id: 2,
            type: "APPLICATIONS",
            title: "Application Update: InnoDesign",
            description: "Your application for UX/UI Designer position has moved to the screening phase.",
            time: "5 hours ago",
            icon: "star",
            color: "#10b981", // Green for applications
            actions: [
                { label: "VIEW APPLICATION", primary: false }
            ]
        },
        {
            id: 3,
            type: "MESSAGES",
            title: "New Message from Sarah Kim",
            description: "Sarah Kim (Senior Product Manager at TechCorp) has sent you a message about your upcoming interview.",
            time: "Yesterday",
            icon: "message",
            color: "#f59e0b", // Yellow for messages
            actions: [
                { label: "REPLY", primary: true },
                { label: "VIEW MESSAGE", primary: false }
            ]
        },
        {
            id: 4,
            type: "INSIGHTS",
            title: "AI Interview Coach Insight",
            description: "Based on your recent mock interview performance, we've identified areas for improvement in system design questions.",
            time: "2 days ago",
            icon: "cpu",
            color: "#3b82f6", // Blue for insights
            actions: [
                { label: "START PRACTICE", primary: true },
                { label: "VIEW REPORT", primary: false }
            ]
        }
    ];

    // Get notifications based on active filter
    const filteredNotifications =
        activeFilter === "ALL"
            ? notifications
            : notifications.filter((item) => item.type === activeFilter);

    // Count number of notifications in each category 
    const counts = {
        INTERVIEWS: notifications.filter(n => n.type === "INTERVIEWS").length,
        MESSAGES: notifications.filter(n => n.type === "MESSAGES").length,
        APPLICATIONS: notifications.filter(n => n.type === "APPLICATIONS").length,
        INSIGHTS: notifications.filter(n => n.type === "INSIGHTS").length
    };

    const getIconComponent = (iconName: string) => {
        switch(iconName) {
            case 'calendar':
                return <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect><line x1="16" y1="2" x2="16" y2="6"></line><line x1="8" y1="2" x2="8" y2="6"></line><line x1="3" y1="10" x2="21" y2="10"></line></svg>;
            case 'star':
                return <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>;
            case 'message':
                return <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"></path></svg>;
            case 'cpu':
                return <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><rect x="4" y="4" width="16" height="16" rx="2" ry="2"></rect><rect x="9" y="9" width="6" height="6"></rect><line x1="9" y1="1" x2="9" y2="4"></line><line x1="15" y1="1" x2="15" y2="4"></line><line x1="9" y1="20" x2="9" y2="23"></line><line x1="15" y1="20" x2="15" y2="23"></line><line x1="20" y1="9" x2="23" y2="9"></line><line x1="20" y1="14" x2="23" y2="14"></line><line x1="1" y1="9" x2="4" y2="9"></line><line x1="1" y1="14" x2="4" y2="14"></line></svg>;
            default:
                return null;
        }
    };

    return (
        <div className={`min-h-screen py-16 px-4 md:px-10 flex justify-center ${darkMode ? 'bg-gray-900' : 'bg-fairjob-bg'}`}>
            <div className="w-full max-w-5xl">
                {/* Header with theme toggle */}
                <div className="flex justify-between items-center mb-6">
                    <h1 className={`text-5xl font-bold ${darkMode ? 'text-white' : 'text-gray-800'}`}>
                        Notifications
                    </h1>
                    <div className="flex gap-3">
                        {/* Theme toggle button */}
                        <button 
                            onClick={() => setDarkMode(!darkMode)}
                            className={`p-2 rounded-full text-sm font-medium transition-all duration-200 ${darkMode ? 'bg-gray-700 text-white' : 'bg-gray-200 text-gray-800'}`}
                        >
                            {darkMode ? 
                                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><circle cx="12" cy="12" r="5"></circle><line x1="12" y1="1" x2="12" y2="3"></line><line x1="12" y1="21" x2="12" y2="23"></line><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line><line x1="1" y1="12" x2="3" y2="12"></line><line x1="21" y1="12" x2="23" y2="12"></line><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line></svg> :
                                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path></svg>
                            }
                        </button>
                        
                        {/* Mark all as read button */}
                        <button className="bg-gradient-to-r from-fairjob-text to-fairjob-primary text-white px-4 py-2 rounded-full text-sm font-medium transition-all transform hover:scale-105 hover:shadow-lg duration-200">
                            MARK ALL AS READ
                        </button>
                    </div>
                </div>

                {/* Filter navigation */}
                <div className={`rounded-lg shadow-sm mb-8 ${darkMode ? 'bg-gray-800' : 'bg-white'}`}>
                    <div className="flex p-1 overflow-x-auto">
                        {[
                            { type: "ALL", count: notifications.length },
                            { type: "INTERVIEWS", count: counts.INTERVIEWS },
                            { type: "MESSAGES", count: counts.MESSAGES },
                            { type: "APPLICATIONS", count: counts.APPLICATIONS },
                            { type: "INSIGHTS", count: counts.INSIGHTS },
                        ].map(({ type, count }) => (
                            <button
                                key={type}
                                onClick={() => setActiveFilter(type)}
                                className={`py-3 px-4 rounded-md text-lg font-medium transition-colors mx-1 ${
                                    activeFilter === type 
                                    ? 'bg-boliaj text-white' 
                                    : darkMode 
                                        ? 'text-gray-300 hover:bg-gray-700' 
                                        : 'text-gray-500 hover:bg-gray-100'
                                }`}
                            >
                                {type} <span className="font-mono">({count})</span>
                            </button>
                        ))}
                    </div>
                </div>

                {/* Notification cards list */}
                <div className="space-y-4">
                    {filteredNotifications.length > 0 ? (
                        filteredNotifications.map((note) => (
                            <div 
                                key={note.id} 
                                className={`rounded-lg shadow-lg overflow-hidden relative transition-all hover:shadow-xl ${darkMode ? 'bg-gray-800' : 'bg-white'}`}
                                style={{
                                    borderLeft: `4px solid ${note.color}`
                                }}
                            >
                                <div className="p-6">
                                    {/* Header with title, icon and time */}
                                    <div className="flex justify-between items-start mb-4">
                                        <div className="flex items-center">
                                            <div className="w-12 h-12 rounded-full flex items-center justify-center mr-4"
                                                style={{ 
                                                    backgroundColor: darkMode ? 'rgba(255,255,255,0.1)' : 'rgba(0,0,0,0.05)',
                                                    color: note.color 
                                                }}>
                                                {getIconComponent(note.icon)}
                                            </div>
                                            <h2 className={`font-bold text-lg ${darkMode ? 'text-white' : 'text-gray-800'}`}>
                                                {note.title}
                                            </h2>
                                        </div>
                                        <span className={`text-xs px-3 py-1 rounded-full ${darkMode ? 'bg-gray-700 text-gray-300' : 'bg-gray-100 text-gray-500'}`}>
                                            {note.time}
                                        </span>
                                    </div>

                                    {/* Description */}
                                    <p className={`text-sm mb-5 ml-16 ${darkMode ? 'text-gray-300' : 'text-gray-600'}`}>
                                        {note.description}
                                    </p>

                                    {/* Action buttons */}
                                    <div className="flex gap-3 ml-16">
                                        {note.actions.map((action, idx) => {
                                            // Style the button based on primary/secondary and the notification type
                                            const btnStyle = action.primary
                                                ? { backgroundColor: note.color, color: 'white' }
                                                : { 
                                                    backgroundColor: 'transparent', 
                                                    color: note.color,
                                                    border: `1px solid ${note.color}`
                                                };
                                            
                                            return (
                                                <button
                                                    key={idx}
                                                    className="px-5 py-2 rounded-full text-xs font-medium transition-all hover:shadow-md"
                                                    style={btnStyle}
                                                >
                                                    {action.label}
                                                </button>
                                            );
                                        })}
                                    </div>
                                </div>
                            </div>
                        ))
                    ) : (
                        <div className={`rounded-lg shadow-sm p-8 text-center ${darkMode ? 'bg-gray-800 text-gray-300' : 'bg-white text-gray-500'}`}>
                            <p>No notifications in this category.</p>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}