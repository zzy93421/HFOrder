'''
Created on 2017年3月5日

@author: 张志远
'''


class MenuActivity():
    '''
    动态调用菜单关联的模块、类及方法
    '''

    def __init__(self, module_name, class_name, method_name):
        '''
        初始化函数，接收输入的模块、类及方法
        '''
        self.module_name = module_name
        self.class_name = class_name
        self.method_name = method_name

    def call_method(self, cur, conn):
        '''
        动态调用方法
        '''
        self.current_module = __import__(self.module_name)
        self.current_class = getattr(self.current_module, self.class_name)
        self.current_method = getattr(self.current_class, self.method_name)
        self.current_method(self, cur, conn)
