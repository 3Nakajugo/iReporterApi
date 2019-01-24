import os
import psycopg2
import psycopg2.extras
from pprint import pprint


class Database:
    """ database class"""

    def __init__(self):
        try:
            if os.getenv('APP_SETTINGS') == 'testing':
                db = 'testdb'
            else:
                db = 'reporter'
            self.connection = psycopg2.connect(
                dbname=db, user="postgres", host="localhost", port="5432")
            self.cursor_obj = self.connection.cursor(
                cursor_factory=psycopg2.extras.RealDictCursor)
            self.connection.autocommit = True
        except:
            print("cannot connect succesfully")

    def create_tables(self):
        commands = (
            """CREATE TABLE IF NOT EXISTS users ( user_id SERIAL PRIMARY KEY NOT NULL,
            first_name VARCHAR NOT NULL, last_name VARCHAR NOT NULL,other_names VARCHAR NOT NULL,
            email VARCHAR NOT NULL, telephone INT NOT NULL,user_name VARCHAR NOT NULL,
            password VARCHAR(10) NOT NULL,registered TIMESTAMPTZ DEFAULT NOW(), isadmin VARCHAR DEFAULT 'false')
        """,
            """CREATE TABLE IF NOT EXISTS redflags(incident_id SERIAL PRIMARY KEY NOT NULL,
            incident_type VARCHAR DEFAULT 'redflag' , date TIMESTAMPTZ DEFAULT NOW(),
            location INT NOT NULL, status VARCHAR DEFAULT 'draft',
            file VARCHAR ,comment VARCHAR NOT NULL
        )""",
            """CREATE TABLE IF NOT EXISTS interventions(incident_id SERIAL PRIMARY KEY NOT NULL,
            incident_type VARCHAR DEFAULT 'intervention', date TIMESTAMPTZ DEFAULT NOW(),
            location INT NOT NULL, status VARCHAR DEFAULT 'draft',
            file VARCHAR ,comment VARCHAR NOT NULL
        )"""
        )
        for command in commands:
            self.cursor_obj.execute(command)

    def drop_tables(self):
        query = 'TRUNCATE users,redflags,interventions'
        self.cursor_obj.execute(query)

    def create_user(self, first_name, last_name, other_names, email, telephone, user_name, password):
        """
        creates user in database table users
        """
        query = ("""INSERT INTO users(first_name, last_name, other_names, email, telephone, user_name, password) VALUES ('{}','{}','{}','{}','{}','{}','{}')RETURNING user_name """.format(
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
            """INSERT INTO redflags( location, file, comment) VALUES ('{}','{}','{}')RETURNING incident_id""".format(location, file, comment))
        self.cursor_obj.execute(query)
        reflag_record = self.cursor_obj.fetchall()
        return reflag_record

    def get_user_by_username(self, user_name):
        query = ("""SELECT * FROM users WHERE user_name='{}'""".format(user_name))
        self.cursor_obj.execute(query)
        user_exists = self.cursor_obj.fetchone()
        return user_exists

    def login(self, username, password):
        """
        logs in user that exists inthe database
        """
        query = (
            """ SELECT * FROM users WHERE user_name='{}'AND password='{}' """).format(username, password)
        self.cursor_obj.execute(query)
        returned_user = self.cursor_obj.fetchone()
        return returned_user

    def get_all_redflags(self):
        """
        gets all redflags from table redflags
        """
        query = """SELECT * FROM redflags"""
        self.cursor_obj.execute(query)
        all_redflags = self.cursor_obj.fetchall()
        return all_redflags

    def get_single_redflag(self, incident_id):
        """
        gets single redflag from table redflags
        """
        query = (
            """SELECT * FROM redflags WHERE incident_id = '{}' """.format(incident_id))
        self.cursor_obj.execute(query)
        single_redflag = self.cursor_obj.fetchone()
        return single_redflag

    def delete_redflag(self, incident_id):
        """
        deletes redflag from table redflags
        """
        query = (
            """ DELETE FROM redflags WHERE incident_id = '{}'""".format(incident_id))
        self.cursor_obj.execute(query)

    def update_location(self, location, incident_id):
        """updates location """
        query = ("""UPDATE redflags SET location = {} WHERE incident_id = {} """.format(
            location, incident_id))
        self.cursor_obj.execute(query)
        updated_location = self.cursor_obj
        return updated_location

    def update_comment(self, comment, incident_id):
        """updates location """
        query = ("""UPDATE redflags SET location = {} WHERE incident_id = {} """.format(
            comment, incident_id))
        self.cursor_obj.execute(query)
        updated_comment = self.cursor_obj
        return updated_comment

    def create_intervention(self, location, file, comment):
        """
        creates intervention in database table intervention
        """
        query = (
            """INSERT INTO interventions( location, file, comment) VALUES ('{}','{}','{}')RETURNING incident_id """.format(location, file, comment))
        self.cursor_obj.execute(query)
        intervention_record = self.cursor_obj.fetchone()
        return intervention_record

    def get_all_interventions(self):
        """
        gets all interventions from table interventions
        """
        query = """SELECT * FROM interventions"""
        self.cursor_obj.execute(query)
        all_interventions = self.cursor_obj.fetchall()
        return all_interventions

    def get_single_intervention(self, incident_id):
        """
        gets single intervention
        """
        query = (
            """SELECT * FROM interventions WHERE incident_id = {} """.format(incident_id))
        self.cursor_obj.execute(query)
        single_intervention = self.cursor_obj.fetchone()
        return single_intervention

    def delete_intervention(self, incident_id):
        """
        deletes intervention from table interventions
        """

        query = (
            """ DELETE FROM interventions WHERE incident_id = '{}'""".format(incident_id))
        self.cursor_obj.execute(query)

    def update_intervention_location(self, location, incident_id):
        """updates location of intervention"""
        query = ("""UPDATE interventions SET location = {} WHERE incident_id = {}""".format(
            location, incident_id))
        self.cursor_obj.execute(query)
        new_location = self.cursor_obj
        return new_location

    def update_intervention_comment(self, comment, incident_id):
        """updates comment of intervention"""
        query = ("""UPDATE interventions SET comment = '{}' WHERE incident_id = {}""".format(
            comment, incident_id))
        self.cursor_obj.execute(query)
        new_comment = self.cursor_obj
        return new_comment
    
    # def update_status(self,isadmin,incident_id):
    #     """ 
    #     update status
    #     """
    #     query= ()



if __name__ == '__main__':
    db = Database()
