export const state = () => ({
    lastCity: "Choose City",
});

export const mutations = {
  setCity(state, newCity) {
    state.lastCity = newCity;
  },
};

// export const getters: {
//     lastCity: state => state.lastCity,
//   },