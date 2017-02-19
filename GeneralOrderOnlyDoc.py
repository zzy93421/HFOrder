'''
Created on 2016年10月23日

@author: 张志远
功能说明：本模块用于处理'仅需实施文档的普通工单'
'''
import os,shutil
from gainver import GPVer
from HFOrder import HFOrder
from win32com.client import Dispatch
import configparser
class GeneralOrderOnlyDoc(HFOrder):
    order_dict={
                'DocName':'',
                'DocTemplateFile':r'D:\HFOrder\template\template_general_only_doc.docx',
                'DocPath':'D:\\aeg2\\Aegean2_update',
                'Version':'',
                }
    def input(self):
        conf_use=input('是否要用配置文件代替输入？\n输入Y或N：').strip().upper()
        if conf_use=='Y':
            conf_file_name=input('请输入配置文件 的路径及文件名称：\n').strip().replace('\\', '\\\\')
            cfg=configparser.ConfigParser() 
            cfg.read(conf_file_name)
            for kvs in cfg.items('hf_dict'):
                self.hf_dict[kvs[0]]=kvs[1]
            for kvs in cfg.items('db_range'):
                self.db_range[kvs[0]]=kvs[1]
        elif conf_use=='N':
            super().input()
            #将输入生成conf文件
            conf_file_name=self.hf_dict['order_no']+'.conf'
            cfg=configparser.ConfigParser()            
            cfg.add_section('hf_dict')
            for key in self.hf_dict.keys():
                cfg.set('hf_dict',key,self.hf_dict[key])
                pass
            cfg.add_section('db_range')
            for key in self.db_range.keys():
                cfg.set('db_range',key,self.db_range[key])
            cfg.write(open(conf_file_name,'w'))
            
        
    def writeDoc(self):
        #获取文档版本号
        gv=GPVer()
        self.order_dict['Version']=gv.getVer(self.order_dict['DocPath'],1)
        #self.order_dict['Version']=gv.getVer()
        
        #获取实施文档名称
        self.order_dict['DocName']='Aeg2DB_'+str(self.order_dict['Version'])+'_'+self.hf_dict['order_name']+'_实施文档.docx'
        #从模板生成实施文档
        try:
            os.chdir(self.order_dict['DocPath'])
            practice_file=os.path.join(self.order_dict['DocPath'],self.order_dict['DocName'])
            shutil.copy(self.order_dict['DocTemplateFile'],practice_file)
            #用当前的信息替换模板信息     
            w=Dispatch('Word.Application')
            w.Visible=0
            w.DisplayAlerts=0
            doc=w.Documents.Open(practice_file)      
            w.Selection.Find.ClearFormatting()
            w.Selection.Find.Replacement.ClearFormatting()
            for key in self.hf_dict.keys():
                w.Selection.Find.Execute('{'+key+'}',False,False,False,False,False,True,1,True,self.hf_dict[key],2)
            #生成实施文档的数据库更新部分
            tab=doc.Tables[1]
            #doc.Tables[1].Rows[1].Cells[1].Select()
            i=len(tab.Rows)-1
            #tab.Rows.Add()     
            #生成高频归集库的实施部分  
            if len(self.db_range['clctdb'])>0:
                tab.Rows[i].Cells[1].Range.Text='pl/sql登录\n填入相关信息'                
                tab.Rows[i].Cells[2].Range.Text='用户名：aeg2\n数据库：CLCTGP'
                tab.Rows[i].Cells[4].Range.Text='22:00'
                '''
                tab.Rows.Add()
                i+=1
                #备份表和插入版本记录
                file=open(r'D:\HFOrder\template\backup_tab_and_record_ver.sql','r')
                backup_sql=file.read()
                file.close()
                backup_sql=backup_sql.replace('{order_name}',self.hf_dict['order_name'])
                backup_sql=backup_sql.replace('{order_no}',self.hf_dict['order_no'])
                backup_sql=backup_sql.replace('{developer}',self.hf_dict['rd_person_name'])
                backup_sql=backup_sql.replace('{version}',self.order_dict['Version'])                
                backup_tab_str=input('请输入高频归集库需要备份的表，每项之间用“,”分隔,无需备份则不输入:').strip()
                if len(backup_tab_str)==0:
                    backup_sql=backup_sql.replace("p_all_backup_tables(p_tab_list =>'{backup_tab_list}' , p_title => v_task_name)","--p_all_backup_tables(p_tab_list =>'{backup_tab_list}")
                else:
                    backup_sql=backup_sql.replace('{backup_tab_list}',backup_tab_str)
                file=open('backup_and_ver.sql','w')
                file.write(backup_sql)
                file.close()
                tab.Rows[i].Cells[1].Range.Text='执行备份和记录版本SQL'
                tab.Rows[i].Cells[2].Select()
                a=w.Selection
                a.InlineShapes.AddOLEObject(ClassType='SQL',FileName=os.path.join(self.order_dict['DocPath'],'backup_and_ver.sql')) 
                os.remove(os.path.join(self.order_dict['DocPath'],'backup_and_ver.sql'))               
                '''
                tab.Rows.Add()
                i+=1
                tab.Rows[i].Cells[1].Range.Text='执行变更SQL脚本' 
                update_file=input('输入高频归集库变更SQL脚本文件的全路径文件名称：\n').strip() 
                update_file=update_file.replace('\\','\\\\')               
                if len(update_file)>0:
                    tab.Rows[i].Cells[2].Select()
                    a=w.Selection
                    a.InlineShapes.AddOLEObject(ClassType='SQL',FileName=update_file) 
                
                tab.Rows.Add()
                i+=1
                tab.Rows[i].Cells[1].Range.Text='执行检查SQL'                
                #tab.Rows[i].Cells[2].Range.Text='用户名：aeg2\n数据库：CLCTGP'
                #tab.Rows[i].Cells[2].Range.Text='用户名：aeg2\n数据库：CLCTGP'
            
            #生成某组高频库的实施部分
            if len(self.db_range['one'])>0:
                if len(tab.Rows[i].Cells[1].Range.Text.strip())==0:
                    tab.Rows.Add()
                i=len(tab.Rows)-1
                #生成PLSQL登录信息
                tab.Rows[i].Cells[1].Range.Text='pl/sql登录\n填入相关信息'                
                tab.Rows[i].Cells[2].Range.Text='用户名：helios\n数据库：'+self.db_range['one']
                while True:
                    operator_time=input('选择第'+self.db_range['one']+'组高频库操作开始时间：\n'+'1.非长奖期时间：22:00\n2.长奖期时间：'+self.dbgroup_time[self.db_range['one']]).strip()
                    if operator_time=='1':
                        operator_time='22:00'
                        break
                    elif operator_time=='2':
                        operator_time=self.dbgroup_time[self.db_range['one']]
                        break
                    else:
                        print('你的选择不正确，请输入1或2进行选择！')
                tab.Rows[i].Cells[4].Range.Text=operator_time
                #生成备份表和插入版本记录
                tab.Rows.Add()
                i+=1
                file=open(r'D:\HFOrder\template\backup_tab_and_record_ver.sql','r')
                backup_sql=file.read()
                file.close()
                backup_sql=backup_sql.replace('{order_name}',self.hf_dict['order_name'])
                backup_sql=backup_sql.replace('{order_no}',self.hf_dict['order_no'])
                backup_sql=backup_sql.replace('{developer}',self.hf_dict['rd_person_name'])
                backup_sql=backup_sql.replace('{version}',self.order_dict['Version'])                
                backup_tab_str=input('请输入高频归集库需要备份的表，每项之间用“,”分隔,无需备份则不输入:').strip()
                if len(backup_tab_str)==0:
                    backup_sql=backup_sql.replace("p_all_backup_tables(p_tab_list =>'{backup_tab_list}' , p_title => v_task_name)","--p_all_backup_tables(p_tab_list =>'{backup_tab_list}")
                else:
                    backup_sql=backup_sql.replace('{backup_tab_list}',backup_tab_str)
                file=open('backup_and_ver.sql','w')
                file.write(backup_sql)
                file.close()
                tab.Rows[i].Cells[1].Range.Text='执行备份和记录版本SQL'
                tab.Rows[i].Cells[2].Select()
                a=w.Selection
                a.InlineShapes.AddOLEObject(ClassType='SQL',FileName=os.path.join(self.order_dict['DocPath'],'backup_and_ver.sql')) 
                os.remove(os.path.join(self.order_dict['DocPath'],'backup_and_ver.sql')) 
                
                #生成某组高频库的更新操作步骤
                tab.Rows.Add()
                i+=1
                  
                pass
            #print(len(tab.Rows))
            #生成所有组高频库的实施部分
            #生成某组高频库的实施部分
        finally:
            doc.Close()
            w.Quit()
            pass
        pass