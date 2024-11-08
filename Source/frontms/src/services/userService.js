// 定义不同用户类型的存储键
const STUDENT_KEY = 'student-user';
const MENTOR_KEY = 'mentor-user';

export const userService = {
  // 存储用户信息
  setUser(userData) {
    try {
      // 根据用户类型选择存储键，但不清除其他类型的用户信息
      const storageKey = userData.userType === 'mentor' ? MENTOR_KEY : STUDENT_KEY;
      console.log(`Setting ${userData.userType} user data:`, userData);
      localStorage.setItem(storageKey, JSON.stringify(userData));
    } catch (e) {
      console.error('存储用户信息失败:', e);
    }
  },

  // 获取特定类型用户信息
  getUserByType(userType) {
    try {
      const key = userType === 'mentor' ? MENTOR_KEY : STUDENT_KEY;
      const userStr = localStorage.getItem(key);
      const userData = userStr ? JSON.parse(userStr) : null;
      console.log(`Getting ${userType} user data:`, userData);
      return userData;
    } catch (e) {
      console.error(`获取${userType}用户信息失败:`, e);
      return null;
    }
  },

  // 检查特定类型用户是否已登录
  isAuthenticatedByType(userType) {
    const user = this.getUserByType(userType);
    const isAuth = user && user.isAuthenticated;
    console.log(`Checking ${userType} auth:`, isAuth);
    return isAuth;
  },

  // 获取特定类型用户ID
  getUserId(userType) {
    const user = this.getUserByType(userType);
    if (!user) return null;
    return userType === 'mentor' ? user.mentor_id : user.applicant_id;
  },

  // 清除特定类型用户信息
  clearUserByType(userType) {
    const key = userType === 'mentor' ? MENTOR_KEY : STUDENT_KEY;
    console.log(`Clearing ${userType} user data`);
    localStorage.removeItem(key);
  },

  // 清除所有用户信息
  clearAllUsers() {
    localStorage.removeItem(STUDENT_KEY);
    localStorage.removeItem(MENTOR_KEY);
  },

  // 更新特定类型用户信息
  updateUser(newData) {
    if (!newData.userType) return;
    const key = newData.userType === 'mentor' ? MENTOR_KEY : STUDENT_KEY;
    const currentUser = this.getUserByType(newData.userType);
    if (currentUser) {
      localStorage.setItem(key, JSON.stringify({ ...currentUser, ...newData }));
    }
  }
};