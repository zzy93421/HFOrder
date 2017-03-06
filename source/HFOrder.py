'''
Created on 2016年10月23日

@author: 张志远
    本模块为顶层框架部分，主要用于接收用户的输入，及初始化一部分变量
'''

import pandas as pd


class HFOrder:
    '''
    高频工单类
    '''

    def __init__(self):
        '''
        初始化函数
        '''

    def input(self, cur, conn):
        '''
        输入函数，用于接收用户输入
       '''
        # 输入工单共用的信息
        order_no = input('请输入工单编号：\n').strip()
        order_name = input('请输入工单名称：\n').strip()

        # 选择研发人员信息，从DB读取
        self.cur = cur
        self.conn = conn
        sql = 'select id,name,telphone,mobilephone  from person'
        self.cur.execute(sql)
        rs = self.cur.fetchall()
        self.person_tab = pd.DataFrame(rs, index=range(
            1, len(rs) + 1), columns=['id', 'name', 'telphone', 'mobilephone'])
        # print(self.person_tab['id'][2])
        while True:
            print('请输入前面的数字，选择研发人员及研发负责人（例如：1,2）：')
            for row in self.person_tab.values:
                print("%5d %10s %6s %15s" % (row[0], row[1], row[2], row[3]))
            person = input('请选择（例如：1,2）:').strip()
            try:
                id_list = [int(x) for x in person.split(',')]
            except Exception:
                print('你的选择不正确，请重新选择！')
            if id_list[0] not in self.person_tab['id'] or id_list[1] not in self.person_tab['id'] or len(id_list) != 2:
                print('你的选择不正确，请重新选择！')
            else:
                print('你的选择如下：')
                print(
                    chr(9) + '研发人员：' + self.person_tab[self.person_tab['id'] == id_list[0]].values[0][1])
                print(
                    chr(9) + '研发负责人：' + self.person_tab[self.person_tab['id'] == id_list[1]].values[0][1])
                developer_id = id_list[0]
                manager_id = id_list[1]
            # 将工单信息保存到数据库表中
                sql = '''
            INSERT INTO work_order
  (order_no, order_name, doc_name, semente_no, deploy_date, time_estimate,
   attention, developer_id, manager_id)
VALUES
  (:order_no, :order_name, NULL, '运维补充', '运维补充', '30分钟', '长奖期内操作',
   :developer_id, :manager_id)
  '''
                self.cur.execute(
                    sql, (order_no, order_name, developer_id, manager_id))
                self.conn.commit()
                break

        # print(self.person_tab.values)
