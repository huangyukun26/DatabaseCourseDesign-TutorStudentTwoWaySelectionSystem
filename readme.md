# 2024 BJFU Database Course Design

## Introduction

The overall goal of this course design is to design a two-way selection system for tutors and students based on SQL database, providing business functions for three roles: candidates, tutors, and administrators. The candidate-side business line includes viewing personal information and enrollment plans, volunteer registration, score query, and admission status query, helping candidates understand admission information and complete the volunteer application process. The tutor-side business line focuses on the screening of candidates' volunteer information and scores, and provides tutors with suitable student choices through a multi-level matching mechanism. The administrator-side business line is responsible for global management, configuring enrollment plans, monitoring the selection process of tutors and students, and managing system activity logs.

The system builds multiple core table structures, fully designs and implements the persistence layer, and uses the signal mechanism to automatically generate system role associations to ensure data consistency and security. In addition, the system integrates multiple security controls such as verification codes and role permission control in login verification to ensure data access security.

## Demo

This project has not been fully developed and is very crude. We have not yet deployed it to the server. Please use the local view.

## Table of Contents

- [Analyze](#analyze)
- [Design](#design)
- [Usage](#usage)
- [Development](#development)
- [Contribute](#contribute)

## Analyze

[(Back to top)](#table-of-contents)

## Design

[(Back to top)](#table-of-contents)

## Usage

##### Environment

```
git clone https://github.com/huangyukun26/BJFU-Database-Course-Design.git
-- It is recommended to use a virtual conda environment
cd Source
conda env create -f environment.yaml
conda activate mentor_student
```

##### Initialization Database

**If you need data testing for this course design, please contact me huangyukun@bjfu.edu.cn**

```
cd Source/src
Modify the 'database' in the 'setting' file
my database eg:
DATABASES = {
    'default': {
        'ENGINE':'django.db.backends.mysql',
        'NAME':'mentor_student',
        'USER':'root',
        'PASSWORD':'yourpassword',
        'HOST':'localhost',
        'PORT':'3306',
    }
}

*Database Migration
**for initialization
cd ..
python manage.py migrate
```

##### Initialization For Vue

```
cd frontms
npm install
```

##### View In The Web

```
cd frontms
npm run serve
cd ..
python manage.py runserver
Visit the browser address http://127.0.0.1:8080/
```

[(Back to top)](#table-of-contents)

## Development

#### Technology Stack

Backend framework Django4.2.16 ![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green)

Database MySQL8.0 ![MySQL](https://img.shields.io/badge/MySQL-005C84?style=for-the-badge&logo=mysql&logoColor=white)

Frontend framework Vue3.0 ![Vue](https://img.shields.io/badge/Vue%20js-35495E?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D)

[(Back to top)](#table-of-contents)

## Contribute

For details, please see the commit notes of the main branch.

If you are interested in this project, welcome to fork and submit changes!

[(Back to top)](#table-of-contents)
