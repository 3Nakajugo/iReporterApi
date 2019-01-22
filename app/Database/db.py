import psycopg2
import psycopg2.extras


class Database:
    """ database class"""

    def __init__(self):
        self.connection = psycopg2.connect(
            dbname="reporter", user="edna", password="edna123", host="localhost", port="5432")
        self.cursor_obj = self.connection.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor)
        self.connection.autocommit = True

    def create_tables(self):
        commands = (
            """CREATE TABLE IF NOT EXISTS users ( user_id SERIAL PRIMARY KEY NOT NULL,
            first_name VARCHAR NOT NULL, last_name VARCHAR NOT NULL,other_names VARCHAR NOT NULL,
            email VARCHAR NOT NULL, telephone INT NOT NULL,user_name VARCHAR(10) NOT NULL,
            password VARCHAR(10) NOT NULL,registered TIMESTAMPTZ DEFAULT NOW(), isadmin VARCHAR DEFAULT 'false')
        """,
            """CREATE TABLE IF NOT EXISTS redflags(incident_id SERIAL PRIMARY KEY NOT NULL,
            incident_type VARCHAR DEFAULT 'redflag' , date TIMESTAMPTZ DEFAULT NOW(),
            location VARCHAR NOT NULL, status VARCHAR DEFAULT 'draft',
            file VARCHAR ,comment VARCHAR NOT NULL
        )""",
            """CREATE TABLE IF NOT EXISTS interventions(incident_id SERIAL PRIMARY KEY NOT NULL,
            incident_type VARCHAR NOT NULL, date TIMESTAMPTZ DEFAULT NOW(),location VARCHAR NOT NULL, status VARCHAR,
            file VARCHAR ,comment VARCHAR NOT NULL
        )"""
        )
        for command in commands:
            self.cursor_obj.execute(command)

    def create_user(self, first_name, last_name, other_names, email, telephone, user_name, password):
        """
        creates user in database table users
        """
        query = ("""INSERT INTO users(first_name, last_name, other_names, email, telephone, user_name, password) VALUES ('{}','{}','{}','{}','{}','{}','{}')RETURNING user_id""".format(
            first_name, last_name, other_names, email, telephone, user_name, password))
        self.cursor_obj.execute(query)
        returned_record = self.cursor_obj.fetchone()
        return returned_record

    def select_all_users(self):
        pass

    def create_redflag(self, location, file, comment):
        """
        creates redflag in database table redflags
        """
        query = (
            """INSERT INTO redflags( location, file, comment) VALUES ('{}','{}','{}')RETURNING *""".format(location, file, comment))
        self.cursor_obj.execute(query)
        returned_record = self.cursor_obj.fetchone()
        return returned_record

    def create_intervention(self, location, file, comment):
        """
        creates intervention in database table intervention
        """
        query = (
            """INSERT INTO redflags( location, file, comment) VALUES ('{}','{}','{}')RETURNING *""".format(location, file, comment))
        self.cursor_obj.execute(query)
        returned_record = self.cursor_obj.fetchone()
        return returned_record

    def login(self, username, password):
        """
        logs in user that exists inthe database
        """
        query = (
            """ SELECT * FROM users WHERE user_name='{}'AND password='{}' """).format(username, password)
        self.cursor_obj.execute(query)
        returned_user = self.cursor_obj.fetchone()
        return returned_user
