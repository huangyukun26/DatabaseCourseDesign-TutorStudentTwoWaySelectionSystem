<template>
  <div class="content">
    <div class="volunteer-selection">
      <h2>志愿填报</h2>
      
      <!-- 加载提示 -->
      <div v-if="loading" class="loading">加载中...</div>
      <div v-if="error" class="error">{{ error }}</div>

      <!-- 导师列表 -->
      <div v-if="!loading && !error" class="table-container">
        <table class="custom-table">
          <thead>
            <tr>
              <th>导师姓名</th>
              <th>职称</th>
              <th>研究方向</th>
              <th>志愿顺序</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="mentor in mentorList" :key="mentor.mentor_id">
              <td>{{ mentor.name }}</td>
              <td>{{ mentor.title }}</td>
              <td>{{ mentor.bio }}</td>
              <td>
                <select v-model="mentor.rank" class="volunteer-select">
                  <option value="">请选择</option>
                  <option v-for="n in 3" :key="n" :value="n"
                          :disabled="isRankUsed(n) && mentor.rank !== n">
                    第{{ n }}志愿
                  </option>
                </select>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- 提交按钮 -->
      <div class="submit-section">
        <button class="submit-button" 
                @click="submitVolunteer" 
                :disabled="!isValidSelection || loading">
          {{ loading ? '提交中...' : '提交志愿' }}
        </button>
      </div>

      <!-- 当前选择状态 -->
      <div class="selection-status">
        <h3>当前志愿选择</h3>
        <div class="status-container">
          <div v-for="n in 3" :key="n" class="status-item">
            <span class="status-label">第{{ n }}志愿：</span>
            <span class="status-value">{{ getSelectedMentorName(n) }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

export default {
  name: 'VolunteerSelection',
  setup() {
    const mentorList = ref([])
    const applicantId = ref(null)
    const loading = ref(false)
    const error = ref(null)

    // 获取导师列表
   const fetchMentors = async () => {
      try {
        loading.value = true
        const response = await axios.get('http://localhost:8000/api/mentors/')
        if (response.data.status === 'success') {
          mentorList.value = response.data.data.map(mentor => ({
            ...mentor,
            rank: null
          }))
          // 获取导师列表后立即获取已提交的志愿信息
          await fetchExistingVolunteers()
        } else {
          throw new Error(response.data.message || '获取数据失败')
        }
      } catch (e) {
        error.value = '获取导师列表失败: ' + (e.message || '未知错误')
        console.error('获取导师列表错误:', e)
      } finally {
        loading.value = false
      }
    }

    // 获取当前登录的考生ID
    const fetchApplicantId = () => {
      try {
        const userStr = localStorage.getItem('user')
        if (userStr) {
          const user = JSON.parse(userStr)
          console.log('当前登录用户信息:', user)
          if (user && user.applicant_id && user.isAuthenticated) {
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

    // 获取已提交的志愿信息
    const fetchExistingVolunteers = async () => {
      if (!applicantId.value) return

      try {
        const response = await axios.get(`http://localhost:8000/api/applicant/volunteers/${applicantId.value}`)
        if (response.data.status === 'success' && response.data.data.length > 0) {
          // 更新导师列表中的选择状态
          const existingChoices = response.data.data
          mentorList.value = mentorList.value.map(mentor => {
            const existingChoice = existingChoices.find(
              choice => choice.mentor_id === mentor.mentor_id
            )
            if (existingChoice) {
              return {
                ...mentor,
                rank: existingChoice.rank
              }
            }
            return mentor
          })
          console.log('已加载已提交的志愿:', existingChoices)
        }
      } catch (e) {
        console.error('获取已提交志愿失败:', e)
        error.value = '获取已提交志愿失败: ' + (e.response?.data?.message || e.message)
      }
    }

    // 检查志愿顺序是否已被使用
    const isRankUsed = (rank) => {
      return mentorList.value.some(mentor => mentor.rank === rank)
    }

    // 获取指定志愿顺序的导师姓名
    const getSelectedMentorName = (rank) => {
      const mentor = mentorList.value.find(m => m.rank === rank)
      return mentor ? mentor.name : '未选择'
    }

    // 验证选择是否有效
    const isValidSelection = computed(() => {
      const selectedCount = mentorList.value.filter(m => m.rank !== null).length
      return selectedCount === 3
    })

    // 提交志愿
    const submitVolunteer = async () => {
      if (!isValidSelection.value) {
        alert('请选择三个志愿')
        return
      }

      const userStr = localStorage.getItem('user')
      if (!userStr) {
        alert('请先登录')
        return
      }

      const user = JSON.parse(userStr)
      if (!user.isAuthenticated || !user.applicant_id) {
        alert('登录信息无效，请重新登录')
        return
      }

      try {
        loading.value = true
        const choices = mentorList.value
          .filter(mentor => mentor.rank !== null)
          .sort((a, b) => a.rank - b.rank)
          .map(mentor => ({
            mentor_id: mentor.mentor_id,
            rank: mentor.rank
          }))

        const response = await axios.post('http://localhost:8000/api/volunteer/submit', {
          applicant_id: applicantId.value,
          mentor_choices: choices
        })

        if (response.data.status === 'success') {
          alert('志愿提交成功！')
          // 提交成功后重新获取最新的志愿信息
          await fetchExistingVolunteers()
        } else {
          throw new Error(response.data.message || '提交失败')
        }
      } catch (e) {
        console.error('提交失败详情:', e.response || e)
        error.value = '提交失败: ' + (e.response?.data?.message || e.message || '未知错误')
        alert(error.value)
      } finally {
        loading.value = false
      }
    }


    // 组件挂载时获取数据
    onMounted(async () => {
      if (fetchApplicantId()) {
        await fetchMentors() // fetchMentors 会自动调用 fetchExistingVolunteers
      }
    })

    return {
      mentorList,
      loading,
      error,
      isRankUsed,
      getSelectedMentorName,
      isValidSelection,
      submitVolunteer
    }
  }
}
</script>

<style scoped>
.content {
  padding: 20px;
  background-color: #f5f5f5;
  height: 100%;
}

.volunteer-selection {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

h2 {
  text-align: center;
  color: RGB(51, 132, 93);
  margin-bottom: 20px;
  font-size: 24px;
}

.loading, .error {
  text-align: center;
  padding: 20px;
  color: RGB(51, 132, 93);
}

.error {
  color: #ff4444;
}

.table-container {
  margin: 20px 0;
  overflow-x: auto;
}

.custom-table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 20px;
}

.custom-table th,
.custom-table td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #ddd;
}

.custom-table th {
  background-color: RGB(51, 132, 93);
  color: white;
}

.custom-table tr:hover {
  background-color: #f5f5f5;
}

.volunteer-select {
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  width: 120px;
}

.submit-section {
  text-align: center;
  margin: 20px 0;
}

.submit-button {
  background-color: RGB(51, 132, 93);
  color: white;
  padding: 10px 30px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
}

.submit-button:hover {
  background-color: RGB(41, 112, 73);
}

.submit-button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.selection-status {
  margin-top: 20px;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 4px;
}

.selection-status h3 {
  color: RGB(51, 132, 93);
  margin-bottom: 15px;
}

.status-container {
  display: grid;
  gap: 10px;
}

.status-item {
  display: flex;
  gap: 10px;
}

.status-label {
  font-weight: bold;
  color: RGB(51, 132, 93);
}
</style>