import sqlite3


class sqlite3_plus(object):
    def __init__(self, **args):
        self.path = args['Path']
        self.tables = args['Tab']
        self.cmd = ''
        self.rows = []

    def _json(self, **args):
        data_arr = []
        for x in range(len(args['values'])):
            tmp = {}
            for i in range(len(args['keys'])):
                tmp[args['keys'][i]] = args['values'][x][i]
            data_arr.append(tmp)
        return data_arr

    def _tables_row(self):
        connect = sqlite3.connect(self.path)
        cursor = connect.cursor()
        cursor.execute("PRAGMA table_info('"+self.tables+"')")
        res = cursor.fetchall()
        for x in res:
            self.rows.append(x[1])
        connect.commit()
        connect.close()

    def find(self, **args):
        connect = sqlite3.connect(self.path)
        cursor = connect.cursor()
        if args and len(args) < 2:
            for x in args:
                self.cmd = 'select * from ' + self.tables + \
                    ' where ' + x + ' like \'%{}%\''.format(args[x])
        else:
            self.cmd = "select* from " + self.tables
        cursor.execute(self.cmd)
        data = cursor.fetchall()
        self._tables_row()
        result = self._json(keys=self.rows, values=data)
        connect.commit()
        connect.close()
        return result

    def delete(self, **args):
        connect = sqlite3.connect(self.path)
        cursor = connect.cursor()
        tmp = []
        for x in args:
            if type(args[x]) == list:
                for i in range(len(args[x])):
                    tmp.append(args[x][i])
            if len(tmp) > 0:
                self.cmd = 'DELETE FROM '+self.tables + ' WHERE ' + \
                    x+' in('+",".join(str(x) for x in tmp)+')'
            else:
                self.cmd = 'DELETE FROM '+self.tables + \
                    ' WHERE '+x+' in('+args[x]+')'
        cursor.execute(self.cmd)
        res = cursor.fetchall()
        connect.commit()
        connect.close()
        return res

    def add(self, **args):
        connect = sqlite3.connect(self.path)
        cursor = connect.cursor()
        tmp_key = []
        tmp_value = []
        placeholder = []
        self._tables_row()
        for x in args['Data']:
            if x in self.rows and x != 'ID':
                tmp_key.append(x)
                placeholder.append('?')
                tmp_value.append(args['Data'][x])
        self.cmd = "INSERT INTO "+self.tables + \
            " ("+",".join(str(x) for x in tmp_key)+") VALUES (" + \
            ",".join(str(x) for x in placeholder)+")"
        cursor.execute(self.cmd, tmp_value)
        res = cursor.fetchall()
        connect.commit()
        connect.close()
        return res

    def update(self, **args):
        connect = sqlite3.connect(self.path)
        cursor = connect.cursor()
        tmp_value = []
        placeholder = []
        self._tables_row()
        for x in args['Data']:
            if x in self.rows:
                placeholder.append(x+'=?')
                tmp_value.append(args['Data'][x])
        for x in args:
            if x != 'Data':
                tmp_value.append(args[x])
                self.cmd = "UPDATE "+self.tables+" SET " + \
                    ",".join(str(x) for x in placeholder) + \
                    " where "+x+" = ?"
        cursor.execute(self.cmd,tmp_value)
        res = cursor.fetchall()
        connect.commit()
        connect.close()
        return res
