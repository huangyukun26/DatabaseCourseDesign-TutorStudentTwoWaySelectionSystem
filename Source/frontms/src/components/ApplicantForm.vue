<template>
  <div>
    <h2>提交个人资料</h2>
    <form @submit.prevent="submitForm">
      <div>
        <label>姓名：</label>
        <input type="text" v-model="form.name" required />
      </div>
      <div>
        <label>出生日期：</label>
        <input type="date" v-model="form.birth_date" required />
      </div>
      <div>
        <label>身份证号：</label>
        <input type="text" v-model="form.id_card_number" required />
      </div>
      <div>
        <label>籍贯：</label>
        <input type="text" v-model="form.origin" required />
      </div>
      <div>
        <label>本科专业：</label>
        <input type="text" v-model="form.undergraduate_major" required />
      </div>
      <div>
        <label>电子邮件：</label>
        <input type="email" v-model="form.email" required />
      </div>
      <div>
        <label>手机号：</label>
        <input type="text" v-model="form.phone" required />
      </div>
      <div>
        <label>本科院校：</label>
        <input type="text" v-model="form.undergraduate_school" required />
      </div>
      <div>
        <label>院校类型：</label>
        <input type="text" v-model="form.school_type" required />
      </div>
      <div>
        <label>简历：</label>
        <textarea v-model="form.resume" required></textarea>
      </div>
      <button type="submit">提交</button>
    </form>
    <p v-if="message">{{ message }}</p>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      form: {
        name: '',
        birth_date: '',
        id_card_number: '',
        origin: '',
        undergraduate_major: '',
        email: '',
        phone: '',
        undergraduate_school: '',
        school_type: '',
        resume: ''
      },
      message: ''
    };
  },
  methods: {
    async submitForm() {
      try {
        const response = await axios.post('http://localhost:8000/api/submit_applicant_info/', this.form);
        this.message = response.data.message;
      } catch (error) {
        this.message = "提交失败，请检查您的输入。";
      }
    }
  }
};
</script>

<style scoped>
form {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 5px;
  background-color: #f9f9f9;
}

h2 {
  text-align: center;
  color: #333;
}

div {
  margin-bottom: 15px;
}

label {
  display: block;
  font-weight: bold;
  margin-bottom: 5px;
  color: #555;
}

input[type="text"],
input[type="date"],
input[type="email"],
textarea {
  width: 100%;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
}

button {
  width: 100%;
  padding: 10px;
  background-color: #4CAF50;
  color: white;
  font-size: 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background-color: #45a049;
}

p {
  text-align: center;
  font-size: 14px;
  color: #f00;
}
</style>

