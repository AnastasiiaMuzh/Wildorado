import { useState } from "react";
import { useNavigate } from "react-router-dom";

const EventForm = ({ initialData = { title: "", description: "", maxParticipants: "", date: "" }, onSubmit, submitButtonText }) => {
    const [formData, setFormData] = useState(initialData);
    const [errors, setErrors] = useState({});
    const [successMessage, setSuccessMessage] = useState("");
    const navigate = useNavigate();

    // field changes
    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData((prev) => ({ ...prev, [name]: value }));
    };

    // send form
    const handleSubmit = async (e) => {

        e.preventDefault();

        try {
            const result = await onSubmit(formData); 
            if (result) {
                setSuccessMessage(`${submitButtonText} successful!`);
                setTimeout(() => navigate("/events"), 1500);
            } else {
                setErrors({general: "Events form failed."})
            }
        } catch (err) {
            // Если произошла ошибка, сначала берем сообщение из ошибки, если оно есть!
            let errorMessage = err.message || "Error during submission";
            // Если объект ошибки имеет метод json (например, Response от fetch), пытаемся извлечь из него подробное сообщение
            if (err.json) {
                try {
                    const errData = await err.json();
                    if (errData && errData.message) {
                        errorMessage = errData.message;
                    }
                    if (errData && errData.errors) {
                        setErrors(errData.errors);
                        return; 
                    }
                } catch (jsonErr) {
                    console.error("Error parsing error response:", jsonErr);
                }
            }          
            //сообщение об ошибке, dlya пользователya
            setErrors({ general: errorMessage });
        }
    };

    return (
        <form onSubmit={handleSubmit}>
        <h1>{submitButtonText}</h1>

        {successMessage && <p style={{ color: "green" }}>{successMessage}</p>}
        {errors.general && <p style={{ color: "red" }}>{errors.general}</p>}

        <label>Title:</label>
        <input type="text" name="title" value={formData.title} onChange={handleChange} />
        {errors.title && <p style={{color: "red"}}>{errors.title}</p>}

        <label>Description:</label>
        <textarea name="description" value={formData.description} onChange={handleChange} />
        {errors.description && <p style={{color: "red"}}>{errors.description}</p>}

        <label>Date:</label>
        <input type="datetime-local" name="date" value={formData.date} onChange={handleChange} />
        {errors.date && <p style={{color: "red"}}>{errors.date}</p>}

        <label>Max Participants:</label>
        <input type="number" name="maxParticipants" value={formData.maxParticipants} onChange={handleChange} />
        {errors.maxParticipants && <p style={{color: "red"}}>{errors.maxParticipants}</p>}

        <button type="submit">{submitButtonText}</button>
        </form>
    );
};

export default EventForm;
