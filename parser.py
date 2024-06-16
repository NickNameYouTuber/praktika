import os
import re
import sqlite3
from datetime import datetime
import configparser

LOG_PATTERN = r'(?P<ip>\S+) (?P<client>\S+) (?P<user>\S+) \[(?P<time>.*?)\] "(?P<request>.*?)" (?P<status>\d+) (?P<size>\S+)'


def parse_logs():
    # Read config file
    config = configparser.ConfigParser()
    config.read('config.ini')

    # Get data from config
    files_dir = os.path.abspath(config['settings']['files_dir'])
    ext = config['settings']['ext']
    db_path = config['database']['db']
    format_pattern = config['settings']['format']

    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    for file_name in os.listdir(files_dir):
        if file_name.endswith(ext):
            with open(os.path.join(files_dir, file_name), 'r') as file:
                for line in file:
                    log_data = parse_log_line(line, format_pattern)
                    if log_data:
                        save_to_db(log_data, cursor, connection)

    connection.close()


def parse_log_line(line, format_pattern):
    match = re.match(LOG_PATTERN, line)
    if match:
        log_data = match.groupdict()
        log_data['time'] = datetime.strptime(log_data['time'], format_pattern).isoformat()
        log_data['size'] = int(log_data['size']) if log_data['size'] != '-' else 0
        return log_data
    return None


def save_to_db(log_data, cursor, connection):
    cursor.execute(
        "SELECT COUNT(*) FROM logs WHERE ip=? AND date=? AND request=? AND status=? AND size=?",
        (log_data['ip'], log_data['time'], log_data['request'], log_data['status'], log_data['size'])
    )
    count = cursor.fetchone()[0]

    if count == 0:
        cursor.execute(
            "INSERT INTO logs (ip, date, request, status, size) VALUES (?, ?, ?, ?, ?)",
            (log_data['ip'], log_data['time'], log_data['request'], log_data['status'], log_data['size'])
        )
        connection.commit()
