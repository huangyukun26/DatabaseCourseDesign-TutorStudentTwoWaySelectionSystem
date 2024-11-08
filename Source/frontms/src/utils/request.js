import axios from 'axios'
import { message } from 'ant-design-vue'

// 创建 axios 实例
const request = axios.create({
  baseURL: 'http://localhost:8000',  //
  timeout: 6000
})

// 响应拦截器
request.interceptors.response.use(
  response => {
    return response.data
  },
  error => {
    console.error('API Error:', error)  // 添加错误日志
    message.error(error.message || '请求失败')
    return Promise.reject(error)
  }
)

export default request