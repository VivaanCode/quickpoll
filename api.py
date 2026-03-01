import random, os
import psycopg2
from psycopg2.extras import RealDictCursor

db_url = os.getenv("DATABASE_URL")

try: 
  from dotenv import load_dotenv
  load_dotenv()
except:
  pass

conn = None

def dbConnect():
  global conn
  conn = psycopg2.connect(db_url)
  with conn.cursor() as c:
    c.execute("""
      CREATE TABLE IF NOT EXISTS polls (
        id TEXT PRIMARY KEY,
        question TEXT NOT NULL,
        options TEXT[] NOT NULL,
        votes INTEGER[] NOT NULL
      )
    """)
    conn.commit()

dbConnect()

def createId():
    try:
        while True:
            id = ""
            for i in range(6):
                id += random.choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
            
            with conn.cursor() as c:
                c.execute("SELECT id FROM polls WHERE id = %s", (id,))
                if c.fetchone() is None:
                    return id
    except psycopg2.InterfaceError as e:
        dbConnect()
        return createId()

def createPoll(question, *args):
    try:
        print(question)
        print(args)
        
        id = createId()
        votes = [0] * len(args)
        
        with conn.cursor() as c:
            c.execute(
                "INSERT INTO polls (id, question, options, votes) VALUES (%s, %s, %s, %s)",
                (id, question, list(args), votes)
            )
            conn.commit()
        
        return id
    except psycopg2.InterfaceError as e:
        dbConnect()
        return createPoll(question, *args)

def getPoll(id):
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as c:
            c.execute("SELECT * FROM polls WHERE id = %s", (id,))
            result = c.fetchone()
        
        if result:
            return {
                "question": result["question"],
                "options": result["options"],
                "votes": result["votes"]
            }
        return None
    except psycopg2.InterfaceError as e:
        dbConnect()
        return getPoll(id)

def vote(id, option):
    try:
        with conn.cursor() as c:
            c.execute("SELECT votes, options FROM polls WHERE id = %s", (id,))
            result = c.fetchone()
        
        if result:
            votes, options = result
            if 0 <= option < len(options):
                votes[option] += 1
                with conn.cursor() as c:
                    c.execute("UPDATE polls SET votes = %s WHERE id = %s", (votes, id))
                    conn.commit()
                return True
        
        return False
    except psycopg2.InterfaceError as e:
        dbConnect()
        return vote(id, option)

