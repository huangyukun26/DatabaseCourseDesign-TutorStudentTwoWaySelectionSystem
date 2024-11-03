from django.db import models

#SUBJECT 表
class Subject(models.Model):
    subject_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, verbose_name="学科名称")
    level = models.CharField(max_length=50, verbose_name="学科等级")
    parent_subject = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, verbose_name="上级学科ID")
    description = models.TextField(blank=True, verbose_name="学科描述")
    type = models.CharField(max_length=50, verbose_name="学科类型")

    def __str__(self):
        return self.name


#MENTOR 表
class Mentor(models.Model):
    mentor_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, verbose_name="导师姓名")
    title = models.CharField(max_length=100, verbose_name="导师职称")
    photo = models.ImageField(upload_to='photos/', null=True, blank=True, verbose_name="导师照片")
    bio = models.TextField(blank=True, verbose_name="导师简介")
    email = models.EmailField(verbose_name="导师邮箱")
    phone = models.CharField(max_length=20, verbose_name="导师电话")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name="学科ID")

    def __str__(self):
        return self.name


#APPLICANT 表
class Applicant(models.Model):
    applicant_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, verbose_name="考生姓名")
    birth_date = models.DateField(verbose_name="考生出生日期")
    id_card_number = models.CharField(max_length=20, unique=True, verbose_name="考生身份证号")
    origin = models.CharField(max_length=255, verbose_name="考生生源地")
    undergraduate_major = models.CharField(max_length=100, verbose_name="考生本科专业")
    email = models.EmailField(verbose_name="考生邮箱")
    phone = models.CharField(max_length=20, verbose_name="考生电话")
    undergraduate_school = models.CharField(max_length=255, verbose_name="本科院校")
    school_type = models.CharField(max_length=50, verbose_name="本科学校类型")
    resume = models.TextField(blank=True, verbose_name="志愿选择")

    def __str__(self):
        return self.name


#ADMISSION_CATALOG 表
class AdmissionCatalog(models.Model):
    catalog_id = models.AutoField(primary_key=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name="学科ID")
    direction_id = models.IntegerField(verbose_name="研究方向编号")
    total_quota = models.IntegerField(verbose_name="年度招生指标")
    additional_quota = models.IntegerField(verbose_name="补充招生指标")
    year = models.IntegerField(verbose_name="招生年度")

    def __str__(self):
        return f"{self.subject.name} - {self.year}"


#MENTOR_CATALOG_ASSIGNMENT 表
class MentorCatalogAssignment(models.Model):
    assignment_id = models.AutoField(primary_key=True)
    catalog = models.ForeignKey(AdmissionCatalog, on_delete=models.CASCADE, verbose_name="招生目录ID")
    mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE, verbose_name="导师ID")
    year = models.IntegerField(verbose_name="分配年度")
    has_admission_eligibility = models.BooleanField(default=False, verbose_name="是否具备招生资格")


#APPLICANT_SCORE 表
class ApplicantScore(models.Model):
    score_id = models.AutoField(primary_key=True)
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE, verbose_name="考生ID")
    preliminary_score = models.FloatField(verbose_name="初试成绩")
    final_score = models.FloatField(verbose_name="复试成绩")

#MENTOR_APPLICANT_PREFERENCE 表
class MentorApplicantPreference(models.Model):
    preference_id = models.AutoField(primary_key=True)
    applicant = models.ForeignKey('Applicant', on_delete=models.CASCADE, verbose_name="考生ID")
    mentor = models.ForeignKey('Mentor', on_delete=models.CASCADE, verbose_name="导师ID")
    preference_rank = models.IntegerField(verbose_name="志愿优先级")
    status = models.CharField(
        max_length=20,
        choices=[
            ('Pending', '待定'),
            ('Accepted', '已接受'),
            ('Rejected', '已拒绝')
        ],
        default='Pending',
        verbose_name="志愿状态"
    )
    remarks = models.TextField(blank=True, verbose_name="备注信息")

    def __str__(self):
        return f"{self.applicant.name} - {self.mentor.name} - Rank: {self.preference_rank}"

#APPLICANT_SCORE 表
class ApplicantScore(models.Model):
    score_id = models.AutoField(primary_key=True)
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE, verbose_name="考生ID")
    preliminary_score = models.FloatField(verbose_name="初试成绩")
    final_score = models.FloatField(verbose_name="复试成绩")

    def __str__(self):
        return f"{self.applicant.name} - Scores"



#SYSTEM_ROLE 表
class SystemRole(models.Model):
    role_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, verbose_name="角色名称")
    description = models.TextField(blank=True, verbose_name="角色描述")

    def __str__(self):
        return self.name


#USER_ROLE 表
class UserRole(models.Model):
    user_role_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(verbose_name="用户ID")
    role = models.ForeignKey(SystemRole, on_delete=models.CASCADE, verbose_name="角色ID")


#SYSTEM_ACTIVITY 表
class SystemActivity(models.Model):
    activity_id = models.AutoField(primary_key=True)
    role = models.ForeignKey(SystemRole, on_delete=models.CASCADE, verbose_name="角色ID")
    activity = models.TextField(verbose_name="核心业务需求活动描述")

