import sqlite3
import json
'''
Example

sql_add_data(Path='../../sql/Data.db', Tab='users_info',Data={'username': 'asda', 
'password': '123', 'name': '123', 'level': 'admin', 'ip': '123', 'cookies': '123'})
'''


def sql_add_data(**A):
    if 'Path' in A.keys() and A['Path'] != '' and A['Path'] != [] and A['Path'] != None:
        connect = sqlite3.connect(A['Path'])
        cursor = connect.cursor()
        tables_rows = []
        if ('Tab' in A.keys() and A['Tab'] != '' and A['Tab'] != [] and A['Tab'] != None):
            search_tables = "select name from sqlite_master where name =?"
            cursor.execute(search_tables, [A['Tab']])
            Data = cursor.fetchall()
            if Data != []:
                tables = ''
                for x in Data[0]:
                    if x == A['Tab']:
                        tables = x
                if tables == '':
                    print('err')
                search_tables_rows = "PRAGMA table_info('"+tables+"')"
                cursor.execute(search_tables_rows)
                Data = cursor.fetchall()
                for x in Data:
                    tables_rows.append(x[1])
                if 'Data' in A.keys():
                    par = []
                    val = []
                    V = []
                    for x in A['Data']:
                        if x in tables_rows and x != "ID":
                            print(x)
                            par.append(x)
                            val.append(A['Data'][x])
                            V.append('?')
                    values = ",".join(str(x) for x in par)
                    keys = ",".join(str(x) for x in V)
                    add_sql_data = "INSERT INTO "+tables + \
                        " ("+values+") VALUES ("+keys+")"
                    print(add_sql_data)
                    cursor.execute(add_sql_data, val)
                    connect.commit()
                    connect.close()
                else:
                    return 'where is update Data ?'
            else:
                return 'table name is not true !'
        else:
            return 'what is name of db tables ?'
    else:
        return 'where is db Path ?'


