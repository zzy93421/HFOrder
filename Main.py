'''
Created on 2016年10月23日

@author: Administrator
'''
from GeneralOrderOnlyDoc import GeneralOrderOnlyDoc
if __name__=="__main__":
    #工单类型:1.仅需实施文档的普通工单；2.需要程序和实施文档的普通工单；3.促销类工单；4.关键业务工单；5.UMP查询模块；
    while True:
        order_type=input('''请选择工单类型(默认为2)：
                1.仅需实施文档的普通工单；
                2.需要程序和实施文档的普通工单；
                3.促销类工单；
                4.关键业务工单；
                5.UMP查询模块；\n输入1-5选择：''').strip()
        
        if order_type=='1':
            #处理仅需要实施文档的工单
            order=GeneralOrderOnlyDoc()
            order.input()
            order.writeDoc()
            break
            pass
        elif order_type=='2':
            break
            pass
        elif order_type=='3':
            break
            pass
        elif order_type=='4':
            break
            pass
        elif order_type=='5':
            break
            pass
        else:
            print('你的选择结果不正确！')
    print('程序执行完毕！')