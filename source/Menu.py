'''
Created on 2017年3月5日

@author: 张志远
'''


import pandas as pd


class Menu():
    '''
    整个软件的菜单结构
    '''

    def __init__(self, cur):
        '''
        Constructor
        '''
        self.menu_dict = {}
        self.cur = cur
        sql_str = 'SELECT t.id, t.name, nvl(t.parent_id,0) parent_id, t.module_name, t.class_name, t.method_name FROM menu_list t '
        self.cur.execute(sql_str)
        rs = self.cur.fetchall()
        self. df = pd.DataFrame(
            rs, index=range(1, len(rs) + 1),  columns=['id', 'name', 'parent_id', 'module_name', 'class_name', 'method_name'])
        # print(self.df)

    def get_menu_list(self, parent_id=0):
        '''
        依据输入的parent_id，获取子菜单列表，当其为0时，获取根菜单
        '''
        menu_level = self.df[self.df['parent_id'] == parent_id]
        return menu_level
        # print(menu_level0['name'])