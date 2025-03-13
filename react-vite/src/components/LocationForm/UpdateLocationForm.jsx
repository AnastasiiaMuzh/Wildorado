import { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import { useDispatch } from "react-redux";
import { thunkUpdateLocation } from "../../redux/locations";
import LocationForm from "./LocationForm";
import { useNavigate } from "react-router-dom";

function removeSuffix(str, suffix) {
  if (!str) return "";
  return str.replace(suffix, "").trim();
}

const UpdateLocationForm = () => {
  const { locationId } = useParams();
  const dispatch = useDispatch();
  const navigate = useNavigate(); 

  const [initialData, setInitialData] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    async function fetchData() {
      try {
        const res = await fetch(`/api/locations/${locationId}`);
        if (!res.ok) {
          throw new Error("Failed to fetch location data");
        }
        const data = await res.json();
        console.log("GET FROM SERVER!:", data);

        // 1) Parsing categorySpecific
        const catSpec = data.categorySpecific || {};

        // distance/elevation
        const dist = removeSuffix(catSpec.distance, " mi");
        const elev = removeSuffix(catSpec.elevation, " ft");

        // Other fields
        const difficulty = catSpec.difficulty || "";
        const bestSeason = catSpec.bestSeason || "";
        const riverClass = catSpec.river_class || "";
        const maxTents = catSpec.maxTents ?? "";
        const fireAllowed = catSpec.fireAllowed ? "Yes" : "No";
        const lake = catSpec.lake ? "Yes" : "No";
        const routeType = catSpec.routeType || "";
        const terrainType = catSpec.terrainType || "";

        // 2) Convert an array of images objects into an array of strings (URLs)
        const images = data.images?.map((img) => img.url) || ["", "", "", ""];
        while (images.length < 4) images.push("");

        // 3) the object that we will pass to LocationForm
        const newFormData = {
          categoryId: data.categoryId,     
          name: data.name || "",
          city: data.city || "",
          description: data.description || "",
          distance: dist,
          elevation: elev,
          difficulty,
          bestSeason,
          riverClass,
          maxTents,
          fireAllowed,
          lake,
          routeType,
          terrainType,
          images,
        };

        setInitialData(newFormData);
      } catch (err) {
        console.error("Error loading:", err);
        setError(err.message);
      }
    }
    fetchData();
  }, [locationId]);

  const handleCancel = () => {
    navigate(`/locations/current`); 
  };


  const handleSubmit = async (payload) => {
    const updatedLoc = await dispatch(thunkUpdateLocation(locationId, payload)); //will return the updated location (or null)
    return updatedLoc;
  };

  if (error) {
    return <p className="error">{error}</p>;
  }
  if (!initialData) {
    return <p>Loading location data...</p>;
  }

  return (
    <div className="update-loc-container">
    <LocationForm
      initialData={initialData}
      onSubmit={handleSubmit}
      submitButtonText="Update Location"
      disableCategory={true}  // Can't change!!!!!!
    />
    <button type="button" className="cancel-btn" onClick={handleCancel}>
      Cancel
    </button>
  </div>
  );
};

export default UpdateLocationForm;
