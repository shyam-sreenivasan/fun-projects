# ORM with SQLAlchemy - 

## 13 Reasons Why (ORM story)
1. **Entity Mapping:**
   - Mapping database tables to object-oriented classes for seamless interaction.

2. **CRUD Operations:**
   - Object-oriented syntax for creating, reading, updating, and deleting database records.

3. **Query Language:**
   - Declarative query language simplifying database queries within the programming language.

4. **Database Agnostic:**
   - Achieving database independence, allowing compatibility with various database systems.

5. **Connection Management:**
   - Efficient handling of database connections through connection pooling for reduced overhead.

6. **Lazy Loading:**
   - On-demand loading of data for improved performance and reduced resource consumption.

7. **Transaction Support:**
   - Ensuring the success or failure of a series of operations as a single, atomic unit.

8. **Caching:**
   - Mechanisms for caching frequently accessed data, enhancing overall application performance.

9. **Concurrency Control:**
   - Providing optimistic and pessimistic locking mechanisms for managing concurrent data access.

10. **Schema Migrations:**
    - Tools facilitating versioning and application of database schema changes over time.

11. **Integration with Frameworks:**
    - Seamless incorporation into popular web frameworks and development tools.

12. **Validation and Data Integrity:**
    - Support for data validation pre-persistence, ensuring data integrity and consistency.

13. **Pluggable Architecture:**
    - A flexible, extensible architecture enabling customization for specific project requirements.


## SQLAlchemy architecture diagram
![Alt text](architecture.png "a title")

## Prerequisites
- setup mysql
- create a database with the name of your choice. Say "test".
- create a table with the following schema
```sql
 CREATE TABLE `persons` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(40) NOT NULL,
  `email` varchar(40) DEFAULT NULL,
  `status` int(11) DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
)
```
- setup python3,other related packages for python-mysql and install sqlalchemy.

## Key ideas
- **engine** is the like the endpoint to the db connection
- sqlalchemy as 2 important modules. 
	- **core**
	- **orm**.
- core can be used to build parameterized queries whereas orm is used with classes and objects.
- `connection and session` are two key api's from the core and orm modules respectively to interact with the db.

## Insert multiple rows in the person table at once. 
```python
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
engine = create_engine("mysql+pymysql://root:root@mysql:3306/giottus")

persons = [
	{
		"name": "shyam",
		"email": "shyam@genius.com"
	},
	{
		"name": "sreeni",
		"email": "sreeni@comedy.com"
	}
]

params = [{"x": p["name"], "y": p["email"]} for p in persons]

```

- Using core (connection).
```
with engine.connect() as conn:
	stmt = text("INSERT INTO Persons(name, email) VALUES (:x, :y)")
	res = conn.execute(stmt, params)
	print(res)
```

- Using core (connection) when `autocommit and autoflush disabled`.
```python
with engine.connect() as conn:
	conn.execution_options(autocommit=False, autoflush=False)
	stmt = text("INSERT INTO Persons(name, email) VALUES (:x, :y)")
	res = conn.execute(stmt, params)
	conn.flush()
	conn.commit()
```

- Using orm (Session)
```python
with Session(engine) as session:
	stmt = text("INSERT INTO Persons(name, email) VALUES (:x, :y)")
	res = session.execute(stmt, params)

```

- Using ORM (session) `autocommit and autoflush is disabled`.
```python
with Session(engine, autocommit=False, autoflush=False) as session:
	stmt = text("INSERT INTO Persons(name, email) VALUES (:x, :y)")
	res = session.execute(stmt, params)
	session.flush()
	session.commit()

```

`Note conn.begin() and session.begin() can be used to write a single block of atomic transaction`

