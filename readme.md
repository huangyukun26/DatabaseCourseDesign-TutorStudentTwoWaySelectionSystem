# 2024 BJFU Database Course Design

## Introduction

## Demo

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

#### For Developers(Beta version)

##### Environment

```
git clone https://github.com/huangyukun26/BJFU-Database-Course-Design.git
-- It is recommended to use a virtual conda environment
cd Source
conda env create -f environment.yaml
conda activate mentor_student
```

##### Initialization For Django

```
cd Source/src
Modify the 'database' in the 'setting' file
my database eg:
DATABASES = {
    'default': {
        'ENGINE':'django.db.backends.mysql',
        'NAME':'mentor_student',
        'USER':'root',
        'PASSWORD':'ROOT050313cel*',
        'HOST':'localhost',
        'PORT':'3306',
    }
}

*Database Migration
**for initialization
cd ..
python manage.py migrate

**after modify database(if)
python manage.py makemigrations mentor_student
python manage.py migrate
***The above two commands must be executed every time the database is modified.!!***
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
python manage.py runserver8
Visit the browser address http://127.0.0.1:8080/
```

[(Back to top)](#table-of-contents)

## Development

#### Technology Stack

Django MySQL8.0 Vue3.0

[(Back to top)](#table-of-contents)

## Contribute

[(Back to top)](#table-of-contents)
