<template>
  <div class="content">
   <div class="query-container">
    <div class="title">
      <h2>录取状态查询</h2>
    </div>

    <div v-if="loading" class="loading">
      <p>加载中...</p>
    </div>
    <div v-else-if="error" class="error">
      <p>{{ error }}</p>
    </div>
    <div v-else class="status-container">
      <!-- 总体状态卡片 -->
      <div class="status-overview">
        <div class="status-card" :class="overallStatusClass">
          <div class="status-header">总体录取状态</div>
          <div class="status-content">{{ getOverallStatusText }}</div>
        </div>
      </div>

      <!-- 志愿状态列表 -->
      <div class="preference-list">
        <div class="section-title">志愿详情</div>
        <el-table
          :data="admissionInfo.preferences"
          style="width: 100%"
          :header-cell-style="{ background: '#f5f7fa' }"
        >
          <el-table-column prop="rank" label="志愿" width="80">
            <template #default="scope">
              第{{ scope.row.rank }}志愿
            </template>
          </el-table-column>
          
          <el-table-column prop="mentor_name" label="导师姓名" width="120">
            <template #default="scope">
              {{ scope.row.mentor_name }}
            </template>
          </el-table-column>
          
          <el-table-column prop="mentor_title" label="职称" width="100">
            <template #default="scope">
              {{ scope.row.mentor_title }}
            </template>
          </el-table-column>
          
          <el-table-column prop="status" label="状态" width="100">
            <template #default="scope">
              <el-tag :type="getStatusType(scope.row.status)">
                {{ getStatusText(scope.row.status) }}
              </el-tag>
            </template>
          </el-table-column>
          
          <el-table-column prop="remarks" label="备注">
            <template #default="scope">
              {{ scope.row.remarks || '暂无备注' }}
            </template>
          </el-table-column>
        </el-table>
      </div>
    </div>
   </div>
  </div>
</template>

<script>
import { userService } from '@/services/userService';

export default {
  data() {
    return {
      admissionInfo: null,
      loading: false,
      error: null
    };
  },

  computed: {
    overallStatusClass() {
      if (!this.admissionInfo) return '';
      const status = this.admissionInfo.overall_status;
      return `status-${status}`;
    },

    getOverallStatusText() {
      if (!this.admissionInfo) return '暂无信息';
      return this.admissionInfo.overall_status;
    }
  },

  methods: {
    async fetchAdmissionStatus() {
      const studentUser = userService.getUserByType('student');
      const applicantId = studentUser?.applicant_id;
      
      if (!applicantId) {
        this.error = '请先登录';
        return;
      }

      try {
        this.loading = true;
        const response = await fetch(
          `http://localhost:8000/api/admission/status/${applicantId}`
        );
        const data = await response.json();

        if (response.ok) {
          this.admissionInfo = data;
          this.error = null;
        } else {
          this.error = data.message || '获取录取状态失败';
        }
      } catch (error) {
        console.error('获取录取状态失败:', error);
        this.error = '网络错误，请稍后重试';
      } finally {
        this.loading = false;
      }
    },

    getStatusText(status) {
      const statusMap = {
        'Pending': '待定',
        'Accepted': '已录取',
        'Rejected': '未录取'
      };
      return statusMap[status] || status;
    },

    getStatusType(status) {
      const typeMap = {
        'Pending': 'info',
        'Accepted': 'success',
        'Rejected': 'danger'
      };
      return typeMap[status] || 'info';
    }
  },

  created() {
    this.fetchAdmissionStatus();
  }
};
</script>

<style scoped>
.content {
  padding: 20px;
  background-color: #f5f5f5;
  height: 100%;
}

.query-container {
  background-color: #fff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);


}

.title {
  margin-top: 20px;
  margin-bottom: 20px;
}

.title h2 {
  text-align: center;
  color: RGB(51, 132, 93);
  font-size: 24px;
  margin: 0;
  font-weight: bold;
}

.status-container {
  background-color: #fff;
  border-radius: 4px;
}

.status-overview {
  margin-bottom: 30px;
}

.status-card {
  padding: 20px;
  border-radius: 4px;
  text-align: center;
}

.status-header {
  font-size: 16px;
  color: #666;
  margin-bottom: 10px;
}

.status-content {
  font-size: 24px;
  font-weight: bold;
}

.status-已录取 {
  background-color: #f0f9eb;
  color: #67c23a;
}

.status-未录取 {
  background-color: #fef0f0;
  color: #f56c6c;
}

.status-待定 {
  background-color: #f4f4f5;
  color: #909399;
}

.section-title {
  font-size: 16px;
  color: #333;
  margin: 20px 0;
  padding-left: 10px;
  border-left: 4px solid RGB(51, 132, 93);
}

.preference-list {
  margin-top: 20px;
}

.loading, .error {
  text-align: center;
  padding: 40px;
  color: #666;
}

.error {
  color: #f56c6c;
}


:deep(.el-table) {
  --el-table-border-color: #ebeef5;
  --el-table-header-background-color: #f5f7fa;
}

:deep(.el-table th) {
  background-color: #f5f7fa !important;
}
</style>