<template>
  <div class="sidebar">
    <div class="menu-item" @click="navigateTo('mentor-admission-plan')">招生计划</div>
    <div class="menu-item" @click="navigateTo('mentor-basic-info')">导师基本信息</div>
    <div class="menu-item" @click="navigateTo('mentor-student-list')">学生志愿申请</div>
    <div class="menu-item" @click="navigateTo('mentor-all-applications')">全院学生申请信息</div>
    <div class="menu-item" @click="navigateTo('mentor-accepted-students')">已录取学生</div>
  </div>
</template>

<script>
export default {
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
  min-width: 250px;
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