#!/usr/bin/env python3
"""log filter"""

import re
import os
import logging
import mysql.connector
from typing import List


PII_FIELDS = ("name", "ssn", "email", "password", "phone")


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class"""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    """def format(self, record: logging.LogRecord) -> str:
        print("Message type:", type(record.msg))
        print("Message value:", record.msg)
        record.msg = filter_datum(self.fields, self.REDACTION, record.msg, self.SEPARATOR)
        return super().format(record)"""

    def format(self, record: logging.LogRecord) -> str:
        """Formats a record with class Redactformatter"""
        if not isinstance(record.msg, str):
            # Convert record.msg to a string
            record.msg = str(record.msg)
        record.msg = filter_datum(self.fields, self.REDACTION, record.msg, self.SEPARATOR)
        return super().format(record)



def filter_datum(
        fields: List[str],
        redaction: str,
        message: str,
        separator: str) -> str:
    """return an obfuscated message"""
    for field in fields:
        # Substitute field values with redaction string
        # r'\b' matches exact field strings
        # re.escape(field) removes special char if any
        # r'=*.? matches chars few times as possible and
        # (?={}$) looks ahead to match chars before end of line
        message = re.sub(r'\b' + re.escape(field) + r'=.*?(?={}|$)'
                .format(re.escape(separator)),
                field + '=' + redaction, message)
    return message.replace(' ', separator)


def get_logger() -> logging.Logger:
    """A function that gets a logging data"""
    # creates a logger object called user_data
    user_data = logging.getLogger('user_data')
    user_data.setLevel(logging.INFO)

    # console handler
    stream_handler = logging.StreamHandler()

    # This formatter uses our class defined formatter
    formatter = RedactingFormatter(PII_FIELDS)
    stream_handler.setFormatter(formatter)

    # Add stream handler to logger
    user_data.addHandler(stream_handler)

    return user_data


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Accesses a db for data"""
    username = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    password = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    db_name = os.getenv('PERSONAL_DATA_DB_NAME')
    host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')

    return mysql.connector.connect(user=username, password=password, database=db_name, host=host)


def main():
    """main function"""
    logger = get_logger()
    connector = get_db()

    cursor = connector.cursor()

    cursor.execute("SELECT * FROM users;")

    rows = cursor.fetchall()

    for row in rows:
        res = [item for item in row]
        message = f"name={res[0]};email={res[1]};phone={res[2]};ssn={res[3]};password={res[4]};ip={res[5]};last_login={res[6]};user_agent={res[7]}"
        logger.info(message)

    cursor.close()

    connector.close()


if __name__ == '__main__':
    main()
