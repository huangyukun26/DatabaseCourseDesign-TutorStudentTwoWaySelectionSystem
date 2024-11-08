// 用户信息管理服务
const USER_KEY = 'user';

export const userService = {
  // 存储用户信息
  setUser(userData) {
    try {
      localStorage.setItem(USER_KEY, JSON.stringify(userData));
    } catch (e) {
      console.error('存储用户信息失败:', e);
    }
  },

  // 获取用户信息
  getUser() {
    try {
      const userStr = localStorage.getItem(USER_KEY);
      return userStr ? JSON.parse(userStr) : null;
    } catch (e) {
      console.error('获取用户信息失败:', e);
      return null;
    }
  },

  // 获取用户ID
  getUserId() {
    const user = this.getUser();
    return user ? user.applicant_id : null;
  },

  //获取导师的学科ID
  getCurrentUserSubjectId() {
    const user = this.getUser();
    return user ? user.subject : null;
  },

  // 检查是否已登录
  isAuthenticated() {
    const user = this.getUser();
    return user && user.isAuthenticated;
  },

  // 清除用户信息（登出）
  clearUser() {
    localStorage.removeItem(USER_KEY);
  },

  // 更新用户信息
  updateUser(newData) {
    const currentUser = this.getUser();
    if (currentUser) {
      this.setUser({ ...currentUser, ...newData });
    }
  }
};