import json
import sqlite3

class DecisionApp:
    def __init__(self, json_filepath="comprehensive_decision_maker.json", db_path="users_data.db"):
        self.json_filepath = json_filepath
        self.db_path = db_path
        self.data = self.load_json()
        self.init_db()

    def load_json(self):
        try:
            with open(self.json_filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error reading JSON file: {e}")
            return {"categories": []}

    def init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                password TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                category TEXT,
                score INTEGER,
                total_possible_score INTEGER,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()

    def login_or_register(self, username, password):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()
        if user:
            conn.close()
            return True, "Welcome back!"
        else:
            try:
                cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
                conn.commit()
                conn.close()
                return True, "New user registered and logged in!"
            except Exception as e:
                conn.close()
                return False, str(e)

    def get_categories(self):
        return [cat["category"] for cat in self.data.get("categories", [])]

    def get_questions_for_category(self, category_name, num_questions=15):
        for cat in self.data.get("categories", []):
            if cat["category"] == category_name:
                return cat["questions"][:num_questions]
        return []

    def save_result(self, username, category, answers, questions):
        total_score = 0
        total_possible_score = 0
        for i, q in enumerate(questions):
            ans_idx = answers[i]
            # Handle list based or integer answer mapping depending on structure
            weight = q["weights"][ans_idx]
            total_score += weight
            total_possible_score += max(q["weights"])

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO results (username, category, score, total_possible_score) VALUES (?, ?, ?, ?)",
            (username, category, total_score, total_possible_score)
        )
        conn.commit()
        conn.close()
        return total_score, total_possible_score
# import json
# import sqlite3

# class DecisionApp:
#     def __init__(self, json_filepath="comprehensive_decision_maker.json", db_path="users_data.db"):
#         self.json_filepath = json_filepath
#         self.db_path = db_path
#         self.data = self.load_json()
#         self.init_db()

#     def load_json(self):
#         try:
#             with open(self.json_filepath, 'r', encoding='utf-8') as f:
#                 return json.load(f)
#         except Exception as e:
#             print(f"Error reading JSON file: {e}")
#             return {"categories": []}

#     def init_db(self):
#         conn = sqlite3.connect(self.db_path)
#         cursor = conn.cursor()
#         cursor.execute('''
#             CREATE TABLE IF NOT EXISTS users (
#                 id INTEGER PRIMARY KEY AUTOINCREMENT,
#                 username TEXT,
#                 password TEXT
#             )
#         ''')
#         cursor.execute('''
#             CREATE TABLE IF NOT EXISTS results (
#                 id INTEGER PRIMARY KEY AUTOINCREMENT,
#                 username TEXT,
#                 category TEXT,
#                 score INTEGER,
#                 total_possible_score INTEGER,
#                 timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
#             )
#         ''')
#         conn.commit()
#         conn.close()

#     def login_or_register(self, username, password):
#         conn = sqlite3.connect(self.db_path)
#         cursor = conn.cursor()
#         cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
#         user = cursor.fetchone()
#         if user:
#             conn.close()
#             return True, "Welcome back!"
#         else:
#             try:
#                 cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
#                 conn.commit()
#                 conn.close()
#                 return True, "New user registered and logged in!"
#             except Exception as e:
#                 conn.close()
#                 return False, str(e)

#     def get_categories(self):
#         return [cat["category"] for cat in self.data.get("categories", [])]

#     def get_questions_for_category(self, category_name, num_questions=15):
#         for cat in self.data.get("categories", []):
#             if cat["category"] == category_name:
#                 return cat["questions"][:num_questions]
#         return []

#     def save_result(self, username, category, answers, questions):
#         total_score = 0
#         total_possible_score = 0
#         for i, q in enumerate(questions):
#             ans_idx = answers[i]
#             weight = q["weights"][ans_idx]
#             total_score += weight
#             total_possible_score += max(q["weights"])

#         conn = sqlite3.connect(self.db_path)
#         cursor = conn.cursor()
#         cursor.execute(
#             "INSERT INTO results (username, category, score, total_possible_score) VALUES (?, ?, ?, ?)",
#             (username, category, total_score, total_possible_score)
#         )
#         conn.commit()
#         conn.close()
#         return total_score, total_possible_score


