<!---
<template>
  <div id="app">
    <StudentDashboard />
  </div>
</template>

<script>
import StudentDashboard from './components/StudentDashboard'

export default {
  components: {
    StudentDashboard
  }
}
</script>
--->
<template>
  <div id="app">
    <router-view />
  </div>
</template>

<script>
export default {
  name: "App",
};
</script>

<style>
body {
  margin: 0;
  font-family: Arial, sans-serif;
  background-color: #e8e8e8;
}
</style>


