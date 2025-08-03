# coding=utf-8

import os

import psycopg2
import requests

db_url = os.environ["DATABASE_URL"]

if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)

connection = psycopg2.connect(db_url, sslmode="require")
cursor = connection.cursor()
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS users (
        id BIGINT PRIMARY KEY,
        username TEXT,
        password TEXT
    );
    """
)
connection.commit()


class Instapaper(object):

    def __init__(self, user_id):
        cursor.execute("SELECT username, password FROM users WHERE id = %s;", (user_id,))

        data = cursor.fetchone()

        self._username, self._password = data if data else (None, None)
        self._user_id = user_id
        self._url = 'https://www.instapaper.com/api/'

    def auth(self, username, password) -> int:
        """
        Authorizes user.
        :param username: User's username or email.
        :param password: User's password.
        :return: Status code as an integer (200, 403, 500).
        """
        self._username = username
        self._password = password

        data = {
            'username': username,
            'password': password
        }

        response = requests.get(self._url + 'authenticate', params=data)

        if response.status_code == 200:
            try:
                cursor.execute("INSERT INTO users VALUES (%s, %s, %s);", (self._user_id, username, password))

            except psycopg2.IntegrityError:
                cursor.execute(
                    "UPDATE users SET username = %s, password = %s WHERE id = %s;",
                    (username, password, self._user_id),
                )

            connection.commit()

        return response.status_code

    def add(self, url) -> int:
        """
        Adds url to an Instapaper account.
        :param url: URL that should be saved.
        :return: Status code as an integer (201, 400, 403, 500).
        """
        data = {
            'username': self._username,
            'password': self._password,
            'url': url
        }

        response = requests.get(self._url + 'add', params=data)

        return response.status_code

    def is_authorized(self) -> bool:
        """
        Checks if the user is authorized.
        """
        return bool(self._username)
