<template>
  <div class="dashboard">
    <StudentNavbar /> <!-- 复用学生导航栏组件 -->
    <div class="main-content">
      <MentorSidebar />
      <div class="content">
        <template v-if="$route.path === '/mentor/dashboard'">
          <h1>欢迎来到北京林业大学研究生招生系统-导师端</h1>
          <div class="announcement">
          <h1>公告</h1>
          <h2>关于信息学院（人工智能学院）硕士研究生招生指标分配指导意见（试行）的通知</h2>
          <h3>第一章 总则</h3>
          <p>第一条 根据《北京林业大学研究生招生计划指标配置办法》（北林研发〔2020〕48 号）、《北京林业大学研究生指导教师招生资格年度审核管理办法》（北林研发〔2019〕 27 号，2020 年 6 月修订）等文件精神，为兼顾学科发展和人才培养需求，结合我院实际，特制定此文件。</p>
          <p>第二条 本文件适用于学院全日制学术型硕士学位和专业学位型硕士招生（不含联合培养学生）指标分配。非全日制和联合培养学生分配及导师选择学生办法参照本文件执行。</p>
          <h3>第二章 招生指标分配条件、原则和过程</h3>
          <p>第三条 学科和专业学位总体指标分配基本条件及原则。</p>
          <ol>
              <li>基本条件：学科或专业学位（以下统称学科）通过最近一次学位授权点合格性评估。</li>
              <li>围绕学院中长期事业学科建设发展规划，对于拟申请博士点的学科，在总体指标分配时予以适当增加。</li>
              <li>考虑各学科均衡发展需要，电子信息导师人均招生指标数和农业工程与信息技术的导师人均招生指标数差距不多于 1 人。</li>
          </ol>
          <p>第四条 各学科导师招生指标分配基本条件和主要过程。</p>
          <ol>
            <li>基本条件：参与学科招生指标分配的导师需通过年度导师资格审核且上一年校级导师立德树人考核结果为合格及以上。</li>
            <li>主要过程：各学科首先根据本文件第三章第六条确定学科内每位导师年度招生指标数，然后根据文件第四章第十条确定每位导师招收的具体学生信息。</li>
          </ol>
          <h3>第三章 各学科导师年度招生指标数计算</h3>
          <p>第五条 坚持均衡分配，兼顾发展，遵循民主集中制原则。</p>
          <p>第六条 各学科导师年度招生指标数组成：导师年度招生指标数=均分指标数+轮询指标数。</p>
          <p>第七条 各学科导师年度招生指标数方法：</p>
          <ol>
            <li>根据“均衡分配”原则，确定学科导师年度招生均分指标数。均分指标计算方法如下：</li>
            <li>根据“遵循民主集中制”和“兼顾发展”原则，轮询指标采取学科全体导师整体轮询排序为主方法确定。</li>
            <li>学科每位导师轮询指标数不超过 1 人，目录中新晋导师参与轮询顺序由学科全体导师共同商议确定。</li>
          </ol>
          <p>第八条 各学科导师年度招生指标数核增或核减参照学校有关文件规定执行。</p>

          <h3>第四章 各学科导师选择学生办法</h3>
          <p>第九条 各学科导师选择学生的原则和步骤：</p>
          <ol>
            <li>坚持学生志愿优先，师生双向选择，学科集中商议原则。</li>
            <li>主要步骤为学院下发招生信息，师生双向选择，学科集中商议决策。</li>
          </ol>
            <p>第十条 各学科需在研究生院发布拟录取通知后 30 天内完成导师选择学生，具体步骤为：</p>
          <ol>
            <li>导师选择学生：导师根据学生志愿和自身招生指标，从志愿选择导师的学生中选择符合条件的学生。选择过程应遵循公平、公正、公开的原则，确保每位导师的招生指标得到合理利用。</li>
            <li>学科集中商议：对于无法确定导师的学生，学科负责人应组织学科内导师进行集中商议，根据学生的综合情况和导师的意愿，确定最终的学生分配方案。</li>
            <li>确认与上报：导师在学生报名表上签字确认后，学院将确认的学生名单上报研究生院，完成导师选择学生的流程。</li>
          </ol>
          <h3>第五章 研究生招生信息公开或查阅</h3>
          <p>第十一条 研究生招生信息公开或查阅事项在满足教育部和国家保密局发布的《教育工作中国家秘密及其秘密具体范围的规定》(教密〔2002〕2 号)和教育部当年《全国硕士研究生招生工作管理规定》文件要求基础上，结合学校和学院研究生招生工作要求，在规定范围公开或查阅。</p>
          <p>第十二条 信息公开或查阅范围：</p>
          <ol>
              <li>学院研究生教学管理办公室根据教育部当年《全国硕士研究生招生工作管理规定》公布复试工作方案、推免学生复试成绩、复试学生的初试成绩、复试学生的复试成绩。</li>
              <li>各学科复试专业测试命题组组长可根据成绩复核需要，在学院规定场地查阅专业测试试卷命题和评阅情况。</li>
              <li>学科负责人在轮询指标数分配过程中，公示学科各导师近三年招生数量。</li>
              <li>学科负责人或学科秘书根据学生报考志愿情况，向学生报考志愿的导师，公布学生的初试、复试各科目成绩和学生源学历信息（原单位、专业）等信息。</li>
              <li>学科完成导师选择学生工作后，学院公示各学科导师招生人数信息。</li>
          </ol>
          <h3>第六章 附则</h3>
          <p>第十三条 该文件由学院研究生教学管理办公室负责解释。经学院党委会会议、学院党政联席会按程序审议后，自公布之日起开始实施本文件试行一年，可根据实际情况做必要修订。</p>
          <p>第十四条 文件未尽事宜由学院研究生招生工作领导小组和学科负责人联席会议讨论并形成意见，学院党政联席会审议并形成决议。</p>

              </div>
        </template>
        <router-view v-else />
      </div>
    </div>
  </div>
</template>

<script>
import StudentNavbar from "@/components/StudentNavbar.vue";
import MentorSidebar from "@/components/MentorSidebar.vue";

export default {
  components: {
    StudentNavbar,
    MentorSidebar,
  }
}
</script>

<style scoped>
.dashboard {
  display: flex;
  flex-direction: column;
  height: 100vh;
}

.main-content {
  display: flex;
  flex: 1;
}

.content {
  flex: 1;
  padding: 20px;
  background-color: white;
}


.announcement {
  margin-top: 20px;
  padding: 10px;
  padding-left: 30px;
  background-color: #f5f5f5;
  border: 1px solid #ccc;
  border-radius: 5px;
  max-height: 800px;
  overflow-y: auto;
}

.announcement h1 {
  text-align: center;
  font-size: 25px;
}

.announcement h2 {
  text-align: center;
  margin-top: 0;
  color: #333;
  font-size: 22px;
  font-weight: bold;
}

.announcement h3 {
  text-align: center;
  margin-top: 10px;
  color: #333;
  font-size: 20px;
  font-weight: bold;
}

.announcement p {;
  line-height: 1.6;
  margin-bottom: 5px;
  font-weight: 550;
}

.announcement ol, .announcement ul {
  color: #666;
  margin-left: 20px;
}

.announcement li {
  color: #666;
  margin-bottom: 5px;
}
</style>