export const categoryNames = {
  1: "Hiking",
  2: "Rafting",
  3: "Camping",
  4: "Climbing",
  5: "Snow Sports",
  6: "ATV/Bikes",
};

export const categoryFields = {
  1: ["name", "city", "description", "elevation", "difficulty", "distance", "bestSeason"],
  2: ["name", "city", "description", "river_class", "distance"],
  3: ["name", "city", "description", "maxTents", "fireAllowed", "lake", "distance", "elevation"],
  4: ["name", "city", "description", "routeType", "difficulty", "elevation", "distance"],
  5: ["name", "city", "description", "bestSeason", "elevation", "distance"],
  6: ["name", "city", "description", "terrainType", "distance", "elevation"],
};

export const enumOptions = {
  difficulty: ["Easy", "Medium", "Hard"],
  river_class: ["I", "II", "III", "IV", "V"],
  routeType: ["Trad", "Sport"],
  terrainType: ["Dirt", "Rocky", "Forest", "Mixed"],
  fireAllowed: ["Yes", "No"],
  lake: ["Yes", "No"],

};