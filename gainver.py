'''
Created on 2016年10月24日

@author: zhangzhiyuan
此模块用于获取各种版本信息
ver_type:1表示仅有实施文档的版本；2.获取应用一组高频库的程序版本；3.获取应用 所有组高频库程序版本号；4.获取高频归集库的版本号；5.获取高频二次验奖库的程序版本号
'''
import os
import pysvn
class GPVer:
    def __init__(self):
        self.nextver=''
        pass
    def f(self,s):
        ss= s.split('_')[1].replace('Build','')
        return ss
    def getVer(self,svn_path=r'D:\aeg2\Aegean2_update',ver_type=1):
        svn=pysvn.Client()
        svn.update(svn_path)
        #获取新工单的版本号
        #切换到决定工单下一版本的SVN目录
        os.chdir(svn_path)
        if ver_type in [1,2,3]:          
            cmd=r'dir Aeg2DB_Build*.doc? /B'
        elif ver_type==4:
            #高频归集库
            cmd=r'dir CLCTDB_Build* /B'
        elif ver_type==5:
            #二次验奖库
            cmd=r'dir Aeg2DBCheck_Build* /B'
            
        list_file=os.popen(cmd).readlines()
        list_file=list(map(self.f,list_file))        
        list_temp=map(lambda x:int(x.split('.')[0]),list_file)
        newVer='Build'+str(max(list_temp)).zfill(2)+'.'
        list_temp=map(lambda x:int(x.split('.')[1]),list_file)
        if ver_type==1:
            #仅实施文档的版本号
            newVer=newVer+str(max(list_temp)+1)+'.0'
        elif ver_type==2:
            #应用于一组高频库的版本号
            newVer=newVer+str(max(list_temp)+1)+'.30.1.0'
        elif ver_type==3:
            #应用于所有组高频库的版本号
            newVer=newVer+str(max(list_temp)+1)+'.10.1.0'
        elif ver_type==4:
            newVer=newVer+str(max(list_temp)+1).zfill(3)+'.4.1.0'
            pass
        elif ver_type==5:
            #高频二次验奖库
            newVer=newVer+str(max(list_temp)+1).zfill(3)+'.1.0'
            pass
        self.nextver=newVer
        return self.nextver

if __name__=='__main__':
    gv=GPVer()
    gv.getVer(svn_path=r'D:\高频归集\trunk\script\update',ver_type=4)