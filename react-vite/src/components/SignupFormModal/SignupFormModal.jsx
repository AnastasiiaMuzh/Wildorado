import { useState } from "react";
import { useDispatch } from "react-redux";
import { useModal } from "../../context/Modal";
import { thunkSignup } from "../../redux/session";
import "./SignupForm.css";


function SignupFormModal() {
  const dispatch = useDispatch();
  const [email, setEmail] = useState("");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [avatar, setAvatar] = useState(""); 
  const [bio, setBio] = useState(""); 
  const [interests, setInterests] = useState(""); 
  const [errors, setErrors] = useState({});
  const { closeModal } = useModal();

  const handleSubmit = async (e) => {
    e.preventDefault();
  
    if (password !== confirmPassword) {
      return setErrors({
        confirmPassword: "Confirm Password field must be the same as the Password field",
      });
    }
  
    console.log("Отправка данных на сервер...", { email, username, password, avatar, bio, interests });
  
    const serverResponse = await dispatch(
      thunkSignup({
        email,
        username,
        password,
        avatar: avatar || null,
        bio: bio || null,
        interests: interests || null
      })
    );
  
    console.log("✅ Ответ сервера:", serverResponse); // ✅ Теперь должно быть не undefined
  
    if (serverResponse && !serverResponse.errors) {
      closeModal();
    } else {
      setErrors(serverResponse);
    }
  };
  

  return (
    // <div className="modal-overlay" onClick={(e) => {
    //   if (e.target.classList.contains("modal-overlay")) {
    //     closeModal();
    //   }
    //   }}>
      <div className="signup-form-modal">
        <h1>Sign Up</h1>
        {errors.server && <p>{errors.server}</p>}
        <form onSubmit={handleSubmit} className="signup-form">
          <label>
            Email
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </label>
          {errors.email && <p>{errors.email}</p>}
  
          <label>
            Username
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
            />
          </label>
          {errors.username && <p>{errors.username}</p>}
  
          <label>
            Password
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </label>
          {errors.password && <p>{errors.password}</p>}
  
          <label>
            Confirm Password
            <input
              type="password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              required
            />
          </label>
          {errors.confirmPassword && <p>{errors.confirmPassword}</p>}
  
          <label>
            Upload Avatar (optional)
            <input
              type="text"
              value={avatar}
              onChange={(e) => setAvatar(e.target.value)}
            />
          </label>
  
          <label>
            Bio (optional)
            <textarea
              value={bio}
              onChange={(e) => setBio(e.target.value)}
              placeholder="Tell something about yourself"
            />
          </label>
  
          <label>
            Interests (optional)
            <input
              type="text"
              value={interests}
              onChange={(e) => setInterests(e.target.value)}
              placeholder="Hiking, Camping, etc."
            />
          </label>
  
          <button type="submit">Sign Up</button>
        </form>
      </div>
    // </div>
  );
}
export default SignupFormModal;
