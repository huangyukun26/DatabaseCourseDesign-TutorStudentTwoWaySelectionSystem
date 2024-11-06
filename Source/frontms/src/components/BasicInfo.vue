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
  max-width: 800px;
  margin: 30px auto;
  padding: 30px;
  background-color: #ffffff;
  border-radius: 10px;
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  color: #444;
}

h2 {
  text-align: center;
  color: #333;
  margin-bottom: 25px;
  font-size: 26px;
  font-weight: bold;
}

.info-card {
  display: grid;
  grid-template-columns: 1fr;
  row-gap: 15px;
  padding: 15px;
}

.info-card p {
  font-size: 20px;
  line-height: 1.6;
  border-bottom: 1px solid #dcdcdc;
  padding: 8px 0;
}

.info-card p strong {
  color: #666;
}

p:last-child {
  border-bottom: none;
}

.navigation {
  font-size: 18px;
}
</style>

