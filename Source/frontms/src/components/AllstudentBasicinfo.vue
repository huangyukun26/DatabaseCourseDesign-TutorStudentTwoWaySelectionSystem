<template>
  <div class="all-student-basic-info">
    <h2>本学科所有学生的基本信息</h2>
    <div v-if="loading">
      <p>加载中...</p>
    </div>
    <div v-else-if="error">
      <p>{{ error }}</p>
    </div>
    <div v-else>
      <ul>
        <li v-for="student in students" :key="student.id">
          <router-link :to="{ name: 'StudentInfo', params: { id: student.id } }">
            <p><strong>姓名：</strong>{{ student.name }}</p>
            <p><strong>初试成绩：</strong>{{ student.applicantScore.first_exam_score }}</p>
            <p><strong>复试成绩：</strong>{{ student.applicantScore.second_exam_score }}</p>
            <button @click="viewStudentInfo(student.applicant_id)">查看详情</button>
          </router-link>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { userService } from '@/services/userService';

export default {
  data() {
    return {
      students: [],
      loading: false,
      error: null
    };
  },

  created() {
    this.getStudentList();
  },

  methods: {
    async getStudentList() {
      const subjectId = userService.getCurrentUserSubjectId();
      if (!subjectId) {
        this.error = '未找到学科ID';
        return;
      }

      try {
        this.loading = true;
        const response = await axios.get(`http://localhost:8000/api/students/subject/${subjectId}/`);
        this.students = response.data;
      } catch (error) {
        this.error = '获取学生信息失败';
        console.error(error);
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>

<style scoped>
.student-list {
  /* 样式代码 */
}
</style>
