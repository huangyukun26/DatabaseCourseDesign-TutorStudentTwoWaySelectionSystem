<template>
  <div class="content">
    <div class="basic-info">
      <h2>基本信息</h2>
      
      <!-- 加载提示 -->
      <div v-if="loading" class="loading">加载中...</div>
      <div v-if="error" class="error-message">
        {{ error }}
        <button @click="error = null" class="close-button">×</button>
      </div>

      <!-- 信息展示 -->
      <div v-if="!loading && !error && basicInfo" class="info-card">
        <div class="info-section">
          <div class="info-grid">
            <div class="info-item">
              <span class="label">姓名：</span>
              <span class="value">{{ basicInfo.name }}</span>
            </div>
            <div class="info-item">
              <span class="label">出生日期：</span>
              <span class="value">{{ basicInfo.birth_date }}</span>
            </div>
            <div class="info-item">
              <span class="label">身份证号：</span>
              <span class="value">{{ basicInfo.id_card_number }}</span>
            </div>
            <div class="info-item">
              <span class="label">生源地：</span>
              <span class="value">{{ basicInfo.origin }}</span>
            </div>
            <div class="info-item">
              <span class="label">本科院校：</span>
              <span class="value">{{ basicInfo.undergraduate_school }}</span>
            </div>
            <div class="info-item">
              <span class="label">本科专业：</span>
              <span class="value">{{ basicInfo.undergraduate_major }}</span>
            </div>
            <div class="info-item">
              <span class="label">学校类型：</span>
              <span class="value">{{ basicInfo.school_type }}</span>
            </div>
            <div class="info-item">
              <span class="label">邮箱：</span>
              <span class="value">{{ basicInfo.email }}</span>
            </div>
            <div class="info-item">
              <span class="label">电话：</span>
              <span class="value">{{ basicInfo.phone }}</span>
            </div>
          </div>
        </div>

        <!-- 简历信息 -->
        <div class="info-section">
          <h3>简历信息</h3>
          <div class="resume-content">
            {{ basicInfo.resume }}
          </div>
        </div>
      </div>

      <!-- 无数据提示 -->
      <div v-else-if="!loading && !error" class="no-data">
        暂无个人信息数据
      </div>
    </div>
  </div>
</template>

<script>
import { userService } from '@/services/userService'
import { ElMessage } from 'element-plus'

export default {
  data() {
    return {
      basicInfo: null,
      loading: false,
      error: null
    }
  },

  created() {
    // 使用新的 isAuthenticatedByType 方法检查学生登录状态
    if (!userService.isAuthenticatedByType('student')) {
      ElMessage.error('请先登录')
      this.$router.push('/login')
      return
    }
    this.fetchBasicInfo()
  },

  methods: {
    async fetchBasicInfo() {
      try {
        this.loading = true
        this.error = null
        
        const studentUser = userService.getUserByType('student')
        if (!studentUser || !studentUser.applicant_id) {
          throw new Error('无法获取用户信息')
        }

        const response = await fetch(`http://localhost:8000/api/applicant/basic-info/${studentUser.applicant_id}/`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
          },
          credentials: 'include'
        })

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`)
        }

        const data = await response.json()
        console.log('Received data:', data)

        if (data.status === 'success') {
          this.basicInfo = data.data
        } else {
          throw new Error(data.message || '获取基本信息失败')
        }
      } catch (error) {
        console.error('Error fetching basic info:', error)
        this.error = error.message || '获取信息失败，请稍后重试'
        ElMessage.error(this.error)
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
.content {
  padding: 20px;
  background-color: #f5f5f5;
  min-height: 100%;
}

.basic-info {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

h2 {
  text-align: center;
  color: RGB(51, 132, 93);
  margin-bottom: 20px;
}

h3 {
  color: RGB(51, 132, 93);
  margin-bottom: 15px;
  font-size: 18px;
}

.info-container {
  display: grid;
  gap: 20px;
}

.info-section {
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
}

.info-item {
  padding: 10px;
  display: flex;
  align-items: center;
}

.label {
  color: RGB(51, 132, 93);
  font-weight: bold;
  min-width: 80px;
  margin-right: 10px;
}

.value {
  color: #333;
}

.resume-section {
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
}

.resume-content {
  background-color: white;
  padding: 15px;
  border-radius: 4px;
  min-height: 100px;
  line-height: 1.6;
}

.loading {
  text-align: center;
  padding: 20px;
  color: RGB(51, 132, 93);
}

.error-message {
  background-color: #ff4444;
  color: white;
  padding: 10px 20px;
  border-radius: 4px;
  margin-bottom: 20px;
  position: relative;
}

.close-button {
  background: none;
  border: none;
  color: white;
  position: absolute;
  right: 10px;
  top: 50%;
  transform: translateY(-50%);
  cursor: pointer;
}

.no-data {
  text-align: center;
  padding: 40px;
  color: #666;
}
</style>
