import { getToken, setToken } from '@baserow/modules/core/utils/auth'

export const state = () => ({
  authToken: null,
  isPublic: false,
})

export const mutations = {
  SET_AUTH_TOKEN(state, value) {
    state.authToken = value
  },
  SET_IS_PUBLIC(state, value) {
    state.isPublic = value
  },
}

export const actions = {
  setAuthTokenFromCookies({ commit }, { slug }) {
    const token = getToken(this.app, slug)
    commit('SET_AUTH_TOKEN', token)
    return token
  },
  setAuthToken({ commit }, { slug, token }) {
    setToken(token, this.app, slug)
    commit('SET_AUTH_TOKEN', token)
  },
  setIsPublic({ commit }, value) {
    commit('SET_IS_PUBLIC', value)
  },
}

export const getters = {
  getAuthToken(state) {
    return state.authToken
  },
  getIsPublic(state) {
    return state.isPublic
  },
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
}
