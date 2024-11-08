<template>
  <div class="admission-plan">
    <h2 class="page-title">招生计划查看</h2>

    <div class="search-area">
      <el-select
        v-model="selectedFirstLevel"
        placeholder="一级学科："
        clearable
        @change="handleFirstLevelChange"
        class="search-item"
      >
        <el-option
          v-for="option in firstLevelOptions"
          :key="option.value"
          :label="option.label"
          :value="option.value"
        />
      </el-select>

      <el-select
        v-model="selectedSecondLevel"
        placeholder="二级学科："
        clearable
        class="search-item"
      >
        <el-option
          v-for="option in secondLevelOptions"
          :key="option.subject_id"
          :label="`${option.subject_id} - ${option.name}`"
          :value="option.subject_id"
        />
      </el-select>

      <el-input
        v-model="year"
        placeholder="年度："
        :disabled="true"
        class="search-item year-input"
      />

      <div class="button-group">
        <el-button type="primary" @click="handleSearch">查询</el-button>
        <el-button @click="handleReset">重置</el-button>
      </div>
    </div>

    <!-- 数据表格 -->
<el-table
  :data="tableData"
  style="width: 100%"
  border
  v-loading="loading"
  :row-key="(row) => row.id"
>
  <el-table-column prop="subject_id" label="学科" min-width="200">
    <template #default="scope">
      {{ scope.row.subject_id }} - {{ scope.row.subject_name }}
    </template>
  </el-table-column>
  <el-table-column prop="direction" label="研究方向" min-width="200" />
  <el-table-column prop="total_quota" label="年度招生指标" width="120" align="center" />
  <el-table-column prop="additional_quota" label="补充招生指标" width="120" align="center" />
  <el-table-column prop="year" label="年度" width="100" align="center">
    <template #default="scope">
      {{ scope.row.year }}年
    </template>
  </el-table-column>
</el-table>

    <!-- 分页 -->
    <div class="pagination-container">
      <el-pagination
        v-if="total > 0"
        :current-page="currentPage"
        :page-size="pageSize"
        :total="total"
        layout="total, prev, pager, next"
        @current-change="handlePageChange"
      />
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import { ElMessage } from 'element-plus'

const apiClient = axios.create({
  baseURL: 'http://127.0.0.1:8000/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  }
})

export default {
  name: 'AdmissionPlan',

  data() {
    return {
      subjects: [],
      firstLevelOptions: [],
      secondLevelOptions: [],
      selectedFirstLevel: '',
      selectedSecondLevel: '',
      year: new Date().getFullYear(),
      tableData: [],
      loading: false,
      total: 0,
      currentPage: 1,
      pageSize: 10,
    }
  },

  created() {
    this.fetchSubjects()
  },

  methods: {
    async fetchSubjects() {
      try {
        this.loading = true
        const response = await apiClient.get('/admission-catalogs/subjects/')
        if (response.data.status === 'success') {
          this.subjects = response.data.data
          this.firstLevelOptions = this.subjects.map(subject => ({
            value: subject.subject_id,
            label: `${subject.subject_id} - ${subject.name}`
          }))
        }
      } catch (error) {
        console.error('获取学科失败:', error)
        ElMessage.error('获取学科列表失败')
      } finally {
        this.loading = false
      }
    },

    handleFirstLevelChange(value) {
      this.selectedSecondLevel = ''
      if (!value) {
        this.secondLevelOptions = []
        return
      }

      const selectedSubject = this.subjects.find(s => s.subject_id === value)
      if (selectedSubject) {
        this.secondLevelOptions = selectedSubject.children || []
        if (this.secondLevelOptions.length === 1 &&
            this.secondLevelOptions[0].level === '一级') {
          this.selectedSecondLevel = this.secondLevelOptions[0].subject_id
        }
      }
    },

    async handleSearch() {
      if (!this.selectedFirstLevel) {
        ElMessage.warning('请选择一级学科')
        return
      }

      try {
        this.loading = true
        const params = {
          subject_id: this.selectedSecondLevel || this.selectedFirstLevel,
          year: this.year,
        }

        const response = await apiClient.get('/admission-catalogs/', { params })
        
        if (response.data) {
          this.tableData = response.data
          this.total = response.data.length
        }
      } catch (error) {
        console.error('查询失败:', error)
        ElMessage.error('查询失败')
        this.tableData = []
      } finally {
        this.loading = false
      }
    },

    handleReset() {
      this.selectedFirstLevel = ''
      this.selectedSecondLevel = ''
      this.secondLevelOptions = []
      this.currentPage = 1
      this.tableData = []
      this.total = 0
    },

    handlePageChange(page) {
      this.currentPage = page
      this.handleSearch()
    }
  }
}
</script>

<style scoped>
.admission-plan {
  padding: 20px;
}

.page-title {
  margin-bottom: 20px;
  color: #303133;
  font-size: 20px;
  font-weight: 500;
}

.search-area {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 20px;
  flex-wrap: wrap;
}

.search-item {
  width: 220px;
}

.year-input {
  width: 120px;
}

.button-group {
  display: flex;
  gap: 10px;
  margin-left: 10px;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}

@media screen and (max-width: 768px) {
  .search-area {
    flex-direction: column;
    align-items: stretch;
  }

  .search-item {
    width: 100%;
  }

  .button-group {
    margin-left: 0;
    justify-content: center;
  }
}

.el-table {
  :deep(td) {
    .cell {
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }
  }
}
</style>