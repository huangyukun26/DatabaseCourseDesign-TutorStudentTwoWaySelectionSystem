<template>
  <div class="logo">
      Beijing Forestry University Master’s Admissions System By Four Stopwatch Group
    </div>
  <div class="login-container">

    <img src="/images/loginpage.jpg" alt="My Image" class="cover-image" />


    <div class="welcome">
      欢迎报考北京林业大学！
    </div>

    <div class="login-box">
      <div class="logo-area">
        <h1>系统登录</h1>

        <form @submit.prevent="login">
          <!-- ID -->
          <div class="form-group">
            <label for="userId">用户 ID:</label>
            <input type="text" v-model="applicantId" required placeholder="请输入用户 ID" />
          </div>

          <!-- 密码 -->
          <div class="form-group">
            <label for="password">密码:</label>
            <input type="password" v-model="password" required placeholder="请输入密码" />
            <div class="link-group">
            <a href="/forgot-password">忘记密码?</a>
            <a href="/help">使用帮助</a>
            </div>
          </div>

          <!-- 验证码 -->
          <div class="form-group">
            <label for="captcha">验证码:</label>
            <input type="text" v-model="captchaInput" required placeholder="请输入验证码" />
            <img :src="captchaUrl" alt="验证码" class="captcha-image" @click="refreshCaptcha" />
          </div>

          <!-- 登录按钮 -->
          <button type="submit" class="login-button">登录</button>

        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { useStore } from 'vuex'
import { userService } from '@/services/userService'
import { ElMessage } from 'element-plus'

export default {
  setup() {
    const store = useStore()
    return { store }
  },

  data() {
    return {
      applicantId: '',
      password: '',
      captchaInput: '',
      captchaUrl: 'http://localhost:8000/api/generate_captcha?' + new Date().getTime()
    }
  },

  methods: {
    async login() {
      try {
        if (!this.applicantId || !this.password || !this.captchaInput) {
          ElMessage.warning("请填写所有信息！")
          return
        }

        console.log('正在尝试登录，applicantId:', this.applicantId)

        const response = await fetch("http://localhost:8000/api/login/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({
            userId: this.applicantId,
            password: this.password,
            captcha: this.captchaInput
          }),
          credentials: 'include'
        })

        const data = await response.json()
        console.log('登录响应:', data)

        if (data.success) {
          const userInfo = {
            applicant_id: this.applicantId,
            isAuthenticated: true,
            userType: data.user_type,
            loginTime: new Date().toISOString(),
            ...data.user
          }
          
          this.store.dispatch('loginUser', {
            applicantId: this.applicantId,
            userInfo: userInfo
          })
          
          localStorage.setItem('vuex-state', JSON.stringify({
            user: userInfo,
            applicantId: this.applicantId,
            userType: data.user_type
          }))
          
          userService.setUser(userInfo)
          
          ElMessage.success('登录成功')
          
          if (data.user_type === 'mentor') {
            this.$router.push('/mentor/dashboard')
          } else {
            this.$router.push({ name: "StudentDashboard" })
          }
        } else {
          ElMessage.error(data.error || "登录失败，请检查信息是否正确")
          this.refreshCaptcha()
        }
      } catch (error) {
        console.error("登录请求失败：", error)
        ElMessage.error("登录失败：" + error.message)
        this.refreshCaptcha()
      }
    },

    refreshCaptcha() {
      this.captchaUrl = 'http://localhost:8000/api/generate_captcha?' + new Date().getTime()
    },

    clearLoginState() {
      this.store.dispatch('logoutUser')
      
      localStorage.removeItem('vuex-state')
      
      userService.clearUser()
    }
  },

  mounted() {
    this.clearLoginState()
    
    this.refreshCaptcha()
  },

  beforeMount() {
    this.clearLoginState()
  }
}
</script>

<style scoped>

html, body {
  height: 100%;
  margin: 0;
  overflow: hidden; 
}

.login-container {
  position: relative; 
  align-items: center;
  eight: calc(100vh - 100px); 
  background-color: #f7f7f7;
}

.cover-image {
  position: fixed; 
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  z-index: 1; 

}

.logo{
  position: relative; 
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 30px;
  height: 100px;
  background-color: RGB(30, 115, 71);
  color: white;
  font-size: 36px;
  font-weight: bold;
  z-index: 3;
}

.welcome {
  background-color: rgba(0, 0, 0, 0);
  align-content: center;
  position: absolute;
  top: 400px; 
  left: 100px; 
  z-index: 3; 
  color: white; 
  font-size: 100px; 

}

.login-box {
  background-color: white;
  position: relative; 
  float: right; 
  width: 500px; 
  height: 700px;
  margin-top: 150px;
  margin-right: 150px;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  z-index: 3; 
}

.logo-area {
  flex: 1; 
  text-align: center;
  margin-right: 20px; 
}


h1 {
  font-size: 24px;
  margin-bottom: 20px;
  color: #333333;
}

.form-group {
  margin-bottom: 1.5rem;
  text-align: left;
}

label {
  display: block;
  font-size: 20px;
  color: #666666;
  margin-bottom: 5px;
}

input[type="text"],
input[type="password"] {
  width: 100%;
  height: 60px;
  padding: 10px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 5px;
  box-sizing: border-box;
}

.captcha-image {
  display: block;
  margin-top: 0.5rem;
  width: 100px;
  height: auto;
}

.login-button {
  width: 100%;
  height: 60px;
  padding: 10px;
  font-size: 20px;
  background-color: rgb(51, 132, 93);
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.login-button:hover {
  background-color: #45a049;
}

.link-group {
  display: flex;
  justify-content: space-between;
  margin-top: 5px;
}

.link-group a {
        text-decoration: none;
        color: rgb(51, 132, 93);
    }
    .link-group a:hover {
        text-decoration: underline;
    }
</style>
