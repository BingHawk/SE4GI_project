export const state = () => ({
    lastCity: "Roma",
});

export const mutations = {
  setCity(state, newCity) {
    state.lastCity = newCity;
  },
};

// export const getters: {
//     lastCity: state => state.lastCity,
//   },