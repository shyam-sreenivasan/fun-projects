from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session

"""
CREATE TABLE Persons (
	`id` int auto_increment,
	`name` varchar(40) not null,
	`email` varchar(40) not null,
	`status` int default 0,
	primary key(`id`)
);
"""

engine = create_engine("mysql+pymysql://root:root@mysql:3306/giottus")
# with engine.connect() as conn:
# 	stmt = text("show tables;")
# 	result = conn.execute(stmt)
# 	print(result.all())

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

print("params", params)

	

# with engine.connect() as conn:
#     # Check if autocommit is enabled
#     is_autocommit = conn.in_transaction() and not conn.in_nested_transaction()
#     # Print the result
#     print(f"Autocommit Enabled: {is_autocommit}")


