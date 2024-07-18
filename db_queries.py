# db_queries.py
import psycopg2
from psycopg2.extras import DictCursor
from datetime import datetime

# Database connection parameters
DB_PARAMS = {
    'dbname': 'hhh',
    'user': 'postgres',
    'password': 'password',
    'host': 'localhost'
}

def get_db_connection():
    return psycopg2.connect(**DB_PARAMS)

def register_user(uid, username, email, hashed_password):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            try:
                cur.execute("INSERT INTO Users (UID, Username, Email, HashPW) VALUES (%s, %s, %s, %s)",
                            (uid, username, email, hashed_password))
                cur.execute("INSERT INTO Players (UID) VALUES (%s)", (uid,))
                conn.commit()
                return True
            except psycopg2.Error:
                conn.rollback()
                return False

def get_user_by_username(username):
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute("SELECT * FROM Users WHERE Username = %s", (username,))
            return cur.fetchone()

def is_admin(uid):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT 1 FROM Admins WHERE UID = %s", (uid,))
            return cur.fetchone() is not None

def get_quests_in_progress(uid):
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute("""
                SELECT q.QID, q.QuestName
                FROM Quests q
                JOIN PlayerQuests pq ON q.QID = pq.QID
                WHERE pq.UID = %s AND pq.IsCompleted = FALSE
            """, (uid,))
            return cur.fetchall()

def get_quests_completed(uid):
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute("""
                SELECT q.QID, q.QuestName
                FROM Quests q
                JOIN PlayerQuests pq ON q.QID = pq.QID
                WHERE pq.UID = %s AND pq.IsCompleted = TRUE
            """, (uid,))
            return cur.fetchall()

def get_quests_available(uid):
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute("""
                SELECT q.QID, q.QuestName
                FROM Quests q
                WHERE q.QID NOT IN (
                    SELECT pq.QID
                    FROM PlayerQuests pq
                    WHERE pq.UID = %s
                )
            """, (uid,))
            return cur.fetchall()

def get_quest(quest_id):
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute("SELECT * FROM Quests WHERE QID = %s", (quest_id,))
            return cur.fetchone()

def get_quest_problems(quest_id):
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute("""
                SELECT p.PID, p.ProblemLink, p.Difficulty
                FROM Problems p
                JOIN QuestProblems qp ON p.PID = qp.PID
                WHERE qp.QID = %s
            """, (quest_id,))
            return cur.fetchall()

def is_quest_started(uid, quest_id):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT 1 FROM PlayerQuests WHERE UID = %s AND QID = %s", (uid, quest_id))
            return cur.fetchone() is not None

def start_quest_for_player(uid, quest_id):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO PlayerQuests (UID, QID) VALUES (%s, %s)", (uid, quest_id))
            conn.commit()

def complete_problem_for_player(uid, problem_id):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO CompletedProblems (UID, PID, CompletionDate) VALUES (%s, %s, %s)",
                        (uid, problem_id, datetime.now()))
            conn.commit()

def uncomplete_problem_for_player(uid, problem_id):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM CompletedProblems WHERE UID = %s AND PID = %s", (uid, problem_id))
            conn.commit()

def get_admin_created_quests(uid):
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute("SELECT QID, QuestName FROM Quests WHERE UID = %s", (uid,))
            return cur.fetchall()

def create_quest_with_problems(uid, quest_name, problems):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            try:
                # Create quest
                cur.execute("INSERT INTO Quests (QuestName, UID) VALUES (%s, %s) RETURNING QID", (quest_name, uid))
                quest_id = cur.fetchone()[0]
                
                # Create problems and associate them with the quest
                for problem in problems:
                    cur.execute("INSERT INTO Problems (ProblemLink, Difficulty) VALUES (%s, %s) RETURNING PID",
                                (problem['link'], problem['difficulty']))
                    problem_id = cur.fetchone()[0]
                    
                    # Associate problem with quest
                    cur.execute("INSERT INTO QuestProblems (QID, PID) VALUES (%s, %s)", (quest_id, problem_id))
                    
                    # Add topics for the problem
                    for topic in problem['topics']:
                        cur.execute("INSERT INTO Topics (Type) VALUES (%s) ON CONFLICT (Type) DO NOTHING", (topic,))
                        cur.execute("INSERT INTO ProblemTopics (PID, Type) VALUES (%s, %s)", (problem_id, topic))
                
                conn.commit()
            except psycopg2.Error:
                conn.rollback()
                raise
