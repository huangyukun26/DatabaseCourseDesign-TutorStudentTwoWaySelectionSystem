<template>
  <div class="content">
    <div class="score-query">
      <h2>成绩查询</h2>
      
      <!-- 加载提示 -->
      <div v-if="loading" class="loading">加载中...</div>
      <div v-if="error" class="error-message">
        {{ error }}
        <button @click="error = null" class="close-button">×</button>
      </div>

      <!-- 成绩展示 -->
      <div v-if="!loading && !error && scoreData" class="score-card">
        <!-- 考生信息 -->
        <div class="info-section">
          <h3>考生信息</h3>
          <div class="info-grid">
            <div class="info-item">
              <span class="label">考生姓名：</span>
              <span class="value">{{ scoreData.applicant_name }}</span>
            </div>
            <div class="info-item">
              <span class="label">本科院校：</span>
              <span class="value">{{ scoreData.undergraduate_info.school }}</span>
            </div>
            <div class="info-item">
              <span class="label">本科专业：</span>
              <span class="value">{{ scoreData.undergraduate_info.major }}</span>
            </div>
          </div>
        </div>

        <!-- 报考信息 -->
        <div class="info-section">
          <h3>报考信息</h3>
          <div class="info-grid">
            <div class="info-item">
              <span class="label">报考学科：</span>
              <span class="value">{{ scoreData.subject_info.name }}</span>
            </div>
            <div class="info-item">
              <span class="label">学科代码：</span>
              <span class="value">{{ scoreData.subject_info.subject_id }}</span>
            </div>
            <div class="info-item">
              <span class="label">学科类型：</span>
              <span class="value">{{ scoreData.subject_info.type }}</span>
            </div>
          </div>
        </div>

        <!-- 成绩信息 -->
        <div class="score-section">
          <h3>成绩详情</h3>
          <div class="score-grid">
            <div class="score-item">
              <div class="score-label">初试成绩</div>
              <div class="score-value">{{ scoreData.preliminary_score }}</div>
            </div>
            <div class="score-item">
              <div class="score-label">复试成绩</div>
              <div class="score-value">{{ scoreData.final_score }}</div>
            </div>
            <div class="score-item total">
              <div class="score-label">总分</div>
              <div class="score-value">{{ calculateTotalScore }}</div>
            </div>
          </div>
        </div>
      </div>

      <!-- 无成绩提示 -->
      <div v-else-if="!loading && !error" class="no-data">
        暂无成绩数据
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'

export default {
  name: 'StudentScoreQuery',
  setup() {
    const scoreData = ref(null)
    const loading = ref(false)
    const error = ref(null)
    const applicantId = ref(null)

    // 计算总分
    const calculateTotalScore = computed(() => {
      if (!scoreData.value) return 0
      const total = scoreData.value.preliminary_score + scoreData.value.final_score
      return total.toFixed(1)
    })

    // 获取考生ID
    const fetchApplicantId = () => {
      try {
        const userStr = localStorage.getItem('user')
        if (userStr) {
          const user = JSON.parse(userStr)
          if (user && user.applicant_id) {
            applicantId.value = user.applicant_id
            return true
          }
        }
        error.value = '请先登录'
        return false
      } catch (e) {
        console.error('获取考生信息失败:', e)
        error.value = '获取用户信息失败'
        return false
      }
    }

    // 获取成绩数据
    const fetchScores = async () => {
      if (!applicantId.value) return

      try {
        loading.value = true
        const response = await axios.get(`http://localhost:8000/api/applicant/scores/${applicantId.value}`)

        if (response.data.status === 'success') {
          scoreData.value = response.data.data
        } else {
          throw new Error(response.data.message || '获取成绩失败')
        }
      } catch (e) {
        console.error('获取成绩失败:', e)
        if (e.response?.status === 404) {
          error.value = e.response.data.message || '暂无成绩信息'
        } else {
          error.value = '获取成绩失败: ' + (e.response?.data?.message || e.message)
        }
      } finally {
        loading.value = false
      }
    }

    onMounted(async () => {
      if (fetchApplicantId()) {
        await fetchScores()
      }
    })

    return {
      scoreData,
      loading,
      error,
      calculateTotalScore
    }
  }
}
</script>

<style scoped>
.content {
  padding: 20px;
  background-color: #f5f5f5;
}

.score-query {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  max-width: 1200px;
  margin: 0 auto;
}

h2 {
  text-align: center;
  color: RGB(51, 132, 93);
  margin-bottom: 30px;
}

h3 {
  color: RGB(51, 132, 93);
  margin-bottom: 20px;
  font-size: 18px;
}

.score-card {
  display: grid;
  gap: 25px;
}

.info-section, .score-section {
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
  background-color: white;
  padding: 20px;
  border-radius: 6px;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 15px;
}

.label {
  color: RGB(51, 132, 93);
  font-weight: bold;
  min-width: 100px;
}

.value {
  color: #333;
  flex: 1;
}

.score-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
}

.score-item {
  background-color: white;
  padding: 25px;
  border-radius: 8px;
  text-align: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  transition: transform 0.2s;
}

.score-item:hover {
  transform: translateY(-2px);
}

.score-label {
  color: RGB(51, 132, 93);
  font-weight: bold;
  margin-bottom: 15px;
  font-size: 16px;
}

.score-value {
  font-size: 28px;
  font-weight: bold;
  color: #333;
}

.total {
  background-color: RGB(51, 132, 93);
}

.total .score-label,
.total .score-value {
  color: white;
}

.loading {
  text-align: center;
  padding: 40px;
  color: RGB(51, 132, 93);
  font-size: 16px;
}

.error-message {
  background-color: #ff4444;
  color: white;
  padding: 12px 20px;
  border-radius: 6px;
  margin-bottom: 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.close-button {
  background: none;
  border: none;
  color: white;
  font-size: 20px;
  cursor: pointer;
  padding: 0 5px;
}

.close-button:hover {
  opacity: 0.8;
}

.no-data {
  text-align: center;
  padding: 60px;
  color: #666;
  font-size: 16px;
  background-color: #f9f9f9;
  border-radius: 8px;
}

@media (max-width: 768px) {
  .score-grid {
    grid-template-columns: 1fr;
  }
  
  .info-grid {
    grid-template-columns: 1fr;
  }
}
</style>