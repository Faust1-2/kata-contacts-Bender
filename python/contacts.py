import random
import string
import sys
import sqlite3
from pathlib import Path
from datetime import datetime


class Contacts:
    def __init__(self, db_path):
        self.db_path = db_path
        if not db_path.exists():
            print("Migrating db")
            connection = sqlite3.connect(db_path)
            cursor = connection.cursor()
            cursor.execute(
                """
                CREATE TABLE contacts(
                  id INTEGER PRIMARY KEY,
                  name TEXT NOT NULL,
                  email TEXT NOT NULL
                )
              """
            )
            connection.commit()
        self.connection = sqlite3.connect(db_path)
        self.connection.row_factory = sqlite3.Row

    def batch_generator(self, generator, batch_size):
        batch = []

        for item in generator:
            batch.append(item)
            if len(batch) == batch_size:
                yield batch
                batch = []

        # Yield any remaining items as the last batch
        if batch:
            yield batch

    def insert_contacts(self, contacts):
        BATCH_SIZE = 10000
        print("Inserting contacts ...")
        cursor = self.connection.cursor()
        for contact_batch in self.batch_generator(contacts, BATCH_SIZE):
            for contact in contact_batch:
                cursor.execute(
                    """
                    INSERT INTO contacts(name, email)
                    VALUES (?, ?)
                    """,
                    contact,
                )
            self.connection.commit()

    def get_name_for_email(self, email):
        print("Looking for email", email)
        cursor = self.connection.cursor()
        start = datetime.now()
        cursor.execute(
            """
            SELECT * FROM contacts
            WHERE email = ?
            """,
            (email,),
        )
        row = cursor.fetchone()
        end = datetime.now()

        elapsed = end - start
        print("query took", elapsed.microseconds / 1000, "ms")
        if row:
            name = row["name"]
            print(f"Found name: '{name}'")
            return name
        else:
            print("Not found")


def yield_contacts(num_contacts):
    yield ("Alice", "alice@domain.tld")
    yield ("Bob", "bob@foo.com")
    yield ("Charlie", "charlie@acme.corp")

    for _ in range(num_contacts - 3):
        char_num = random.randint(3, 10)
        name = ''.join(random.choice(string.ascii_letters) for _ in range(char_num))
        yield (name, f"{name}@random.com")


def main():
    num_contacts = int(sys.argv[1])
    db_path = Path("contacts.sqlite3")
    contacts = Contacts(db_path)
    contacts.insert_contacts(yield_contacts(num_contacts))
    charlie = contacts.get_name_for_email("charlie@acme.corp")


if __name__ == "__main__":
    main()
