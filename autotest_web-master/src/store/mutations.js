export default {

    isLogin(state, value) {
        state.token = value;
    },

    setUser(state, value) {
        state.user = value;
    },
    setRouterName(state, value) {
        state.routerName = value
    },
    setUseractualname(state, value) {
        state.useractualname = value;
    },
    setUseEmail(state, value) {
        state.email = value;
    },
    setIs_superuser(state, value) {
        state.Is_superuser = value;
    },
}