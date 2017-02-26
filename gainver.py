'''
Created on 2016年10月24日

@author: zhangzhiyuan
此模块用于获取各种版本信息
ver_type:1表示仅有实施文档的版本；2.获取应用一组高频库的程序版本；3.获取应用 所有组高频库程序版本号；4.获取高频归集库的版本号；5.获取高频二次验奖库的程序版本号
'''
import os
import pysvn
class GPVer:
    '''
    用于获取高频SVN版本信息的类
    '''
    def __init__(self,svn_path,ver_type):
        '''
        初始化函数
            ver_typ:用5位表示，第1位表示实施文档;第2位表示单组高频库；第3位表示多组高频库；
            第4位表示高频归集库；第5位表示高频计奖验证库。每位用1表示需要版本，0表示不需要版本。
        '''
        self.gpver_input_dict={
            'svn_path':svn_path,
            'ver_typ':list(map(lambda x: int(x), ver_type)), #将ver_type的5位字符转换为整数后放到一个列表中
            }
        self.gpver_output_dict={
             'doc_ver':'', #仅有实施文档时的版本            
             'one_group_ver':'',#仅一组数据库程序包的版本
              'all_group_ver':'', #所有组数据库程序包的版本
             'clctgp_ver':'',#高频归集库的版本
             'pvdb_ver':'',#计奖验证库的版本
            }
    def svn_update(self):
        '''
        更新SVN目录，保持本地目录与SVN服务器目录版本一致
        '''
        client=pysvn.Client()
        client.update(self.gpver_input_dict['svn_path'])
    def get_ver(self):
        '''
        获取SVN下一个新的版本号
        '''
        os.chdir(self.gpver_input_dict['svn_path'])
        list_file=os.popen('dir Aeg2DB_*.doc? /B').readlines()
        list_file=list(map(lambda x: x.split('_')[1].strip('Build'),list_file))
        ver=[0,0]
        for i in list_file:
            li_i=list(map(lambda x: int(x),i.split('.')[0:2]))
            if li_i>ver:
                ver=li_i
        ver[1]=ver[1]+1
        #获取到两位的新的版本号
        new_ver=str(ver[0])+'.'+str(ver[1])
        
        #获取文档版本号
        if self.gpver_input_dict['ver_typ'][0]==1 :
            if sum(self.gpver_input_dict['ver_typ'])==1:
                 self.gpver_output_dict['doc_ver']='Build'+new_ver+'.0'
            else:
                self.gpver_output_dict['doc_ver']='Build'+new_ver
        
        #获取单组高频库的版本号
        if self.gpver_input_dict['ver_typ'][1]==1:
            self.gpver_output_dict['one_group_ver']='Build'+new_ver+'.30.1.0'
        
        #获取多组高频库的版本号
        if self.gpver_input_dict['ver_typ'][2]==1:
            if self.gpver_input_dict['ver_typ'][1]==1:
                self.gpver_output_dict['all_group_ver']='Build'+new_ver+'.10.2.0'
            else:
                self.gpver_output_dict['all_group_ver']='Build'+new_ver+'.10.1.0'
        
        #获取高频计奖验证库的版本号
        if self.gpver_input_dict['ver_typ'][4]==1:
             list_file=os.popen('dir Aeg2DBCheck_* /B').readlines()
             list_file=list(map(lambda x: x.split('_')[1][5:],list_file))
             ver=[0,0,0,0]
             for i in list_file:
                 list_i=i.split('.')
                 list_i=list(map(lambda x: int(x),list_i))
                 if list_i>ver:
                     ver=list_i
             ver[1]=ver[1]+1
             self.gpver_output_dict['pvdb_ver']='Build'+str(ver[0]).zfill(2)+'.'+str(ver[1]).zfill(3)+'.'+str(ver[2])+'.'+str(ver[3])
        

if __name__ == '__main__':
    gv = GPVer(svn_path=r'D:\aeg2\Aegean2_update', ver_type='11101')
    gv.svn_update()
    gv.get_ver()
    for (k,v) in gv.gpver_output_dict.items():
        print(k+':'+v)
    #gv.get_ver(svn_path=r'D:\aeg2\Aegean2_update', ver_type=1)
    print("The program is end.")
