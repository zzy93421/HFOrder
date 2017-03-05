'''
Created on 2015年9月17日

@author: zhang zhiyuan

'''
import sqlite3

import cx_Oracle


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


class XGPDBConn():
    '''
             连接高频数据库类
    '''

    def __init__(self, tns, username, password):
        self.xgpdbconn_input_dict = {
            'username': ('helios' if not username else username),
            'password': ('helios' if not password else password),
            'tns': (r'//192.168.80.21/xgp1' if not tns else tns),
        }
        self.xgpdbconn_output_dict = {
            'conn': '',
            'cur': '',
        }

    def dbconn(self):
        self.xgpdbconn_output_dict['conn'] = cx_Oracle.connect(self.xgpdbconn_input_dict[
                                                               'username'], self.xgpdbconn_input_dict['password'],
                                                               self.xgpdbconn_input_dict['tns'])
        self.xgpdbconn_output_dict[
            'cur'] = self.xgpdbconn_output_dict['conn'].cursor()
        return self.xgpdbconn_output_dict['conn'], self.xgpdbconn_output_dict['cur']

if __name__ == '__main__':
    xgpdb = XGPDBConn(r'//192.168.80.100/xgp1', 'helios', 'helios')
    conn, cur = xgpdb.dbconn()
    print(conn.version)
