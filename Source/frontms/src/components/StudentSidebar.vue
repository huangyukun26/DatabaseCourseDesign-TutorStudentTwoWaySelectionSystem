<template>
  <div class="sidebar">
    <div class="menu-item">招生计划</div>
    <div class="menu-item" @click="navigateTo('basic-info')">基本信息</div>
    <div class="menu-item">成绩查询</div>
    <div class="menu-item">志愿填报</div>
    <div class="menu-item">录取状态</div>
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
}

.menu-item {
  display: flex; /* 使用flex布局 */
  justify-content: center; /* 水平居中 */
  align-items: center; /* 垂直居中 */
  height:40px;
  padding: 15px;
  cursor: pointer;
  color: RGB(249, 249, 249);
  background-color: RGB(51, 132, 93);
  border: 1px solid #DDDDDD; /* 灰色边框 */
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2); /* 阴影效果 */
  margin-bottom: 10px; /* 添加间距 */
  text-align: center; /* 文字居中 */
  font-size: 22px; /* 增大字体大小 */
}

.menu-item:hover {
  background-color: RGB(249, 249, 249);
  color: RGB(1, 101, 54);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3); /* 悬浮时阴影效果更明显 */
}

</style>
