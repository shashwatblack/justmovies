class DatabaseUtils():
    cursor = None

    def __init__(self, cursor):
        self.cursor = cursor

    def get_person(self, name):
        query = """SELECT * FROM person WHERE name='{}';""".format(name)
        self.cursor.execute(query)
        return self.cursor.fetchone()

    def insert_person(self, name, dob=None):
        if dob:
            query = """INSERT INTO person ("name", "dob") VALUES ('{}', '{}');""".format(name, dob)
        else:
            query = """INSERT INTO person ("name") VALUES ('{}');""".format(name)
        self.cursor.execute(query)

    def insert_then_get_person(self, name, dob=None):
        self.insert_person(name, dob)
        return self.get_person(name)

    def get_personal_role(self, person_pk, role):
        if isinstance(person_pk, tuple):
            person_pk = person_pk[0]
        query = """SELECT * FROM personal_role WHERE person='{}' and role='{}';""".format(person_pk, role)
        self.cursor.execute(query)
        return self.cursor.fetchone()

    def insert_role(self, person_pk, role):
        if isinstance(person_pk, tuple):
            person_pk = person_pk[0]
        query = """INSERT INTO personal_role ("person", "role") VALUES ('{}', '{}');""".format(person_pk, role)
        self.cursor.execute(query)


class MockCursor():
    def execute(self, query):
        print("EXECUTING", query)

    def fetchone(self):
        print("FETCH-ONE")
        return {}
