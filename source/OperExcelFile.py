'''
Created on 2017年2月28日

@author: zhangzhiyuan
本程序来源于网上,用于操作excel文件
'''
# -*- coding: utf-8 -*-
# import  xdrlib ,sys
import xlrd
from dbconn import XGPDBConn


def open_excel(file='file.xls'):
    '''
    打开excel文件
    '''
    try:
        data = xlrd.open_workbook(file)
        return data
    except Exception:
        print(Exception)
# 根据索引获取Excel表格中的数据   参数:file：Excel文件路径     colnameindex：表头列名所在行的所以
# ，by_index：表的索引


def excel_table_byindex(file='file.xls', colnameindex=0, by_index=0):
    '''
    以索引方式读取excel文件，colnameindex为列索引，从0开始；by_index为sheets的索引，也是
    从0开始。
    '''
    data = open_excel(file)
    table = data.sheets()[by_index]
    nrows = table.nrows  # 行数
    # ncols = table.ncols  # 列数
    colnames = table.row_values(colnameindex)  # 某一行数据
    list = []
    for rownum in range(1, nrows):

        row = table.row_values(rownum)
        #list = list(map(lambda x, y: {x: y}, colnames, row))
        list.append(dict(zip(colnames, row)))
        '''
        if row:
            app = {}
            for i in range(len(colnames)):
                app[colnames[i]] = row[i]
            list.append(app)
        '''
        print(list)
    return list

# 根据名称获取Excel表格中的数据   参数:file：Excel文件路径     colnameindex：表头列名所在行的所以
# ，by_name：Sheet1名称


def excel_table_byname(file='file.xls', colnameindex=0, by_name=u'Sheet1'):
    '''
    以文件名和sheet名方式读取excel文件，by_name为文件file.xls中单个sheet页的名称
    '''
    data = open_excel(file)
    table = data.sheet_by_name(by_name)
    nrows = table.nrows  # 行数
    colnames = table.row_values(colnameindex)  # 某一行数据
    list = []
    for rownum in range(1, nrows):
        row = table.row_values(rownum)
        if row:
            app = {}
            for i in range(len(colnames)):
                app[colnames[i]] = row[i]
            list.append(app)
    return list


def main():
    '''
    程序执行入口函数，相当于c语言的主函数
    '''
    xgpdb = XGPDBConn(r'//192.168.80.100/xgp1', 'helios', 'helios')
    conn, cur = xgpdb.dbconn()
    tables = excel_table_byindex(
        r'C:\temp\result.xls', 0, 1)
    cur.execute('delete from wh_condition_config')
    for row in tables:
        cur.execute('INSERT INTO wh_condition_config  VALUES  (:1,:2,:3,:4)', [
            row['PROMOTION_CONDITION_ID'], row['CONDITION_CLASS'],
            row['CONDITION_TEXT'], row['DESC_TEXT']])
        # print(row)
        conn.commit()
    cur.close()
    conn.close()

    '''
    tables = excel_table_byname()
    for row in tables:
        print row
    '''
if __name__ == "__main__":
    main()
