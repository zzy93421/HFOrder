'''
Created on 2016年10月23日

@author: 张志远
    本模块为顶层框架部分，主要用于接收用户的输入，及初始化一部分变量
'''
from dbconn import Sqlite3Conn
class HFOrder:
    '''
    高频工单类
    '''
    hf_dict = {
        # 工单编号
        'order_no':'',
        # 工单名称
        'order_name':'',
        # 研发人员信息 RD表示Research & Development
        'rd_person_name':'',
        'rd_person_phone':'',
        'rd_person_mobilephone':'',
        # 研发负责人信息
        'rd_manager_name':'',
        'rd_manager_phone':'',
        'rd_manager_mobilephone':'',
        }

    db_range = {
        'one':'',
        'all':'',
        'clctdb':'',
        'pvdb':'',
        }
    dbgroup_time = {'XGP11':'00:01',
                    'XGP21':'00:01',
                    'XGP31':'02:05',
                    'XGP41':'02:05',
                    'XGP61':'22:00',
                    'XGP71':'02:05',
                   }
    db_one = ['', 'XGP11', 'XGP21', 'XGP31', 'XGP41', '', 'XGP61', 'XGP71']
    db_user = {'XGP11':'helios',
               'XGP21':'helios',
               'XGP31':'helios',
               'XGP41':'helios',
               'XGP61':'helios',
               'XGP71':'helios',
               'CLCTGP':'aeg2',
               'AEGEAN2':'xgp_check',
              }
    def __init__(self):
        self.sqtdb = Sqlite3Conn()
        self.sqtdb.new_connect()
    def exit(self):
        '''
        退出函数
        '''
        self.sqtdb.new_connect()
    def input(self):
        '''
        输入函数，用于接收用户输入
        '''
        # 输入工单共用的信息
        self.hf_dict['order_no'] = input('请输入工单编号：\n').strip()
        self.hf_dict['order_name'] = input('请输入工单名称：\n').strip()
        # 选择研发人员信息，从DB读取
        sql = 'select id,name,phone,mobilephone,role from developer'
        self.sqtdb.sqlite3_cur.execute(sql)
        record_set = self.sqtdb.sqlite3_cur.fetchall()
        print('ID'.ljust(5) + 'name'.ljust(8) + 'phone'.ljust(8) + \
              'mobilephone'.ljust(15) + 'role'.ljust(12),)
        i = 0
        id_list = []
        for record in record_set:
            i += 1
            print(str(i).ljust(5) + record[1].ljust(10) + record[2].ljust(8) + \
                  record[3].ljust(15) + record[4].ljust(12),)
            id_list.append(str(i))
            if record[4] == 'manager':
                self.hf_dict['rd_manager_name'] = record[1]
                self.hf_dict['rd_manager_phone'] = record[2]
                self.hf_dict['rd_manager_mobilephone'] = record[3]
        # 生成研发人员信息
        result = ''
        while True:
            result = input('请输入ID值选择研发人员信息（默认值ID=1）：').strip()
            if len(result) == 0:
                result = '1'
                break
            else:
                if result not in id_list:
                    print('你的输入不正确，请从ID：' + ','.join(id_list) + '中进行选择！')
                else:
                    break
        i = int(result) - 1
        self.hf_dict['rd_person_name'] = record_set[i][1]
        self.hf_dict['rd_person_phone'] = record_set[i][2]
        self.hf_dict['rd_person_mobilephone'] = record_set[i][3]

        # 确认工单实施的某一组数据库
        while True:
            result = input('''请选择需要操作的某组高频数据库：
                1.XGP11;
                2.XGP21;
                3.XGP31;
                4.XGP41;
                6.XGP61;
                7.XGP71;
                0.不需要在某组高频库执行。\n请从0、1、2、3、4、6、7中选择一组：''').strip()
            if result not in ['0', '1', '2', '3', '4', '6', '7']:
                print('你的选择不正确！')
            else:
                self.db_range['one'] = self.db_one[int(result)]
                break
        # 确认工单是否有在所有组高频库执行的操作
        result = input('该工单是否有在所有组高频库执行的操作（输入Y或N,默认为N）?\n请输入：').strip()
        if result.upper() == 'Y':
            self.db_range['all'] = 'XGP11,XGP21,XGP31,XGP41,XGP61,XGP71'

        # 确认工单是否需要在高频归集库上执行
        result = input('该工单是否有在高频归集库执行的操作（输入Y或N,默认为N）?\n请输入：').strip()
        if result.upper() == 'Y':
            self.db_range['clctdb'] = 'CLCTGP'

        # 确认工单是否需要在二次验奖库上执行
        result = input('该工单是否有在高频二次验奖库执行的操作（输入Y或N,默认为N）?\n请输入：').strip()
        if result.upper() == 'Y':
            self.db_range['pvdb'] = 'Aegean2'

if __name__ == "__main__":
    try:
        HF_ORDER = HFOrder()
        HF_ORDER.input()
    finally:
        HF_ORDER.exit()
