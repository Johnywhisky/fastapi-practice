# fast-api practice
Fastapi [공식문서](https://fastapi.tiangolo.com/)를 참고해 만든 기초 프로젝트 구조

## 프로젝트 기초 구조 구성
config, database, api 분리

### config
1. dotenv를 이용해 settings에서 환경변수 분리
2. lru_cache를 이용한 환경변수 캐싱

### router
1. router decorator를 활용한 api 폴더 분리
2. Functional Api Structure

### database
1. Model 별 crud, models 정의, schema 정의