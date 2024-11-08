import { createStore } from 'vuex'

// 从 localStorage 获取初始状态
const getInitialState = () => {
  try {
    const savedState = localStorage.getItem('vuex-state')
    return savedState ? JSON.parse(savedState) : {
      user: null,
      applicantId: null
    }
  } catch (e) {
    return {
      user: null,
      applicantId: null
    }
  }
}

// 创建一个新的 store 实例
export default createStore({
  state: getInitialState(),
  mutations: {
    setUser(state, user) {
      state.user = user
      // 保存到 localStorage
      localStorage.setItem('vuex-state', JSON.stringify(state))
    },
    setApplicantId(state, id) {
      state.applicantId = id
      // 保存到 localStorage
      localStorage.setItem('vuex-state', JSON.stringify(state))
    },
    clearUser(state) {
      state.user = null
      state.applicantId = null
    }
  },
  actions: {
    loginUser({ commit }, { applicantId, userInfo }) {
      commit('setApplicantId', applicantId)
      commit('setUser', userInfo)
    },
    logoutUser({ commit }) {
      commit('clearUser')
    }
  },
  getters: {
    isAuthenticated: state => !!state.user,
    currentApplicantId: state => state.applicantId
  }
})