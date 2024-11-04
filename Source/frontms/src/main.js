/*import { createApp } from 'vue'
import App from './App.vue'

createApp(App).mount('#app')*/
import { createApp } from 'vue';
import App from './App.vue';
import router from './router';  // 导入 Vue Router 配置

// 创建 Vue 应用实例
const app = createApp(App);

// 使用 Vue Router
app.use(router);

// 挂载应用到 DOM
app.mount('#app');




