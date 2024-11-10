<template>
  <div class="accepted-students">
    <h2>已录取学生列表</h2>

    <!-- 学生列表 -->
    <el-table :data="acceptedStudents"
              style="width: 100%"
              :border="true"
              class="student-table">
      <!-- 基本信息 -->
      <el-table-column label="基本信息" min-width="200">
        <template #default="{ row }">
          <div class="student-info">
            <h4>{{ row.name }}</h4>
            <p>学校: {{ row.undergraduate_school }}</p>
            <p>专业: {{ row.undergraduate_major }}</p>
          </div>
        </template>
      </el-table-column>

      <!-- 成绩信息 -->
      <el-table-column label="成绩信息" width="180">
        <template #default="{ row }">
          <div class="score-info">
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
          <div class="application-info">
            <p>志愿顺序: 第{{ row.preference_rank }}志愿</p>
            <el-divider></el-divider>
            <p>报考学科: {{ row.subject_name }}</p>
          </div>
        </template>
      </el-table-column>

      <!-- 录取状态 -->
      <el-table-column label="录取状态" width="150" align="center">
        <template #default="{ row }">
          <div class="status">
            <el-tag type="success">已录取</el-tag>
            <p class="remarks" v-if="row.remarks">
              备注: {{ row.remarks }}
            </p>
          </div>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { userService } from '@/services/userService'

export default {
  name: 'MentorAcceptedStudents',

  setup() {
    const acceptedStudents = ref([])
    const mentorId = ref(null)

    //获取数据的方法
    const fetchData = async () => {
      try {
        const mentorInfo = userService.getUserByType('mentor')
        if (!mentorInfo || !mentorInfo.userId) {
          ElMessage.error('未找到导师信息，请重新登录')
          return
        }

        mentorId.value = mentorInfo.userId
        const response = await fetch(`http://localhost:8000/api/mentor/${mentorId.value}/accepted-students/`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.cookie.match(/csrftoken=([\w-]+)/)?.[1] || ''
          },
          credentials: 'include'
        })

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`)
        }

        const data = await response.json()
        console.log('Received data:', data)

        if (data.status === 'success') {
          acceptedStudents.value = data.students || []
        } else {
          ElMessage.error(data.message || '获取数据失败')
        }
      } catch (error) {
        console.error('Error fetching data:', error)
        ElMessage.error(`获取数据失败: ${error.message}`)
      }
    }

    //格式化日期
    const formatDate = (dateString) => {
      const date = new Date(dateString)
      return date.toLocaleString('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
      })
    }

    onMounted(() => {
      fetchData()
    })

    return {
      acceptedStudents,
      formatDate
    }
  }
}
</script>

<style scoped>
.accepted-students {
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

.status {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.remarks {
  font-size: 12px;
  color: #909399;
  margin: 4px 0;
}

.el-divider {
  margin: 8px 0;
}
</style> 