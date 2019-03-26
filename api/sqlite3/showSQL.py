import sqlite3
'''
Example

sql_show_tab(Path='../../sql/data.db',Tab='users_info',username='admin',cols=['name'])
'''
def sql_show_tab(**A):
    if 'Path' in A.keys() and A['Path'] != '' and A['Path'] != [] and A['Path'] != None:
        connect = sqlite3.connect(A['Path'])
        cursor = connect.cursor()
        tables_rows = []
        cols = []
        res = ''
        if ('Tab' in A.keys() and A['Tab'] != '' and A['Tab'] != [] and A['Tab'] != None):
            search_tables = "select name from sqlite_master where name =?"
            cursor.execute(search_tables, [A['Tab']])
            data = cursor.fetchall()
            if data!=[]:             
                tables=''  
                for x in data[0]:
                    if x == A['Tab']:
                        tables = x                
                search_tables_rows = "PRAGMA table_info('"+tables+"')"
                cursor.execute(search_tables_rows)
                data = cursor.fetchall()
                for x in data:
                    tables_rows.append(x[1])
                if ('cols' in A.keys()):
                    for x in range(len(A['cols'])):
                        if A['cols'][x] in tables_rows:
                            cols.append(A['cols'][x])
                        else:
                            return 'Parameter error ,Please try again !'
                    cols = ",".join(str(x) for x in cols)
                else:
                    cols = '*'
                tar = []
                tar_val = []
                search_tables_data = ''
                for x in A:
                    if x in tables_rows:
                        tar.append(x+'=?')
                        tar_val.append(A[x])
                if len(A)>2 and len(A)<4:
                    target = ",".join(str(x) for x in tar)
                    search_tables_data = "select "+cols+" from "+tables+" where "+target
                    cursor.execute(search_tables_data, tar_val)
                elif len(A)>3:
                    target = " and ".join(str(x) for x in tar)
                    search_tables_data = "select "+cols+" from "+tables+" where "+target
                    cursor.execute(search_tables_data, tar_val)
                else:
                    search_tables_data = "select "+cols+" from "+tables
                    cursor.execute(search_tables_data)
                res = cursor.fetchall()
                connect.commit()
                connect.close()
                return res
            else:
                return 'table name is not true !'
        else:
            return 'what is name of db tables ?'
    else:
        return 'where is db Path ?'
