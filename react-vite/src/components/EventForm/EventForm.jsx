import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./EventFormModal.css";

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

        const newErrors = {}

        const selectDate = new Date(formData.date)
        const now = new Date();

        if(selectDate < now) {
            newErrors.date = "Date must be in the future";
        }

        if (Object.keys(newErrors).length > 0) {
            console.log("Validation errors:", newErrors);
            await setErrors(newErrors); // Ждем обновления состояния
            return; // Прерываем отправку запроса
        }

        try {
            const result = await onSubmit(formData); 
            if (result) {
                setSuccessMessage(`${submitButtonText} successful!`);
                setErrors({});
                setTimeout(() => navigate("/events"), 1500);
            } else {
                setErrors({general: "All fields must to be completed."})
            }
        } catch (err) {
            console.log("ERR for ERIKA", err)
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
                        console.log("Backend errors", errData.errors)
                        await setErrors(errData.errors)
                        return; 
                    }
                } catch (jsonErr) {
                    console.error("Error parsing error response:", jsonErr);
                }
            }          
            // Ошибка НЕ с бэка — записываем в общий блок
            await setErrors({ general: errorMessage });

        }
    };

    return (
        <div className="create-event-main">
            <form onSubmit={handleSubmit}>
            <h1>{submitButtonText}</h1>

            {successMessage && <p style={{ color: "green" }}>{successMessage}</p>}
            {errors.general && <p style={{ color: "red" }}>{errors.general}</p>}

            <div className="crete-event-fields">
                <div className="form-group">
                    <label>Title:</label>
                    <input type="text" name="title" value={formData.title} onChange={handleChange} />
                    {errors.title && <p style={{color: "red"}}>{errors.title}</p>}
                </div>

                <div className="form-group">
                    <label>Description:</label>
                    <textarea name="description" value={formData.description} onChange={handleChange} />
                    {errors.description && <p style={{color: "red"}}>{errors.description}</p>}
                </div>

                <div className="form-group">
                    <label>Date:</label>
                    <input type="datetime-local" name="date" value={formData.date} onChange={handleChange} />
                    {errors.date && <p style={{color: "red"}}>{errors.date}</p>}
                </div>

                <div className="form-group">
                    <label>Max Participants:</label>
                    <input type="number" name="maxParticipants" value={formData.maxParticipants} onChange={handleChange} />
                    {errors.maxParticipants && <p style={{color: "red"}}>{errors.maxParticipants}</p>}
                </div>    
            </div>
            <button type="submit">{submitButtonText}</button>
            </form>
        </div>
    );
};

export default EventForm;
