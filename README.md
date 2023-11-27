# python-basic-sqlite3

>간단한 게임의 메뉴구성과 sqlite3(SQLite 데이터베이스용 DB-API 2.0 인터페이스) 가이드와 예제

## Sample Code
### Preparation
[pygame_textinput](https://github.com/Nearoo/pygame-text-input)을 사전에 반드시 설치하여야 합니다.

### Folder Structure
```
.
├── main.py                 # main.py
├── components              # Components
│   ├── __init__.py         # __init__.py
│   └── button.py           # button object
├── db                      # Database files
│   ├── game_scores.db      # sqlite3 database file
│   └── game_scores.txt     # txt 파일 형태의 데이터 저장소
├── assetss                 # GUI asset files
│   ├── Background.png      # background image file for game
│   ├── Button Rect.png     # background image file for buttons
│   └── font.ttf            # font file
└── README.md
```

## sqlite3 Basic Guide
>SQLite는 Gerhard Häring에 의해 작성된 sqlite3 모듈을 통해 Python에서 사용할 수 있는 C 라이브러리입니다. 이 라이브러리는 별도의 서버 프로세스가 필요 없는 경량의 디스크 기반 데이터베이스를 제공하며, SQL 질의 언어의 비표준 변형을 사용하여 데이터베이스에 접근합니다. SQLite는 간단한 내부 데이터 저장용도로 사용되며, 필요에 따라 PostgreSQL이나 Oracle과 같은 더 큰 데이터베이스로의 코드 이식도 가능합니다.
### 사용법
>Python에서 'sqlite3' module을 사용하는 기본적인 사용방법은 다음과 같습니다.
*본 예제에서는 로컬파일로 제공되는 형태만 고려하였습니다.*
#### sqlite3 모듈 임포트
Python의 표준 라이브러리에 포함된 sqlite3 모듈을 임포트합니다.
```python
import sqlite3
```
#### 데이터베이스 연결 생성
데이터베이스에 연결을 생성합니다. 데이터베이스가 존재하지 않으면 SQLite가 생성합니다. 이 예제에서는 데이터베이스 이름을 example.db로 합니다.
```python
conn = sqlite3.connect('example.db')
```
#### 커서 객체 생성
연결을 사용하여 커서 객체를 생성합니다. 이 커서는 SQL 명령을 실행하는 데 사용됩니다.
```python
cursor = conn.cursor()
```
#### 테이블 생성
커서를 사용하여 테이블을 생성하는 SQL 명령을 실행합니다. 예를 들어, id와 name 두 필드를 가진 users라는 이름의 테이블을 생성합니다.
```python
cursor.execute('''CREATE TABLE users (id integer primary key, name text)''')
```
#### 데이터 삽입
테이블에 데이터를 삽입합니다. 여기서는 ID가 1이고 이름이 'Alice'인 사용자를 추가합니다.
```python
cursor.execute("INSERT INTO users VALUES (1, 'Alice')")
```
#### 트랜잭션 커밋
데이터베이스에 변경 사항을 저장(커밋)합니다.
```python
conn.commit()
```
#### 데이터 조회
테이블에서 데이터를 검색하는 쿼리를 실행합니다. 이 예제에서는 users 테이블의 모든 행을 가져옵니다.
```python
cursor.execute('SELECT * FROM users')
print(cursor.fetchall())
```
#### 연결 닫기
작업이 끝나면 데이터베이스 연결을 닫습니다.
```python
conn.close()
```
### 참고 
[https://www.sqlite.org](https://www.sqlite.org)   
SQLite 웹 페이지; 설명서는 지원되는 SQL 언어에 대한 문법과 사용 가능한 데이터형을 설명합니다.   
[https://www.w3schools.com/sql/](https://www.w3schools.com/sql/)   
SQL 문법 학습을 위한 자습서, 레퍼런스 및 예제   
[PEP 249 - 데이터베이스 API 명세 2.0](https://peps.python.org/pep-0249/)   
Marc-André Lemburg가 작성한 PEP.   
