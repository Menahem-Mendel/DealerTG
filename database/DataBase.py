import sqlite3
from database.struc import *


class db_object(dict):
    ob_type = None

    def __init__(self, ob_id):
        super().__init__()

        # Setting up db
        self.conn = sqlite3.connect(filename)
        self.c = self.conn.cursor()

        # Declaring id and filling parameters
        for key in nav[self.ob_type]:
            self[key] = None

        self['id'] = ob_id

        # Loading user if id is declared
        if self['id'] is not None:
            self.load()

    def load(self):
        # Running select script and getting values
        script = f"SELECT * FROM {self.ob_type} WHERE (id='{self['id']}')"
        self.c.execute(script)
        values = self.c.fetchone()

        # Checking if object exists in db
        if values is None:
            raise Exception(f"{self.ob_type} {self['id']} not found!")

        # Filling db values
        keys = nav[self.ob_type]
        for i in range(len(keys)):
            self[keys[i]] = values[i]

    def save(self):
        # Creating id if needed
        if self['id'] is None:
            self.create_id()

        # Removing old object from db
        self.delete()

        # Setting and executing insert script
        spacers = str(["?" for i in self.keys()])[1:-1].replace("'", "")
        script = f"""INSERT INTO {self.ob_type} Values({spacers})"""
        self.c.execute(script, list(self.values()))
        self.conn.commit()
        return self['id']

    def delete(self):
        # Setting and executing delete script
        script = "DELETE FROM " + self.ob_type + \
            " WHERE id='" + self['id'] + "'"
        self.c.execute(script)
        self.conn.commit()

    def create_id(self):
        # Getting all objects from type
        script = f"SELECT * FROM {self.ob_type}"
        self.c.execute(script)
        results = self.c.fetchall()

        # Setting id to results len + 1
        self['id'] = str(len(results) + 1)

    def close(self):
        self.conn.close()
        del self


class User(db_object):
    ob_type = USERS

    def __init__(self, user_id=None):
        super().__init__(user_id)


class Deal(db_object):
    ob_type = DEALS

    def __init__(self, user_id=None):
        super().__init__(user_id)


class Commit(db_object):
    ob_type = COMMITS

    def __init__(self, user_id=None):
        super().__init__(user_id)


class FindDeals:

    def __init__(self, search_settings):
        self.search_settings = search_settings
        self.conn = sqlite3.connect(filename)
        self.c = self.conn.cursor()

    def find(self):
        search_settings = self.search_settings
        by_header = self.find_deals_by("headline", search_settings['text'])
        by_description = self.find_deals_by(
            "description", search_settings['text'])
        by_hashtags = self.find_deals_by("hashtags", search_settings['text'])

        header_score = 10
        description_score = 5
        hashtag_score = 3

        results = {}
        for deal in by_header:
            deal = deal[0]
            if deal not in results:
                results[deal] = header_score
            else:
                results[deal] += header_score

        for deal in by_description:
            deal = deal[0]

            if deal not in results:
                results[deal] = description_score
            else:
                results[deal] += description_score

        for deal in by_hashtags:
            deal = deal[0]

            if deal not in results:
                results[deal] = hashtag_score
            else:
                results[deal] += hashtag_score

        results = self.sort_results(results)
        return results

    def find_deals_by(self, by, text):
        script = f"SELECT id FROM deal WHERE({by} LIKE '%{text}%')"
        self.c.execute(script)
        results = self.c.fetchall()
        return results

    @staticmethod
    def sort_results(results: dict):
        results = list(results.items())
        results.sort(key=lambda x: x[1])
        results.reverse()
        results = [item[0] for item in results]
        return results
