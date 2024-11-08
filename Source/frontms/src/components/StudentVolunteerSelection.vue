<template>
  <div class="content">
    <div class="volunteer-selection">
      <h2>志愿填报</h2>
      
      <div v-if="loading" class="loading">加载中...</div>
      <div v-if="error" class="error-message">{{ error }}</div>

      <!-- 已提交志愿的显示 -->
      <div v-if="hasSubmitted" class="submitted-volunteers">
        <h3>已提交志愿（不可更改）</h3>
        <div class="info-card">
          <table class="custom-table">
            <thead>
              <tr>
                <th>志愿顺序</th>
                <th>导师姓名</th>
                <th>职称</th>
                <th>研究方向</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="volunteer in submittedVolunteers" :key="volunteer.mentor_id">
                <td>第{{ volunteer.rank }}志愿</td>
                <td>{{ volunteer.name }}</td>
                <td>{{ volunteer.title }}</td>
                <td>{{ volunteer.research_direction }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- 未提交时的选择界面 -->
      <div v-else-if="!loading && !error && !hasSubmitted && subjectData" class="selection-container">
        <!-- 学科信息显示 -->
        <div class="subject-info">
          <h3>报考学科信息</h3>
          <div class="info-card">
            <p><strong>主报学科：</strong>{{ subjectData.main_subject?.name }}</p>
            <p><strong>学科类型：</strong>{{ subjectData.main_subject?.type }}</p>
          </div>
        </div>

        <!-- 研究方向选择 -->
        <div v-if="subjectData.has_sub_subjects && subjectData.sub_subjects?.length > 0" class="sub-subject-selection">
          <h3>选择研究方向</h3>
          <div class="sub-subjects-grid">
            <div 
              v-for="sub in subjectData.sub_subjects" 
              :key="sub.id"
              class="sub-subject-card"
              :class="{ active: selectedSubSubject?.id === sub.id }"
              @click="selectSubSubject(sub)"
            >
              <h4>{{ sub.name }}</h4>
              <p>导师数量: {{ sub.mentors?.length || 0 }}</p>
            </div>
          </div>
        </div>

        <!-- 导师列表 -->
        <div v-if="displayedMentors.length > 0" class="mentors-section">
          <h3>可选导师</h3>
          <div class="table-container">
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
                <tr v-for="mentor in displayedMentors" :key="mentor.mentor_id">
                  <td>{{ mentor.name }}</td>
                  <td>{{ mentor.title }}</td>
                  <td>{{ mentor.research_direction }}</td>
                  <td>
                    <select 
                      v-model="mentorRanks[mentor.mentor_id]"
                      :disabled="isRankDisabled(mentor.mentor_id)"
                      @change="handleRankChange(mentor.mentor_id)"
                    >
                      <option value="">未选择</option>
                      <option 
                        v-for="n in 3" 
                        :key="n" 
                        :value="n"
                        :disabled="isRankTaken(n, mentor.mentor_id)"
                      >
                        第{{ n }}志愿
                      </option>
                    </select>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
        
        <div v-else-if="subjectData.has_sub_subjects && !selectedSubSubject" class="no-mentors-message">
          请选择研究方向查看导师
        </div>
        <div v-else-if="selectedSubSubject" class="no-mentors-message">
          该研究方向暂无可选导师
        </div>

        <!-- 提交按钮 -->
        <div class="submit-section" v-if="hasSelectedMentors">
          <el-button type="primary" @click="submitVolunteers" :loading="submitting">
            提交志愿
          </el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import axios from 'axios'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'

const store = useStore()
const router = useRouter()

// 获取当前登录的考生ID
const currentApplicantId = computed(() => {
  // 先从 Vuex 获取
  const storeId = store.state.applicantId
  if (storeId) return storeId
  
  // 如果 Vuex 没有，从 localStorage 获取
  try {
    const savedState = localStorage.getItem('vuex-state')
    if (savedState) {
      const state = JSON.parse(savedState)
      if (state.applicantId) {
        // 恢复 Vuex 状态
        store.dispatch('loginUser', {
          applicantId: state.applicantId,
          userInfo: state.user
        })
        return state.applicantId
      }
    }
  } catch (e) {
    console.error('Error reading from localStorage:', e)
  }
  
  return null
})

// 检查登录状态
const checkAuth = () => {
  if (!currentApplicantId.value) {
    ElMessage.error('请先登录')
    router.push('/login')
    return false
  }
  return true
}

const loading = ref(false)
const error = ref('')
const subjectData = ref(null)
const selectedSubSubject = ref(null)
const mentorRanks = ref({})
const submitting = ref(false)

// 添加新的状态
const hasSubmitted = ref(false)
const submittedVolunteers = ref([])

// 设置 axios 默认配置
axios.defaults.baseURL = 'http://localhost:8000'  // 确保这是你的后端地址

// 获取导师信息
const fetchSubjectMentors = async () => {
  try {
    loading.value = true
    error.value = ''
    
    const response = await axios.get(`/api/subject/mentors/${currentApplicantId.value}/`)
    console.log('API Response:', response.data)
    
    if (response.data.status === 'success') {
      subjectData.value = response.data.data
      
      // 如果有数据，打印出来看看结构
      if (subjectData.value) {
        console.log('Subject Data:', {
          mainSubject: subjectData.value.main_subject,
          hasSubSubjects: subjectData.value.has_sub_subjects,
          subSubjectsCount: subjectData.value.sub_subjects?.length,
          mentorsCount: subjectData.value.mentors?.length
        })
      }
    } else {
      throw new Error(response.data.message || '获取数据失败')
    }
  } catch (e) {
    console.error('Error details:', e)
    error.value = '获取数据失败: ' + (e.response?.data?.message || e.message)
  } finally {
    loading.value = false
  }
}

// 计算属性：显示的导师列表
const displayedMentors = computed(() => {
  if (!subjectData.value) return []
  
  if (subjectData.value.has_sub_subjects) {
    return selectedSubSubject.value?.mentors || []
  }
  
  return subjectData.value.mentors || []
})

// 选择研究方向
const selectSubSubject = (sub) => {
  console.log('Selecting sub subject:', sub)
  selectedSubSubject.value = sub
  mentorRanks.value = {} // 清空已选志愿
}

// 检查志愿顺序是否被占用
const isRankTaken = (rank, currentMentorId) => {
  return Object.entries(mentorRanks.value).some(([mentorId, value]) => {
    return value === rank && parseInt(mentorId) !== currentMentorId
  })
}

// 检查是否应该禁用志愿选择
const isRankDisabled = (mentorId) => {
  if (mentorRanks.value[mentorId]) return false
  const selectedCount = Object.values(mentorRanks.value).filter(Boolean).length
  return selectedCount >= 3
}

// 处理志愿顺序变化
const handleRankChange = (mentorId) => {
  if (!mentorRanks.value[mentorId]) {
    delete mentorRanks.value[mentorId]
  }
}

// 计算是否有选择的导师
const hasSelectedMentors = computed(() => {
  return Object.values(mentorRanks.value).some(rank => rank !== '')
})

// 获取已提交的志愿信息
const fetchSubmittedVolunteers = async () => {
  try {
    console.log('Fetching volunteers for applicant:', currentApplicantId.value)
    const response = await axios.get(`/api/applicant/volunteers/${currentApplicantId.value}/`)
    console.log('Submitted volunteers response:', response.data)
    
    if (response.data.status === 'success' && response.data.data) {
      const volunteers = response.data.data
      console.log('Received volunteers:', volunteers)
      
      // 检查是否有志愿数据
      if (Array.isArray(volunteers) && volunteers.length > 0) {
        hasSubmitted.value = true
        // 确保每个志愿对象包含所需的所有字段
        submittedVolunteers.value = volunteers
          .map(v => ({
            mentor_id: v.mentor_id,
            name: v.name || v.mentor_name, // 兼容不同的字段名
            title: v.title || v.mentor_title,
            research_direction: v.research_direction || v.direction,
            rank: v.rank
          }))
          .sort((a, b) => a.rank - b.rank)
        
        console.log('Processed submitted volunteers:', submittedVolunteers.value)
        return true // 表示有提交的志愿
      } else {
        console.log('No submitted volunteers found')
        hasSubmitted.value = false
        submittedVolunteers.value = []
        return false // 表示没有提交的志愿
      }
    } else {
      console.log('Invalid response format or no data')
      hasSubmitted.value = false
      submittedVolunteers.value = []
      return false
    }
  } catch (e) {
    console.error('Error fetching submitted volunteers:', e)
    error.value = '获取已提交志愿信息失败'
    return false
  }
}

// 修改提交志愿的函数
const submitVolunteers = async () => {
  if (!currentApplicantId.value) {
    ElMessage.error('请先登录')
    return
  }

  try {
    submitting.value = true
    
    const volunteers = Object.entries(mentorRanks.value)
      .map(([mentorId, rank]) => ({
        mentor_id: parseInt(mentorId),
        rank: parseInt(rank)
      }))
      .sort((a, b) => a.rank - b.rank)

    if (volunteers.length === 0) {
      ElMessage.warning('请至少选择一个志愿')
      return
    }

    const response = await axios.post('/api/volunteer/submit/', {
      applicant_id: currentApplicantId.value,
      volunteers: volunteers
    })

    if (response.data.status === 'success') {
      ElMessage.success('志愿提交成功')
      hasSubmitted.value = true
      submittedVolunteers.value = volunteers
      await fetchSubmittedVolunteers() // 重新获取最新的提交信息
    } else {
      throw new Error(response.data.message || '提交失败')
    }
  } catch (e) {
    console.error('Submit error:', e)
    ElMessage.error('提交失败: ' + (e.response?.data?.message || e.message))
  } finally {
    submitting.value = false
  }
}

// 修改初始化逻辑
const initialize = async () => {
  if (!checkAuth()) return
  
  try {
    loading.value = true
    error.value = ''
    
    // 先获取已提交信息
    const hasSubmittedData = await fetchSubmittedVolunteers()
    console.log('Has submitted data:', hasSubmittedData)
    
    // 只有在确认没有提交过志愿时才获取可选导师
    if (!hasSubmittedData) {
      console.log('Fetching available mentors...')
      await fetchSubjectMentors()
    } else {
      console.log('Already submitted, skipping mentor fetch')
    }
  } catch (e) {
    console.error('Initialization error:', e)
    error.value = '始化失败'
  } finally {
    loading.value = false
  }
}

// 使用 onMounted 钩子进行初始化
onMounted(() => {
  initialize()
})
</script>

<style scoped>
.content {
  padding: 20px;
  background-color: #f5f5f5;
}

.volunteer-selection {
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
}

/* 已提交志愿的样式 */
.submitted-volunteers {
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  margin-top: 20px;
}

.submitted-volunteers .info-card {
  background-color: white;
  padding: 20px;
  border-radius: 6px;
}

/* 导师选择部分 */
.selection-container {
  display: grid;
  gap: 25px;
}

.subject-info, .sub-subject-selection, .mentors-section {
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.info-card {
  background-color: white;
  padding: 20px;
  border-radius: 6px;
}

.sub-subjects-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin-top: 15px;
}

.sub-subject-card {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  cursor: pointer;
  transition: transform 0.2s;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.sub-subject-card:hover {
  transform: translateY(-2px);
}

.sub-subject-card.active {
  background-color: RGB(51, 132, 93);
  color: white;
}

.custom-table {
  width: 100%;
  border-collapse: collapse;
  background-color: white;
  border-radius: 6px;
  overflow: hidden;
}

.custom-table th,
.custom-table td {
  padding: 15px;
  text-align: left;
  border-bottom: 1px solid #ebeef5;
}

.custom-table th {
  background-color: #f9f9f9;
  color: RGB(51, 132, 93);
  font-weight: bold;
}

.no-mentors-message {
  text-align: center;
  padding: 60px;
  color: #666;
  font-size: 16px;
  background-color: #f9f9f9;
  border-radius: 8px;
}

.submit-section {
  margin-top: 30px;
  text-align: center;
}

select {
  padding: 8px 12px;
  border-radius: 6px;
  border: 1px solid #dcdfe6;
  background-color: white;
  color: #333;
  transition: border-color 0.2s;
}

select:hover {
  border-color: RGB(51, 132, 93);
}

select:disabled {
  background-color: #f5f7fa;
  cursor: not-allowed;
  opacity: 0.7;
}

@media (max-width: 768px) {
  .sub-subjects-grid {
    grid-template-columns: 1fr;
  }
  
  .custom-table {
    display: block;
    overflow-x: auto;
  }
}
</style>