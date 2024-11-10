<template>
  <div class="all-applications">
    <h2>全院学生申请信息</h2>
    
    <el-table 
      :data="applications" 
      style="width: 100%" 
      :border="true"
      class="student-table">
      <!-- 基本信息 -->
      <el-table-column label="基本信息" min-width="200">
        <template #default="{ row }">
          <div class="student-info">
            <h4>{{ row.basic_info.name }}</h4>
            <p>学校: {{ row.basic_info.undergraduate_school }}</p>
            <p>专业: {{ row.basic_info.undergraduate_major }}</p>
          </div>
        </template>
      </el-table-column>

      <!-- 成绩信息 -->
      <el-table-column label="成绩信息" width="180">
        <template #default="{ row }">
          <div class="score-info" v-if="row.scores">
            <el-descriptions :column="1" border>
              <el-descriptions-item label="初试">{{ row.scores.preliminary_score }}</el-descriptions-item>
              <el-descriptions-item label="复试">{{ row.scores.final_score }}</el-descriptions-item>
              <el-descriptions-item label="总分">
                <span class="total-score">{{ row.scores.total_score }}</span>
              </el-descriptions-item>
            </el-descriptions>
          </div>
        </template>
      </el-table-column>

      <!-- 报考信息 -->
      <el-table-column label="报考信息" width="200">
        <template #default="{ row }">
          <div class="application-info" v-if="row.subject">
            <p>报考学科: {{ row.subject.parent_subject_name }}</p>
            <p v-if="row.subject.subject_name !== row.subject.parent_subject_name">
              研究方向: {{ row.subject.subject_name }}
            </p>
          </div>
        </template>
      </el-table-column>

      <!-- 志愿信息 -->
      <el-table-column label="志愿信息" min-width="250">
        <template #default="{ row }">
          <div class="application-info">
            <div v-for="app in row.applications" :key="app.preference_rank" class="volunteer-item">
              <p>第{{ app.preference_rank }}志愿: {{ app.mentor_name }} ({{ app.mentor_title }})</p>
              <div class="status-info">
                <el-tag :type="getStatusType(app.status)">{{ getStatusText(app.status) }}</el-tag>
                <p v-if="app.remarks" class="remarks">{{ app.remarks }}</p>
              </div>
              <el-divider v-if="app.preference_rank !== row.applications.length"/>
            </div>
          </div>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'

export default {
  name: 'MentorAllApplications',
  
  setup() {
    const applications = ref([])

    const fetchData = async () => {
      try {
        const response = await fetch('http://localhost:8000/api/mentor/all-applications/', {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json'
          },
          credentials: 'include'
        })

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`)
        }

        const data = await response.json()
        if (data.status === 'success') {
          applications.value = data.applications
        } else {
          ElMessage.error(data.message || '获取数据失败')
        }
      } catch (error) {
        console.error('Error fetching data:', error)
        ElMessage.error(`获取数据失败: ${error.message}`)
      }
    }

    const getStatusType = (status) => {
      switch (status) {
        case 'Accepted': return 'success'
        case 'Rejected': return 'danger'
        default: return 'info'
      }
    }

    const getStatusText = (status) => {
      switch (status) {
        case 'Accepted': return '已录取'
        case 'Rejected': return '已拒绝'
        default: return '待处理'
      }
    }

    onMounted(() => {
      fetchData()
    })

    return {
      applications,
      getStatusType,
      getStatusText
    }
  }
}
</script>

<style scoped>
.all-applications {
  padding: 20px;
}

.student-table {
  margin-top: 20px;
}

.student-info h4 {
  margin: 0 0 8px 0;
  color: #303133;
}

.student-info p {
  margin: 4px 0;
  color: #606266;
}

.score-info {
  text-align: center;
}

.total-score {
  color: #409EFF;
  font-weight: bold;
}

.application-info {
  color: #606266;
}

.volunteer-item {
  margin-bottom: 8px;
}

.status-info {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 4px;
  margin-top: 4px;
}

.remarks {
  font-size: 12px;
  color: #909399;
  margin: 4px 0;
}

.el-divider {
  margin: 8px 0;
}

.volunteer-item:last-child {
  margin-bottom: 0;
}
</style> 