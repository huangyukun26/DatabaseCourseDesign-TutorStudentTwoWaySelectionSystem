<!-- BasicInfo.vue -->
<template>
  <div class="navigation">主页 -> 基本信息</div>
  <div class="basic-info">
    <h2>基本信息</h2>
    <div v-if="applicant">
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
    <div v-else>
      <p>加载中...</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      applicant: null
    };
  },
  created() {
    const applicantId = localStorage.getItem('applicant_id');
    console.log('Applicant ID:', applicantId);  // 输出 applicantId
    if (!applicantId) {
      console.error("Applicant ID 未找到，请确保已成功登录并存储 applicant_id。");
      return;
    }

    this.fetchApplicantInfo(applicantId);
  },
methods: {
  async fetchApplicantInfo(applicantId) {
    try {
      const response = await axios.get(`http://localhost:8000/api/applicants/${applicantId}/basic-info/`);
      this.applicant = response.data;
    } catch (error) {
      console.error("获取考生信息失败:", error);
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

.navigation {
  font-size: 14px;
  color: #606266;
}
</style>

