'''
Created on 2015年9月17日

@author: zhang zhiyuan
'''
import sqlite3
# import cx_Oracle

class Sqlite3Conn:
    '''
    连接sqlite3的通用类
    '''
    def __init__(self, dbfile=r'D:\HFOrder\high_frequence.db'):
        self.dbstr = dbfile
        self.sqlite3_conn = sqlite3.connect(self.dbstr)
        self.sqlite3_cur = self.sqlite3_conn.cursor()

    def disconn_sqlite3(self):
        '''
        断开sqlite3数据库
        '''
        self.sqlite3_cur.close()
        self.sqlite3_conn.commit()
        self.sqlite3_conn.close()

    def new_connect(self):
        '''
        建立新的sqlite3数据库连接
        '''
        self.sqlite3_conn = sqlite3.connect(self.dbstr)
        self.sqlite3_cur = self.sqlite3_conn.cursor()
        