
import { createApp } from 'vue';
import App from './App.vue';
import router from './router';  // 导入 Vue Router 配置
import store from './store'  // 导入 store
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import Antd from 'ant-design-vue'
import 'ant-design-vue/dist/reset.css'

//创建 Vue 应用实例
const app = createApp(App);

//使用 Vue Router
app.use(store)
app.use(router);
app.use(ElementPlus)  //全局使用 Element Plus
app.use(Antd)
//挂载应用到 DOM
app.mount('#app');







