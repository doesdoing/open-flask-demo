import sqlite3
'''
Example


sql_del_data(Path='../../sql/data.db', Tab='users_info',Data={"ID":[123,123],"name":['asd','asd',123]})


'''


def sql_del_data(**A):
    if 'Path' in A.keys() and A['Path'] != '' and A['Path'] != [] and A['Path'] != None:
        connect = sqlite3.connect(A['Path'])
        cursor = connect.cursor()
        tables_rows = []
        if ('Tab' in A.keys() and A['Tab'] != '' and A['Tab'] != [] and A['Tab'] != None):
            search_tables = "select name from sqlite_master where name =?"
            cursor.execute(search_tables, [A['Tab']])
            D = cursor.fetchall()
            if D != []:
                tables = ''
                for x in D[0]:
                    if x == A['Tab']:
                        tables = x
                if tables == '':
                    print('err')
                search_tables_rows = "PRAGMA table_info('"+tables+"')"
                cursor.execute(search_tables_rows)
                D = cursor.fetchall()
                for x in D:
                    tables_rows.append(x[1])
                target = []
                values=[]
                if A['Data']:
                    for x in A['Data']:
                        if x in tables_rows:
                            print(x)
                            tmp = []
                            tmp1 = []
                            for i in range(len(A['Data'][x])):
                                tmp.append('?')
                                values.append(A['Data'][x][i])
                            tmp1 = ','.join(str(x) for x in tmp)
                            target.append(x+' in ('+tmp1+')')
                    del_tables_data=''
                    tar=''
                    if len(target) > 1:
                        tar = ' and '.join(str(x) for x in target)       
                    else:
                        tar = ''.join(str(x) for x in target)
                    del_tables_data = 'DELETE FROM '+tables+' WHERE '+tar
                    cursor.execute(del_tables_data, values)
                    connect.commit()
                    connect.close()   
                else:
                    return 'where is Data json ?'             
                '''
                        tmp = []
                        tmp1 = []
                        for i in range(len(A[x])):
                            tmp.append('?')
                            values.append(A[x][i])
                        tmp1 = ','.join(str(x) for x in tmp)
                        target.append(x+' in ('+tmp1+')')
                del_tables_data=''
                tar=''
                if len(target) > 1:
                    tar = ' and '.join(str(x) for x in target)       
                else:
                    tar = ''.join(str(x) for x in target)
                del_tables_data = 'DELETE FROM '+tables+' WHERE '+tar
                cursor.execute(del_tables_data, values)
                connect.commit()
                connect.close()
                '''
                '''
                if 'target' in A.keys() and 'val' in A.keys():
                    target = []
                    for x in A['target']:
                        if x in tables_rows:
                            target.append(x+' = ?')
                        else:
                            return 'target is not true !'
                    print(target)
                    if len(A['target']) < 1 :
                        target = ''.join(str(x) for x in target)
                    else:
                        target = ' and '.join(str(x) for x in target)
                    del_tables_data = 'DELETE FROM '+tables+' WHERE '+target
                    print(del_tables_data)
                    print(A['val'])
                    cursor.execute(del_tables_data, A['val'])
                    connect.commit()
                    connect.close()
                else:
                    return 'where is del target ?'
                    '''
            else:
                return 'table name is not true !'
        else:
            return 'what is name of db tables ?'
    else:
        return 'where is db Path ?'

