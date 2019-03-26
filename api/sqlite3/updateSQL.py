import sqlite3
import json
'''
Example

sql_update_Data(Path='../../sql/user.db', Tab='users_info',Data={'name': 'sss'}, name='sss1')
'''


def sql_update_Data(**A):
    if 'Path' in A.keys() and A['Path'] != '' and A['Path'] != [] and A['Path'] != None:
        connect = sqlite3.connect(A['Path'])
        cursor = connect.cursor()
        tables_rows = []
        par = []
        val = []
        if ('Tab' in A.keys() and A['Tab'] != '' and A['Tab'] != [] and A['Tab'] != None):
            search_tables = "select name from sqlite_master where name =?"
            cursor.execute(search_tables, [A['Tab']])
            Data = cursor.fetchall()
            if Data != []:
                tables = ''
                for x in Data[0]:
                    if x == A['Tab']:
                        tables = x
                search_tables_rows = "PRAGMA table_info('"+tables+"')"
                cursor.execute(search_tables_rows)
                Data = cursor.fetchall()
                for x in Data:
                    tables_rows.append(x[1])
                if 'Data' in A.keys():
                    par_bak = []
                    Da = json.dumps(A['Data'])
                    Da = json.loads(Da)
                    for x in Da:
                        if x in tables_rows:    
                            par.append(x)
                            val.append(Da[x])
                    for i in range(len(par)):
                        if par[i] in tables_rows:
                            par_bak.append(par[i]+'=?')
                    key = ",".join(str(x) for x in par_bak)
                    a1 = []
                    a2 = []
                    target = ''
                    for x in A:
                        if x in tables_rows:
                            a1.append(x+'=?')
                            a2.append(A[x])
                            if len(A) < 5:
                                target=','.join(str(x) for x in a1)
                            else:                            
                                target=' and '.join(str(x) for x in a1)
                    add_sql_data = "UPDATE "+tables+" SET " + key + " where "+target
                    for x in a2: 
                        val.append(x)
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




