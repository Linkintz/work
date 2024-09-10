import psycopg2

sql = ''


def get_sql(sql):
    conn = psycopg2.connect(database='test_db', user='test_user',
                            password='abc123', host='192.168.15.79', port=5432)
    cursor = conn.cursor()
    cursor.execute(sql)
    value = cursor.fetchall()
    conn.close()
    return value


def exc_sql(sql):
    conn = psycopg2.connect(database='test_db', user='test_user',
                            password='abc123', host='192.168.15.79', port=5432)
    cursor = conn.cursor()
    cursor.execute(sql)
    cursor.execute('commit')
    conn.close()


def main(sql,prn = False):
    if prn:
        print(sql)
    if 'select' in sql.lower():
        value = get_sql(sql)
        # print(value)
        return value
    else:
        exc_sql(sql)


if __name__ == '__main__':
    main(sql)
