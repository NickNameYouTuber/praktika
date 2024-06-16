import sqlite3

def view_logs(start_date=None, end_date=None, filter=None, filter_value=None):
    connection = sqlite3.connect('log_aggregator.db')
    cursor = connection.cursor()

    query = "SELECT * FROM logs WHERE 1=1"
    params = []

    if start_date:
        query += " AND date >= ?"
        params.append(start_date)
    if end_date:
        query += " AND date <= ?"
        params.append(end_date)
    if filter and filter_value:
        query += f" AND {filter} = ?"
        params.append(filter_value)

    cursor.execute(query, params)

    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    return rows
