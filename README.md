# FastAPI practice
웹 크롤링: 검색 엔진의 구축 등을 위해 특정한 방법으로 웹 페이지를 수집하는 프로그램
<br>웹 스크래핑: 웹에서 데이터를 수집하는 프로그램
<br>robot.txt 에서 disallowed 를 제외한 웹 사이트 스크래핑하는 사이드 프로젝트

## 사용 스택
|      stack       |                                           |
|:----------------:|:-----------------------------------------:|
|     Language     |              Python (^3.11)               |
|    Framework     |             FastAPI (^0.86.0)             |
|     Database     |            PostgreSQL, MongoDB            |
|      Infra       | Docker, Redis, RabbitMQ, AWS EC2, RDS, S3 |
| Version Control  |            Git, Github, Poetry            |

## 목표
### 비동기 api 구현
aiohttp & asyncio 를 활용한 웹 스크래핑

### RDB & NoSQL 복수 DB 연동
기본적인 데이터 관리를 위한 MySQL과 알림 센터 관리를 위한 MongoDB 사용

### DB read 부하 줄이기
redis를 이용헌 DB caching 기능

### Async api w/ MQ
메세지 브로커를 이용해 알림 센터 및 이메일 발송

### Build Notification center

### Traffic Control

### source
- [source code](https://fastapi.tiangolo.com/)
- [gunicorn script1](https://zetawiki.com/wiki/Gunicorn.conf.py)
- [gunicorn script2](http://blog.hwahae.co.kr/all/tech/tech-tech/5567/?popular=5567)

