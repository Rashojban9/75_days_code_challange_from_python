import sqlite3

class OnlineVotingSystem:

    def __init__(self):
        self.conn = sqlite3.connect('online_voting.db')
        self.create_tables()

    def create_tables(self):
        users_table = '''CREATE TABLE IF NOT EXISTS users (
                          user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                          username TEXT,
                          password TEXT,
                          role TEXT);'''

        voters_table = '''CREATE TABLE IF NOT EXISTS voters (
                           voter_id INTEGER PRIMARY KEY AUTOINCREMENT,
                           name TEXT,
                           voter_card TEXT UNIQUE,
                           has_voted INTEGER DEFAULT 0);'''

        candidates_table = '''CREATE TABLE IF NOT EXISTS candidates (
                               candidate_id INTEGER PRIMARY KEY AUTOINCREMENT,
                               name TEXT,
                               votes INTEGER DEFAULT 0);'''

        cursor = self.conn.cursor()
        cursor.execute(users_table)
        cursor.execute(voters_table)
        cursor.execute(candidates_table)
        self.conn.commit()

    def register_voter(self, name, voter_card):
        sql = '''INSERT INTO voters(name, voter_card) VALUES(?, ?);'''
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql, (name, voter_card))
            self.conn.commit()
            print("Voter registered successfully.")
        except sqlite3.IntegrityError:
            print("Voter card already exists.")

    def cast_vote(self, voter_card, candidate_id):
        check_voter_sql = '''SELECT has_voted FROM voters WHERE voter_card = ?;'''
        update_vote_sql = '''UPDATE candidates SET votes = votes + 1 WHERE candidate_id = ?;'''
        update_voter_sql = '''UPDATE voters SET has_voted = 1 WHERE voter_card = ?;'''

        cursor = self.conn.cursor()
        cursor.execute(check_voter_sql, (voter_card,))
        voter = cursor.fetchone()

        if voter and voter[0] == 0:
            cursor.execute(update_vote_sql, (candidate_id,))
            cursor.execute(update_voter_sql, (voter_card,))
            self.conn.commit()
            print("Vote cast successfully.")
        else:
            print("Voter has already voted or does not exist.")

    def display_results(self):
        sql = '''SELECT * FROM candidates;'''
        cursor = self.conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        for row in rows:
            print(f"Candidate: {row[1]} | Votes: {row[2]}")

    def close_connection(self):
        self.conn.close()


def main():
    system = OnlineVotingSystem()

    while True:
        print("1. Register Voter\n2. Cast Vote\n3. Display Results\n4. Exit")
        choice = int(input("Choose an option: "))

        if choice == 1:
            name = input("Enter voter name: ")
            voter_card = input("Enter voter card: ")
            system.register_voter(name, voter_card)

        elif choice == 2:
            voter_card = input("Enter voter card: ")
            candidate_id = int(input("Enter candidate ID: "))
            system.cast_vote(voter_card, candidate_id)

        elif choice == 3:
            system.display_results()

        elif choice == 4:
            system.close_connection()
            print("Exiting...")
            break

        else:
            print("Invalid option. Try again.")


if __name__ == "__main__":
    main()
