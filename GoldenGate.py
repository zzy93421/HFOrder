'''
Created on 2016年10月10日

@author: zhangzhiyuan
'''
from dbconn import Sqlite3Conn
import os,shutil,time
import win32com
from win32com.client import Dispatch
class GG:
    def __init__(self,tab_cre_sql_file,tab_str,source_db_str='XGP11#XGP21#XGP31#XGP41#XGP61#XGP71',gg_mode=1,source_db_type='gp'):
        '''
        tab_cre_sql_file:创建表的SQL文件名，包含目录路径，例如：D:\aeg2\table_structure\b_setmeal.sql
        tab_str:新增表的字符串，每张表之间用#分隔，例如新增表tab1、tab2、tab3则输入tab1#tab2#tab3
        source_db_str:源数据库的字符串，例如需要从源数据库xgp11、xgp21、xgp31，则输入xgp11#xgp21#xgp31
        gg_mode:golden操作模式，1表示新增表时配置goldengate，2表示修改表列（非主键列）时配置goldengate，此时只需重启goldengate
        '''
        
        self.tab_cre_sql_file=tab_cre_sql_file
        #print(self.tab_cre_sql_file)
        self.tab_list=tab_str.strip('#').split('#')
        self.source_db_list=source_db_str.upper().strip('#').split('#')
        self.source_db_list.sort()
        self.gg_mode=gg_mode
        #self.gg_file_path=r'C:\Users\zhangzhiyuan\Desktop'
        self.gg_file_path=r'C:\ggtest'
        self.gg_file_name=os.path.join(self.gg_file_path,'GoldenGate_' +time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))+'.docx')
        self.gg_template_file=r'D:\test\hf_template\GoldenGate_template_1.docx'
        
        #由source_db_type初始化source_db及target_db用户及数据库信息
        if source_db_type=='gp':
            self.db_info={
                          'source_user':'helios',
                          'source_db':'、'.join(self.source_db_list),
                          'target_user':'aeg2',
                          'target_db':'clctgp',
                          }
        else:
            self.db_info={
                          'source_user':'tiger',
                          'source_db':'、'.join(self.source_db_list),
                          'target_user':'tiger',
                          'target_db':'clct',
                          }
        self.db_sqlite=Sqlite3Conn()
        self.db_sqlite.new_connect()
        pass
    def witeGGDoc(self):
        try:
            shutil.copy(self.gg_template_file, self.gg_file_name)
            w=Dispatch('Word.Application')
            w.Visible=0
            w.DisplayAlerts=0
            doc=w.Documents.Open(self.gg_file_name)      
            w.Selection.Find.ClearFormatting()
            w.Selection.Find.Replacement.ClearFormatting()
            w.Selection.Find.Execute('{source_user}',False,False,False,False,False,True,1,True,self.db_info['source_user'],2)
            w.Selection.Find.Execute('{source_db}',False,False,False,False,False,True,1,True,self.db_info['source_db'],2)
            w.Selection.Find.Execute('{target_user}',False,False,False,False,False,True,1,True,self.db_info['target_user'],2)
            w.Selection.Find.Execute('{target_db}',False,False,False,False,False,True,1,True,self.db_info['target_db'],2) 
            doc.Save() 
            gg_tab=doc.Tables[0]
            #gg_tab.Rows.Add()
            #print('rowscount:'+str(gg_tab.Rows.Count))
            #将建表SQL文件嵌入到文档中
            gg_tab.Rows[2].Cells[2].Select()
            a=w.Selection
            a.InlineShapes.AddOLEObject(ClassType='SQL',FileName=self.tab_cre_sql_file)
            #将建表SQL文件嵌入到文档中
            doc.Tables[0].Rows[4].Cells[2].Select()
            a=w.Selection
            a.InlineShapes.AddOLEObject(ClassType='SQL',FileName=self.tab_cre_sql_file)
            
            
            for db in self.source_db_list:                
                self.db_sqlite.sqlite3_cur.execute("select * from goldengate_config where upper(source_db)=upper('%s')" % db)
                record=self.db_sqlite.sqlite3_cur.fetchone()                                  
                #在文档中生成停止源数据库extract进程和pumb进程的部分
                gg_tab.Rows.Add()
                i=gg_tab.Rows.Count-1
                #操作项
                gg_tab.Rows[i].Cells[1].Range.Text='停止'+db+'库的OGG进程'
                #操作内容
                str1='cd $GG_HOME\n./ggsci\nstop '+record[5]+'\nstop '+record[7]+'\ninfo all'
                gg_tab.Rows[i].Cells[2].Range.Text=str1
                #备注
                str1='info all的结果：\n'+record[5]+','+record[7]+'是STOP状态，表示正确。'
                gg_tab.Rows[i].Cells[3].Range.Text=str1
                
                #新的一行,即新表添加附加日志
                gg_tab.Rows.Add()
                i=gg_tab.Rows.Count-1
                #操作项：新表添加附加日志
                gg_tab.Rows[i].Cells[1].Range.Text='新表添加附加日志'
                #操作内容
                str1='dblogin userid ogg, password ogg\n'
                for tab in self.tab_list:
                    str1=str1+'add trandata '+record[2]+'.'+tab+'\n'
                    str1=str1+'info trandata '+record[2]+'.'+tab+'\n'
                    pass
                gg_tab.Rows[i].Cells[2].Range.Text=str1
                #备注
                gg_tab.Rows[i].Cells[3].Range.Text='info trandata 的结果：\n确认信息提示附加日志已经添加成功'
                
                #新的一行，extract进程配置更新
                gg_tab.Rows.Add()
                i=gg_tab.Rows.Count-1
                #操作项
                str1=record[5]+'配置更新'
                gg_tab.Rows[i].Cells[1].Range.Text=str1
                #操作内容
                str1='edit param '+record[5]
                gg_tab.Rows[i].Cells[2].Range.Text=str1
                #备注
                str1='追加如下内容并保存：\n'
                for tab in self.tab_list:
                    str1=str1+'table '+record[2]+'.'+tab+';\n'
                    pass
                gg_tab.Rows[i].Cells[3].Range.Text=str1
                
                #新的一行,pump进程配置更新
                gg_tab.Rows.Add()
                i=gg_tab.Rows.Count-1
                #操作项
                str1=record[7]+'配置更新'
                gg_tab.Rows[i].Cells[1].Range.Text=str1
                #操作内容
                str1='edit param '+record[7]
                gg_tab.Rows[i].Cells[2].Range.Text=str1
                #备注
                str1='追加如下内容并保存：\n'
                for tab in self.tab_list:
                    str1=str1+'table '+record[2]+'.'+tab+';\n'
                    pass
                gg_tab.Rows[i].Cells[3].Range.Text=str1
                    
                    
                pass
            #在目标数据库上停止应用进程，并检查进程状态
            #在目标数据库的第1节点上，停止应用进程
            str2="'"+"','".join(self.source_db_list)+"'"
            self.db_sqlite.sqlite3_cur.execute("select * from goldengate_config where target_home='$GG_HOME1' and upper(source_db)in (%s)" % str2)
            rows=self.db_sqlite.sqlite3_cur.fetchall()
            if len(rows)>0:
                gg_tab.Rows.Add()
                i=gg_tab.Rows.Count-1
                
                #操作项
                str1='停止%s库节点1的OGG进程' % self.db_info['target_db']
                gg_tab.Rows[i].Cells[1].Range.Text=str1
                #操作内容
                str1='cd $GG_HOME1\n./ggsci\n'
                
                str2=''
                for record in rows:
                    str1=str1+'stop '+record[14]+'\n'
                    str2=str2+'、'+record[14]
                    #print(record)
                    pass
                str2=str2.strip('、')
                gg_tab.Rows[i].Cells[2].Range.Text=str1+'info all'
                #备注
                gg_tab.Rows[i].Cells[3].Range.Text='info all的结果：\n'+str2+'是STOP状态，表示正确。'
                
                for rep_process in str2.split('、'):
                    gg_tab.Rows.Add()
                    i=gg_tab.Rows.Count-1
                    #操作项
                    str1= rep_process+'配置更新'
                    gg_tab.Rows[i].Cells[1].Range.Text=str1
                    #操作内容
                    str1='edit param '+rep_process
                    gg_tab.Rows[i].Cells[2].Range.Text=str1
                    #备注
                    str1='追加如下内容并保存：\n'
                    for tab in self.tab_list:
                        str1=str1+'map '+self.db_info['source_user']+'.'+tab+',target '+self.db_info['target_user']+'.'+tab+';\n'
                    gg_tab.Rows[i].Cells[3].Range.Text=str1
            
            #在目标数据库的第2节点上，停止应用进程
            str2="'"+"','".join(self.source_db_list)+"'"
            self.db_sqlite.sqlite3_cur.execute("select * from goldengate_config where target_home='$GG_HOME2' and upper(source_db)in (%s)" % str2)
            rows=self.db_sqlite.sqlite3_cur.fetchall()
            if len(rows)>0:
                gg_tab.Rows.Add()
                i=gg_tab.Rows.Count-1
                #操作项
                str1='停止%s库节点2的OGG进程' % self.db_info['target_db']
                gg_tab.Rows[i].Cells[1].Range.Text=str1
                #操作内容
                str1='cd $GG_HOME1\n./ggsci\n'
                
                str2=''
                for record in rows:
                    str1=str1+'stop '+record[14]+'\n'
                    str2=str2+'、'+record[14]
                    #print(record)
                    pass
                str2=str2.strip('、')
                gg_tab.Rows[i].Cells[2].Range.Text=str1+'info all'
                #备注
                gg_tab.Rows[i].Cells[3].Range.Text='info all的结果：\n'+str2+'是STOP状态，表示正确。'
                
                for rep_process in str2.split('、'):
                    gg_tab.Rows.Add()
                    i=gg_tab.Rows.Count-1
                    #操作项
                    str1= rep_process+'配置更新'
                    gg_tab.Rows[i].Cells[1].Range.Text=str1
                    #操作内容
                    str1='edit param '+rep_process
                    gg_tab.Rows[i].Cells[2].Range.Text=str1
                    #备注
                    str1='追加如下内容并保存：\n'
                    for tab in self.tab_list:
                        str1=str1+'map '+self.db_info['source_user']+'.'+tab+',target '+self.db_info['target_user']+'.'+tab+';\n'
                    gg_tab.Rows[i].Cells[3].Range.Text=str1
                    pass
            
            #启动源数据库的extract和pump进程
            for db in self.source_db_list:
                self.db_sqlite.sqlite3_cur.execute("select * from goldengate_config where upper(source_db)=upper('%s')" % db)
                record=self.db_sqlite.sqlite3_cur.fetchone()
                gg_tab.Rows.Add()
                i=gg_tab.Rows.Count-1
                #操作项
                str1='启动'+db+'库的OGG进程'
                gg_tab.Rows[i].Cells[1].Range.Text=str1
                #操作内容
                str1='cd $GG_HOME\n./ggsci\nstart '+record[5]+'\nstart '+record[7]+'\ninfo all'
                gg_tab.Rows[i].Cells[2].Range.Text=str1
                #备注
                str1='info all的结果：\n'+record[5]+','+record[7]+'是RUNNING状态，表示正确。'
                gg_tab.Rows[i].Cells[3].Range.Text=str1
                pass
            #启动目标库节点1的rep进程
            str1='cd $GG_HOME1\n./ggsci\n'
            str2="'"+"','".join(self.source_db_list)+"'"
            self.db_sqlite.sqlite3_cur.execute("select * from goldengate_config where target_home='$GG_HOME1' and upper(source_db)in (%s)" % str2)
            rows=self.db_sqlite.sqlite3_cur.fetchall()
            #print(len(rows))
            str2=''
            if len(rows)>0:
                gg_tab.Rows.Add()
                i=gg_tab.Rows.Count-1
                #操作项
                str1='启动'+self.db_info['target_db']+'库节点1的OGG进程'
                gg_tab.Rows[i].Cells[1].Range.Text=str1
                #操作内容
                str1='cd $GG_HOME\n./ggsci\n'
                for record in rows:
                    str1=str1+'start '+record[14]+'\n'
                    str2=str2+'、'+record[14]
                    pass
                str1=str1+'info all'
                gg_tab.Rows[i].Cells[2].Range.Text=str1
                #备注
                str2='info all的结果：\n'+str2.strip('、')+'是RUNNING状态，表示正确。'
                gg_tab.Rows[i].Cells[3].Range.Text=str2
            
            #启动目标库节点2的rep进程
            str1='cd $GG_HOME1\n./ggsci\n'
            str2="'"+"','".join(self.source_db_list)+"'"
            self.db_sqlite.sqlite3_cur.execute("select * from goldengate_config where target_home='$GG_HOME2' and upper(source_db)in (%s)" % str2)
            rows=self.db_sqlite.sqlite3_cur.fetchall()
            #print(len(rows))
            str2=''
            if len(rows)>0:
                gg_tab.Rows.Add()
                i=gg_tab.Rows.Count-1
                #操作项
                str1='启动'+self.db_info['target_db']+'库节点1的OGG进程'
                gg_tab.Rows[i].Cells[1].Range.Text=str1
                #操作内容
                str1='cd $GG_HOME\n./ggsci\n'
                for record in rows:
                    str1=str1+'start '+record[14]+'\n'
                    str2=str2+'、'+record[14]
                    pass
                str1=str1+'info all'
                gg_tab.Rows[i].Cells[2].Range.Text=str1
                #备注
                str2='info all的结果：\n'+str2.strip('、')+'是RUNNING状态，表示正确。'
                gg_tab.Rows[i].Cells[3].Range.Text=str2
            
            doc.Save()
        finally:
            doc.Close()
            w.Quit()
    pass

if __name__=='__main__':
    gg=GG(tab_cre_sql_file=r'D:\aeg2\table_structure\log_rng.sql',tab_str='log_rng')
    gg.witeGGDoc()
    print('程序已执行完毕！')
    pass