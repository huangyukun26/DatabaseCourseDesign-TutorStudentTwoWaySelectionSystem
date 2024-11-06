
import { createApp } from 'vue';
import App from './App.vue';
import router from './router';  // 导入 Vue Router 配置
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'

//创建 Vue 应用实例
const app = createApp(App);

//使用 Vue Router
app.use(router);
app.use(ElementPlus)  //全局使用 Element Plus
//挂载应用到 DOM
app.mount('#app');







