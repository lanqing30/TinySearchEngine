import sqlite3
import os

class SQL(object):
    def __init__(self, data_base_name):

        if os.path.exists(data_base_name):
            os.remove(data_base_name)
            print('original db {} has been removed.'.format(data_base_name))

        self.conn = sqlite3.connect(data_base_name)
        self.conn.execute('''CREATE TABLE WORDS
            (ID TEXT PRIMARY KEY NOT NULL,
            VAL TEXT NOT NULL);''')

    def Insert(self, word, lister):
        """insert a tuple（word，a list of page which contains the word)."""
        try:
            lister = [str(x) for x in lister]
            tar = ','.join(lister)
            cmd = "INSERT INTO WORDS (ID, VAL) VALUES ('" + word + "', '" + tar + "')"
            self.conn.execute(cmd)
            self.conn.commit()
        except:
            print(word, lister, ' Failed to insert...')

    def Retrieve(self, word):
        ret_seq = self.conn.execute("SELECT * FROM WORDS WHERE ID = '" + word + "'")
        final_list = []
        for item in ret_seq:
            tmp_str = item[1]
            str_list = tmp_str.split(',')
            int_list = [int(x) for x in str_list]
            for x in int_list:
                final_list.append(x)
        return final_list

    def Close(self):
        self.conn.close()

