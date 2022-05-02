import sqlite3 as sql
from sqlite3 import Error

from colorama import Cursor

#memory db to test stuff
#conn = sql.connect(':memory:')

class DB():
      
    #create connection to db, returns db
    def sql_connection():
        try:

            db = sql.connect('creators.db')

            return db

        except Error:

            print(Error)

    #create creator table
    def create_creators_table(db):
        c = db.cursor()

        c.execute(""" 
            CREATE TABLE IF NOT EXISTS creators (
            id INTEGER PRIMARY KEY AutoIncrement,
            r_user_id TEXT,
            r_username TEXT,
            of_username TEXT,
            has_of INTEGER,
            fansly_username TEXT,
            has_fansly INTEGER,
            karma INTEGER
            )
        """)

        db.commit()

    #insert into creator table
    def insert_creators_table(db, entities: tuple):

        c = db.cursor()

        c.execute("""
            INSERT INTO creators(r_user_id, r_username, of_username,
            has_of, fansly_username, has_fansly, karma)
            VALUES(?, ?, ?, ?, ?, ?, ?)""", entities)

        db.commit()
    
    #create fetish table
    def create_fetish_table(db):
        c = db.cursor()

        c.execute(""" 
            CREATE TABLE IF NOT EXISTS fetish (
            id INTEGER PRIMARY KEY AutoIncrement,
            name TEXT)
        """)

        db.commit()
    
    #insert into fetish table
    def insert_fetish_table(db, entity: str):

        c = db.cursor()

        c.execute("""
            INSERT INTO fetish(name)
            VALUES(?)""", entity)

        db.commit()

    #create user-fetish detail table
    def create_detailUserFetish_table(db):
        c = db.cursor()

        c.execute(""" 
            CREATE TABLE IF NOT EXISTS DetailUserFetish (
            fetish_id INTEGER,
            user_id INTEGER,
            FOREIGN KEY(fetish_id) REFERENCES fetish(id),
            FOREIGN KEY(user_id) REFERENCES creators(id))
        """)

        db.commit()
    
    #insert into user-fetish detail table
    def insert_detailUserFetish_table(db, entities: tuple):

        c = db.cursor()

        c.execute("""
            INSERT INTO DetailUserFetish(fetish_id, user_id)
            VALUES(?, ?)""", entities)

        db.commit()

    #create subreddit table
    def create_subreddit_table(db):
        c = db.cursor()
        #verification: optional/required
        #watermark: allowed/name only/forbidden
        #selling: allowed/restricted/forbidden
        c.execute(""" 
            CREATE TABLE IF NOT EXISTS subreddit (
            id INTEGER PRIMARY KEY AutoIncrement,
            name TEXT,
            sub_id TEXT,
            verification TEXT,
            member_count INTEGER,
            watermark TEXT,
            selling TEXT)
        """)

        db.commit()

    #insert into subreddit table
    def insert_subreddit_table(db, entities: tuple):
        c = db.cursor()

        c.execute("""
            INSERT INTO subreddit(name, sub_id, verification,
            member_count, watermark, selling)
            VALUES(?, ?, ?, ?, ?, ?)""", entities)

        db.commit()

    #create Subreddit-fetish table
    def create_detailSubredditFetish_table(db):
        c = db.cursor()

        c.execute(""" 
            CREATE TABLE IF NOT EXISTS DetailSubredditFetish (
            fetish_id INTEGER,
            subreddit_id INTEGER,
            FOREIGN KEY(fetish_id) REFERENCES fetish(id),
            FOREIGN KEY(subreddit_id) REFERENCES subreddit(id))
        """)

        db.commit()

    #insert into Subreddit-fetish table
    def insert_detailSubredditFetish_table(db, entities: tuple):
        c = db.cursor()

        c.execute("""
            INSERT INTO DetailSubredditFetish(fetish_id, subreddit_id)
            VALUES(?, ?)""", entities)

        db.commit()
   
    #print table
    def show_table(db, table_name: str):
        
        c = db.cursor()
        
        c.execute("""SELECT * from {}""".format(table_name))
    
        for row in c.fetchall():
            print(row)
        
        db.commit()

    def delete_table(db, table_name: str):
        c = db.cursor()
        
        c.execute(""" DROP TABLE {}""".format(table_name))

        db.commit()

        print("Table " + table_name + " dropped.")

    def show_database(db):

        c = db.cursor()

        c.execute("SELECT name FROM sqlite_master WHERE type='table';")
        
        print("List of tables\n")
        print(c.fetchall())