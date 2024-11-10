<template>
  <div class="student-list">
    <h2>学生申请列表</h2>

    <!-- 总配额信息展示 -->
    <div class="quota-info" v-if="quotaInfo">
      <h3>总体招生配额</h3>
      <el-card class="overall-quota">
        <p>总配额: {{ quotaInfo.overall.total_quota }} |
           已使用: {{ quotaInfo.overall.used_quota }} |
           剩余: {{ quotaInfo.overall.remaining_quota }}</p>
      </el-card>

      <!-- 分学科配额信息 -->
      <h3>分学科招生配额</h3>
      <el-card v-for="(subject, subjectId) in quotaInfo.by_subject"
               :key="subjectId"
               class="subject-quota">
        <template #header>
          <div class="subject-header">
            <span>{{ subject.subject_name }}</span>
            <el-tag type="info">
              剩余名额: {{ subject.remaining_quota }}
            </el-tag>
          </div>
        </template>

        <!-- 二级学科配额 -->
        <div v-if="Object.keys(subject.sub_subjects).length > 0"
             class="sub-subjects">
          <div v-for="(subSubject, subId) in subject.sub_subjects"
               :key="subId"
               class="sub-subject-item">
            <span>{{ subSubject.subject_name }}</span>
            <div class="quota-numbers">
              <el-tag size="small" type="success">总额: {{ subSubject.total_quota }}</el-tag>
              <el-tag size="small" type="warning">已用: {{ subSubject.used_quota }}</el-tag>
              <el-tag size="small" type="info">剩余: {{ subSubject.remaining_quota }}</el-tag>
            </div>
          </div>
        </div>
      </el-card>
    </div>

    <!-- 学生列表 -->
    <el-table :data="studentList"
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

      <!-- 状态和操作 -->
      <el-table-column label="状态/操作" width="150" align="center">
        <template #default="{ row }">
          <div class="status-actions">
            <!-- 先检查是否有更高优先级志愿被接受 -->
            <template v-if="row.higher_preference_status === 'Accepted'">
              <el-tag type="info">已被高志愿导师录取</el-tag>
            </template>
            <!-- 再检查是否已接受 -->
            <template v-else-if="row.status === 'Accepted'">
              <el-tag type="success">已接受</el-tag>
            </template>
            <!-- 再检查是否是主动拒绝 -->
            <template v-else-if="row.status === 'Rejected'">
              <el-tag type="danger">已拒绝</el-tag>
            </template>
            <!-- 最后是待处理状态 -->
            <template v-else>
              <el-button-group>
                <el-button
                  type="primary"
                  size="small"
                  @click="handleAccept(row)"
                  :disabled="!canAcceptStudent(row)"
                >
                  接受
                </el-button>
                <el-button
                  type="danger"
                  size="small"
                  @click="handleReject(row)"
                >
                  拒绝
                </el-button>
              </el-button-group>
            </template>
          </div>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { userService } from '@/services/userService'

export default {
  name: 'MentorStudentList',

  setup() {
    const studentList = ref([])
    const quotaInfo = ref(null)
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
        const response = await fetch(`http://localhost:8000/api/mentor/${mentorId.value}/students/`, {
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
        console.log('Student list:', data.students)

        if (data.status === 'success') {
          studentList.value = data.students || []
          
          quotaInfo.value = {
            overall: {
              total_quota: 0,
              used_quota: 0,
              remaining_quota: 0
            },
            by_subject: {}
          }
          
          if (data.quota_info) {
            quotaInfo.value = {
              ...quotaInfo.value,
              ...data.quota_info
            }
          }
        } else {
          ElMessage.error(data.message || '获取数据失败')
        }
      } catch (error) {
        console.error('Error fetching data:', error)
        ElMessage.error(`获取数据失败: ${error.message}`)
      }
    }

    //修改检查高优先级志愿状态的方法
    const hasHigherPreferenceAccepted = (studentData) => {
      try {
        return studentData.higher_preference_status === 'Accepted'
      } catch (error) {
        console.error('Error in hasHigherPreferenceAccepted:', error)
        return false
      }
    }

    //修改检查是否可以接受学生的方法
    const canAcceptStudent = (studentData) => {
      try {
        //如果有更高优先级志愿已被接受，不能接受
        if (hasHigherPreferenceAccepted(studentData)) {
          return false
        }

        //如果当前申请已被接受，不能再接受
        if (studentData.status === 'Accepted') {
          return false
        }

        //检查配额
        if (!quotaInfo.value) {
          console.warn('No quota info available')
          return false
        }

        //检查总体配额
        if (quotaInfo.value.overall.remaining_quota <= 0) {
          return false
        }

        //如果有学科特定配额，则检查
        const parentSubjectId = studentData.parent_subject_id
        if (parentSubjectId && quotaInfo.value.by_subject) {
          const parentQuota = quotaInfo.value.by_subject[parentSubjectId]
          if (parentQuota && parentQuota.remaining_quota <= 0) {
            return false
          }
        }

        return true
      } catch (error) {
        console.error('Error in canAcceptStudent:', error)
        return false
      }
    }

    //处理接受学生
    const handleAccept = async (studentData) => {
      try {
        await ElMessageBox.confirm('确定接受该学生吗？', '确认操作', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        })

        const response = await fetch(`http://localhost:8000/api/mentor/${mentorId.value}/process-application/`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.cookie.match(/csrftoken=([\w-]+)/)?.[1] || ''
          },
          body: JSON.stringify({
            applicant_id: studentData.applicant_id,
            action: 'Accepted'
          }),
          credentials: 'include'
        })

        const data = await response.json()
        if (data.status === 'success') {
          ElMessage.success('已接受该学生')
          await fetchData()  //重新获取最新数据
        } else {
          ElMessage.error(data.message || '操作失败')
        }
      } catch (error) {
        if (error !== 'cancel') {
          console.error('Error accepting student:', error)
          ElMessage.error('操作失败')
        }
      }
    }

    //处理拒绝学生
    const handleReject = async (studentData) => {
      try {
        await ElMessageBox.confirm('确定拒绝该学生吗？', '确认操作', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        })

        const response = await fetch(`http://localhost:8000/api/mentor/${mentorId.value}/process-application/`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.cookie.match(/csrftoken=([\w-]+)/)?.[1] || ''
          },
          body: JSON.stringify({
            applicant_id: studentData.applicant_id,
            action: 'Rejected',
            rejection_reason: 'manual'
          }),
          credentials: 'include'
        })

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`)
        }

        const data = await response.json()
        if (data.status === 'success') {
          ElMessage.success('已拒绝该学生')
          await fetchData()  //重新获取最新数据
        } else {
          ElMessage.error(data.message || '操作失败')
        }
      } catch (error) {
        if (error !== 'cancel') {
          console.error('Error rejecting student:', error)
          ElMessage.error(`操作失败: ${error.message}`)
        }
      }
    }

    onMounted(() => {
      fetchData()
    })

    return {
      studentList,
      quotaInfo,
      canAcceptStudent,
      hasHigherPreferenceAccepted,  //导出新方法
      handleAccept,
      handleReject
    }
  }
}
</script>

<style scoped>
.student-list {
  padding: 20px;
}

.quota-info {
  margin-bottom: 30px;
}

.overall-quota {
  margin-bottom: 20px;
}

.subject-quota {
  margin-bottom: 15px;
}

.subject-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.sub-subjects {
  margin-top: 10px;
}

.sub-subject-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 0;
  border-bottom: 1px solid #ebeef5;
}

.sub-subject-item:last-child {
  border-bottom: none;
}

.quota-numbers {
  display: flex;
  gap: 8px;
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

.status-actions {
  display: flex;
  flex-direction: column;
  gap: 8px;
  align-items: center;
}

.el-divider {
  margin: 8px 0;
}

.status-actions .el-tag {
  margin: 4px 0;
}
</style>