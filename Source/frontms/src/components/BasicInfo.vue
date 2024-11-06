<template>
  <div class="basic-info">
    <h2>基本信息</h2>
    <div v-if="loading">
      <p>加载中...</p>
    </div>
    <div v-else-if="error">
      <p>{{ error }}</p>
    </div>
    <div v-else-if="applicant">
      <p><strong>姓名：</strong> {{ applicant.name }}</p>
      <p><strong>出生日期：</strong> {{ applicant.birth_date }}</p>
      <p><strong>身份证号：</strong> {{ applicant.id_card_number }}</p>
      <p><strong>生源地：</strong> {{ applicant.origin }}</p>
      <p><strong>本科专业：</strong> {{ applicant.undergraduate_major }}</p>
      <p><strong>邮箱：</strong> {{ applicant.email }}</p>
      <p><strong>电话：</strong> {{ applicant.phone }}</p>
      <p><strong>本科院校：</strong> {{ applicant.undergraduate_school }}</p>
      <p><strong>学校类型：</strong> {{ applicant.school_type }}</p>
      <p><strong>简历：</strong> {{ applicant.resume }}</p>
    </div>
  </div>
</template>

<script>
import { userService } from '@/services/userService';
import axios from 'axios';

export default {
  data() {
    return {
      applicant: null,
      loading: false,
      error: null
    };
  },
  
  created() {
    if (!userService.isAuthenticated()) {
      this.$router.push({ name: 'Login' });
      return;
    }
    this.getApplicantInfo();
  },

  methods: {
    async getApplicantInfo() {
      const applicantId = userService.getUserId();
      if (!applicantId) {
        this.error = '未找到考生ID，请重新登录';
        return;
      }

      try {
        this.loading = true;
        const response = await axios.get(`http://localhost:8000/api/applicants/${applicantId}/basic-info/`);
        this.applicant = response.data;
      } catch (error) {
        this.error = '获取考生信息失败';
        console.error(error);
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>

<style scoped>
.basic-info-container {
  padding: 20px;
  background-color: #fff;
  border: 1px solid #e4e7ed;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, .12), 0 0 6px rgba(0, 0, 0, .04);
}

h2 {
  color: RGB(51, 132, 93);
  font-size: 22px;
  font-weight: bold;
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 2px solid RGB(51, 132, 93);
}

.info-card {
  padding: 15px 0;
}

.info-card p {
  display: flex;
  align-items: center;
  font-size: 14px;
  line-height: 2;
  margin: 8px 0;
  padding: 8px 15px;
  background: #f5f7fa;
  border-radius: 4px;
}

.info-card p strong {
  color: #606266;
  width: 120px;
  text-align: right;
  margin-right: 15px;
}

</style>

