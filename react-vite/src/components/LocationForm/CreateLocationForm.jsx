import { useDispatch } from "react-redux";
import { thunkCreateLocation } from "../../redux/locations";
import LocationForm from "./LocationForm";

// For creating Location DATA!
const initialData = {
  categoryId: "",
  name: "",
  city: "",
  description: "",
  distance: "",
  elevation: "",
  difficulty: "",
  bestSeason: "",
  river_class: "",
  maxTents: "",
  fireAllowed: "No",
  lake: "No",
  routeType: "",
  terrainType: "",
  images: ["", "", "", ""],
};

const CreateLocationFormModal = () => {
  const dispatch = useDispatch();

  const handleSubmit = async (payload) => {
    const newLoc = await dispatch(thunkCreateLocation(payload));
    return newLoc;
  };

  return (
    <LocationForm
      initialData={initialData}
      onSubmit={handleSubmit}
      submitButtonText="Create New Location"
      disableCategory={false}
    />
  );
};

export default CreateLocationFormModal;
