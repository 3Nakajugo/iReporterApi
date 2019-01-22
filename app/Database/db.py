import psycopg2


class Database:
    """ database class"""

    def __init__(self):
        self.connection = psycopg2.connect(
            dbname="reporter", user="edna", password="edna123", host="localhost", port="5432")
        self.cursor_obj = self.connection.cursor()
        self.connection.autocommit = True

    def create_tables(self):
        commands = (
            """CREATE TABLE IF NOT EXISTS users ( user_id SERIAL PRIMARY KEY NOT NULL,
            first_name VARCHAR(15) NOT NULL, last_name VARCHAR(15) NOT NULL,other_names VARCHAR(15) NOT NULL,
            email VARCHAR NOT NULL, telephone INT NOT NULL,user_name VARCHAR(5) NOT NULL,
            password VARCHAR(10) NOT NULL,registered TIMESTAMPTZ DEFAULT NOW(),isadmin VARCHAR NOT NULL)
        """,
            """CREATE TABLE IF NOT EXISTS redflags(incident_id SERIAL PRIMARY KEY NOT NULL,
            incident_type VARCHAR NOT NULL, date TIMESTAMPTZ DEFAULT NOW(), 
            created_by int REFERENCES users(user_id),location VARCHAR NOT NULL, status VARCHAR,
            file VARCHAR ,comment VARCHAR NOT NULL
        )""",
            """CREATE TABLE IF NOT EXISTS interventions(incident_id SERIAL PRIMARY KEY NOT NULL,
            incident_type VARCHAR NOT NULL, date TIMESTAMPTZ DEFAULT NOW(), 
            created_by int REFERENCES users(user_id),location VARCHAR NOT NULL, status VARCHAR ,file VARCHAR ,comment VARCHAR NOT NULL
        )"""
        )
        for command in commands:
            self.cursor_obj.execute(command)
