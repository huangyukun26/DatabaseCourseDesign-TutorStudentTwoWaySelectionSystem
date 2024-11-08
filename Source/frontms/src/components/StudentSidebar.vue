<template>
  <div class="sidebar">
       <!-- 学生侧边栏菜单项 -->
    <div v-if="userRole === 'student'" class="menu-item">招生计划</div>
    <div v-if="userRole === 'student'" class="menu-item" @click="navigateTo('basic-info')">基本信息</div>
    <div v-if="userRole === 'student'" class="menu-item" @click="navigateTo('student-scores')">成绩查询</div>
    <div v-if="userRole === 'student'" class="menu-item" @click="navigateTo('student-volunteer-selection')">志愿填报</div>
    <div v-if="userRole === 'student'" class="menu-item">录取状态</div>
      <!-- 导师侧边栏菜单项 -->
    <div v-if="userRole === 'teacher'" class="menu-item">招生计划</div>
    <div v-if="userRole === 'teacher'" class="menu-item" @click="navigateTo('all-student-basic-info')">基本信息</div>
    <div v-if="userRole === 'teacher'" class="menu-item" @click="navigateTo('student-info')">学生信息</div>
    <div v-if="userRole === 'teacher'" class="menu-item" @click="navigateTo('student-volunteer-selection')">已录取的学生</div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      userRole: ''  // 初始值为空
    };
  },
  mounted() {
    // 从 localStorage 获取存储的角色信息
    this.userRole = localStorage.getItem('userRole') || '';  // 如果没有角色信息，默认为空
  },
  methods: {
    navigateTo(routeName) {
      this.$router.push({ name: routeName });
    }
  }
};
</script>

<style scoped>
.sidebar {
  width: 250px;
  background-color: #F1F1F1;
  padding: 10px;
}

.menu-item {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 40px;
  padding: 15px;
  cursor: pointer;
  color: RGB(249, 249, 249);
  background-color: RGB(51, 132, 93);
  border: 1px solid #DDDDDD;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
  margin-bottom: 10px;
  text-align: center;
  font-size: 22px;
}

.menu-item:hover {
  background-color: RGB(249, 249, 249);
  color: RGB(1, 101, 54);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
}
</style>
