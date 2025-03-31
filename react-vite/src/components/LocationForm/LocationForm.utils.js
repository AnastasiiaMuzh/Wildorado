export const categoryNames = {
  1: "Hiking",
  2: "Rafting",
  3: "Camping",
  4: "Climbing",
  5: "Snow Sports",
  6: "ATV/Bikes",
};

export const categoryFields = {
  1: ["name", "city", "elevation", "difficulty", "distance", "bestSeason", "description"],
  2: ["name", "city", "river_class", "distance", "description"],
  3: ["name", "city", "maxTents", "fireAllowed", "lake", "distance", "elevation", "description"],
  4: ["name", "city", "routeType", "difficulty", "elevation", "distance", "description"],
  5: ["name", "city", "bestSeason", "elevation", "distance", "description"],
  6: ["name", "city", "terrainType", "distance", "elevation", "description"],
};

export const enumOptions = {
  difficulty: ["Easy", "Medium", "Hard"],
  river_class: ["I", "II", "III", "IV", "V"],
  routeType: ["Trad", "Sport"],
  terrainType: ["Dirt", "Rocky", "Forest", "Mixed"],
  fireAllowed: ["Yes", "No"],
  lake: ["Yes", "No"],

};