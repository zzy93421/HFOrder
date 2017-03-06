'''
Created on 2016年10月23日

@author: Administrator
'''
#import pandas

from configparser import SafeConfigParser

from Menu import Menu
from dbconn import XGPDBConn
from menufunc import MenuActivity as MA


if __name__ == '__main__':
    # 读取配置信息
    config = SafeConfigParser()
    config.read(r'..\conf\config.ini')
    tns = config.get('XGP1_DB', 'tns')
    username = config.get('XGP1_DB', 'username')
    password = config.get('XGP1_DB', 'password')

    # 建立到XGP1数据库连接
    db = XGPDBConn(tns, username, password)
    conn, cur = db.dbconn()

    # 显示根菜单
    menu = Menu(cur)
    df = menu.get_menu_list(parent_id=0)
    while True:
        print('请输入每项前面的数字选择工作内容：')
        for i in df.index:
            print(' ' * 10 + str(i) + '.' + df.values[i - 1][1])
        sel = input('请选择：').strip()
        if sel in [str(x) for x in df.index]:
            current_index = int(sel) - 1
            break
        else:
            print('你的选择不正确，请输入前面的数字选择！')
    ma = MA(df.values[current_index][3], df.values[
            current_index][4], df.values[current_index][5])
    ma.call_method(cur, conn)
    conn.commit()
    # print(df.values[current_index][3])

    # 关闭数据库连接
    db.dbdisconn()
    print('程序已正常结束运行！')
