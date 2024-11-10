<template>
  <div class="mentor-info">
    <h2>导师基本信息</h2>
    
    <el-card class="info-card" v-if="mentorInfo">
      <template #header>
        <div class="card-header">
          <h3>{{ mentorInfo.basic_info.name }}</h3>
          <el-tag type="success">{{ mentorInfo.basic_info.title }}</el-tag>
        </div>
      </template>
      
      <div class="info-content">
        <el-descriptions :column="1" border>
          <el-descriptions-item label="导师编号">
            {{ mentorInfo.basic_info.mentor_id }}
          </el-descriptions-item>
          <el-descriptions-item label="联系邮箱">
            {{ mentorInfo.basic_info.email }}
          </el-descriptions-item>
          <el-descriptions-item label="联系电话">
            {{ mentorInfo.basic_info.phone }}
          </el-descriptions-item>
        </el-descriptions>

        <div class="bio-section">
          <h4>个人简介</h4>
          <p>{{ mentorInfo.basic_info.bio || '暂无简介' }}</p>
        </div>

        <div class="directions-section">
          <h4>研究方向</h4>
          <el-tag 
            v-for="direction in mentorInfo.research_directions" 
            :key="direction.direction_id"
            class="direction-tag"
            type="info">
            {{ direction.research_direction }}
          </el-tag>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { userService } from '@/services/userService'

export default {
  name: 'MentorBasicInfo',
  
  setup() {
    const mentorInfo = ref(null)
    
    const fetchMentorInfo = async () => {
      try {
        const mentorData = userService.getUserByType('mentor')
        if (!mentorData || !mentorData.userId) {
          ElMessage.error('未找到导师信息')
          return
        }
        
        const response = await fetch(`http://localhost:8000/api/mentor/basic-info/${mentorData.userId}/`, {
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
          mentorInfo.value = data.data
        } else {
          ElMessage.error(data.message || '获取数据失败')
        }
      } catch (error) {
        console.error('Error fetching mentor info:', error)
        ElMessage.error(`获取数据失败: ${error.message}`)
      }
    }
    
    onMounted(() => {
      fetchMentorInfo()
    })
    
    return {
      mentorInfo
    }
  }
}
</script>

<style scoped>
.mentor-info {
  padding: 20px;
  max-width: 100%;
  box-sizing: border-box;
}

.info-card {
  margin-top: 20px;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 16px;
}

.card-header h3 {
  margin: 0;
}

.info-content {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.bio-section,
.directions-section {
  margin-top: 20px;
}

.bio-section h4,
.directions-section h4 {
  margin-bottom: 12px;
  color: #303133;
}

.direction-tag {
  margin: 4px;
}

.bio-section p {
  line-height: 1.6;
  color: #606266;
}
</style> 