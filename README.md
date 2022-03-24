# fast-api practice
Fastapi [공식문서](https://fastapi.tiangolo.com/)를 참고해 만든 기초 프로젝트 구조

## Project setUp
*Todo List*
1. Installation pipenv
```
brew install pipenv
```
(이미 설치되어있다면 생략 가능)

2. Set up project 
```
git clone https://github.com/Johnywhisky/fastapi-practice.git
cd fastapi-practice
pipenv install
pipenv shell
```

3. Run server
```
gunicorn --preload -c gunicorn.conf.py main:app
```

## Project description
config, database, api 분리

### [config](https://github.com/Johnywhisky/fastapi-practice/tree/dev/config)
1. dotenv를 이용해 settings에서 환경변수 분리
2. lru_cache를 이용한 환경변수 캐싱

### [api](https://github.com/Johnywhisky/fastapi-practice/tree/dev/api)
1. router decorator를 활용한 api 폴더 분리
2. Functional Api Structure

### [database](https://github.com/Johnywhisky/fastapi-practice/tree/dev/database)
1. Model 별 crud, models 정의, schema 정의

## 2차 목표
1. naver 부동산 crawling api
2. crawoling 전처리 및 db modeling

### source
- [source code](https://fastapi.tiangolo.com/)
- [gunicorn script1](https://zetawiki.com/wiki/Gunicorn.conf.py)
- [gunicorn script2](http://blog.hwahae.co.kr/all/tech/tech-tech/5567/?popular=5567)