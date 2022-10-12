## Wanted-pre-onboarding-BE

### 사용한 기술
- Python
- Django REST Framework
- PostgreSQL
- Docker

### 요구사항 분석 및 구현 과정
- 1. 채용 공고를 등록
- 2. 채용 공고를 수정
- 3. 채용 공고를 삭제
- 4. 1. 채용 공고 목록 가져오기
- 4. 2. 채용 공고 검색 기능 구현
- 5. 채용 상세 페이지
- 6. 채용 공고 지원

- 전체적인 요구사항이 채용 공고를 기준으로 합니다.
- 따라서 채용 공고(Recruit) 모델을 기준으로 회사(Company), 지원내역(Apply) 모델 생성했습니다.
- App은 Recruit, User만 생성하여 Recruit App에서 Company, Apply 에 필요한 기능들을 구현했습니다.
<img src=/images/ERD.png>

##### 1. 채용 공고를 등록
- Method: POST
- URL: /api/recruit/recruits/
- 제목, 회사이름, 포지션, 보상금, 채용 내용, 사용기술을 입력하여 채용 공고를 등록합니다.
```
{
    "title": "원티드 백엔드",
    "position": "백엔드",
    "company": 원티드,
    "reward": 100000,
    "stack": "Python",
    "description": "Django"
}
```
##### 2. 채용 공고를 수정
- Method: Put, Patch
- URL: /api/recruit/recruits/int:id/
- url에서 수정할 채용 공고의 id를 받습니다.
- 수정할 정보 일부 혹은 전체를 받습니다.
- 유효하지 않은 회사 입력 시 400 에러를 발생합니다.
```
{
    "title": "원티드 프론트엔드",
    "position": "프론트엔드",
    "stack": "JS",
    "description": "React"
}
```
##### 3. 채용 공고를 삭제
- Method: Delete
- URL: /api/recruit/recruits/int:id/
- url에서 삭제할 채용 공고의 id를 받습니다.
- 삭제 후 204 에러를 발생합니다.

##### 4-1. 채용 공고 목록 가져오기
- Method: GET
- URL: /api/recruit/recruits/
- 채용 공고 전체 목록을 가져옵니다.
- 채용 내용은 표시하지 않습니다.
```
[
    {
        "id": 1,
        "title": "원티드랩 백엔드",
        "position": "백엔드",
        "company": "원티드랩",
        "reward": 10000,
        "stack": "Python"
    },
    {
        "id": 2,
        "title": "원티드랩 프론트엔드",
        "position": "프론트엔드",
        "company": "원티드랩",
        "reward": 20000,
        "stack": "js"
    },
    {
        "id": 3,
        "title": "원티드랩 AI",
        "position": "AI엔지니어",
        "company": "원티드랩",
        "reward": 30000,
        "stack": "pytorch"
    }
]
```
##### 4-2. 채용 공고 검색 기능 구현
- Method: GET
- URL: /api/recruit/recruits/?search="키워드"
- "키워드"를 입력하여 검색합니다.
- 검색 가능한 필드는 제목, 포지션, 회사 이름, 기술스택으로 하였습니다.
```
/api/recruit/recruits/?search=백엔드

[
    {
        "id": 1,
        "title": "원티드랩",
        "position": "백엔드",
        "company": "원티드랩",
        "reward": 10000,
        "stack": "Python"
    }
]
```

##### 5. 채용 상세 페이지
- Method: GET
- URL: /api/recruit/recruits/id/
- 상세 페이지에서 description, 회사가올린채용공고(related_ad)를 표시합니다.
```
{
    "id": 1,
    "title": "원티드랩",
    "position": "백엔드",
    "company": "원티드랩",
    "reward": 10000,
    "stack": "Python",
    "description": "django",
    "related_ad": [
        2,
        3
    ]
}

```

##### 6. 채용 공고 지원
- Method: POST
- URL: /api/recruit/applies/
- 채용 공고 id와 user id를 받아서 등록합니다.
- 중복 지원을 막기 위해 채용 공고 id와 user id 조합에 unique constraint를 추가하였습니다.

```
{
    "recruit": 1,
    "user": 1
}
```