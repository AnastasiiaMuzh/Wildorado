import React from "react";
import { useDispatch } from "react-redux";
import { useNavigate } from "react-router-dom";
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
  riverClass: "",
  maxTents: "",
  fireAllowed: "No",
  lake: "No",
  routeType: "",
  terrainType: "",
  images: ["", "", "", ""],
};

const CreateLocationForm = () => {
  const dispatch = useDispatch();
  const navigate = useNavigate();

  const handleSubmit = async (payload) => {
    const newLoc = await dispatch(thunkCreateLocation(payload));
    return newLoc;
  };

  return (
    <LocationForm
      initialData={initialData}
      onSubmit={handleSubmit}
      submitButtonText="Create Location"
      disableCategory={false}
    />
  );
};

export default CreateLocationForm;
