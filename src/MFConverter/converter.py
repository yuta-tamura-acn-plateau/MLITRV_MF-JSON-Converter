import configparser
import datetime
import csv
import re
from sqlite3 import Date
import time
import os
import json
from datetime import datetime
from xml.dom.minidom import Element

import xml.etree.ElementTree as ET
from xmlrpc.client import Boolean
import pandas as pd
import threading
from concurrent.futures import ThreadPoolExecutor

from Utils.Timer import timerClass
from PySide6.QtCore import QThread
import FormatData.MFJson as mf
import FormatData.DefinedFormat as dformat 

INI_FILE    = '\DefinedFormat.ini'
PARAM_PATH  = 'param_path'
PARAM_TYPE  = 'param_type'
DATE_FORMAT = 'date_format'



#============================================================================================
class ConverterClass(QThread):    
    lock = threading.Lock()
    p : str
    data_dict : dict     
    export_item_list : list
   
    progress = 0
    rows = 0
    progress_callback = None
    
    exitflag =False
    
    header_identifer : str
    
    datetime_format : str
    
    fixed_header_list : list
    floating_header_list : list
    len_fixed_headers : int
    len_floating_headers : int


    #============================================================================================
    def run(self):
        self.data_dict =dict()        
        self.do_convert(self.p)

    #============================================================================================
    def set_path(self,path):
        with self.lock:
            self.p=path
        return
        
    #============================================================================================
    def get_path(self)->str:
        with self.lock:
            res = self.p
        return res
            
    #============================================================================================
    def do_convert(self,path):
        ext = os.path.splitext(path)

        with self.lock:
            if ext[-1].casefold() =='.csv'.casefold():                
                if self.check_header_agoop(path):
                    print("convert agoop data")
                    self.convert_agoop(path)
                elif self.check_header_blog_watcher(path):
                    print("convert blog watcher data")
                    self.convert_blog_watcher(path)
                elif self.check_header_unerry(path):
                    print("convert unerry data")
                    self.convert_unerry(path)
                elif self.check_header_Template(path):
                    print("convert user Defined Format")
                    self.convert_template_csv(path)
                else:
                    print("unknown format")
            elif ext[-1].casefold()=='.json'.casefold():
                self.convert_template_json(path)
            elif ext[-1].casefold()=='.xml'.casefold():
                self.convert_template_xml(path)
            else:
                self.progress_callback(1)
                print("unknown format")
        self.progress_callback(1)
        self.p =''
        return

    #============================================================================================
    def count_csv_rows(self,path)->int:
        with open(path, 'r',encoding='utf-8') as file:
            reader = csv.reader(file)
            count = sum(1 for row in reader)
        return count
    
    #============================================================================================
    def check_header_agoop(self,path:str)->bool:
        with open(path,encoding='utf-8')as f:            
            headerLine = f.readline()
            headers = list(filter(None,re.split(',|\n',headerLine)))
            if not((len(dformat.agoop_header_list)>=len(headers)) and (len(headers)>=len(dformat.agoop_essential_list))):                
                return False

            for i in range(len(dformat.agoop_essential_list)):
                if dformat.agoop_header_list[i] in headers[i]:
                    continue
                else:
                    return False
            
            self.fixed_header_list    = list()
            self.floating_header_list = list()
                
            for header in headers:
                if header in dformat.agoop_header_list:
                    if header in dformat.agoop_timeline_items:
                        self.floating_header_list.append(header)
                    elif header in dformat.agoop_reserved_items:
                        pass
                    else:
                        self.fixed_header_list.append(header)
                    continue
                else:
                    return False
                
            self.len_fixed_headers    = len(self.fixed_header_list)
            self.len_floating_headers = len(self.floating_header_list)
            
            return True
    
    #============================================================================================
    def check_header_blog_watcher(self,path:str)->bool:
        with open(path,encoding='utf-8')as f:            
            headerLine = f.readline()
            headers = re.split(',|\n',headerLine)
            
            self.header_identifer = ""
            for i in range(len(dformat.blogwatcer_identifier_list)):
                if dformat.blogwatcer_identifier_list[i] in headers:
                    self.header_identifer = dformat.blogwatcer_identifier_list[i]
                    break                

            if self.header_identifer == "":
                return False
                
            self.fixed_header_list    = list()
            self.floating_header_list = list()
            
            for i in range(len(headers)-1):
                if headers[i] in dformat.blogwatcer_header_list:
                    if headers[i] in dformat.blogwatcher_timleine_items:
                        self.floating_header_list.append(headers[i])
                    elif headers[i] in dformat.blogwatcher_fixed_items:
                        self.fixed_header_list.append(headers[i])
                    elif headers[i] in dformat.blogwatcer_reserved_items:
                        pass
                    else:
                         self.fixed_header_list.append(headers[i]) 
                    continue
                else:
                    return False
                
            self.len_fixed_headers    = len(self.fixed_header_list)
            self.len_floating_headers = len(self.floating_header_list)
            return True
        
    #============================================================================================
    def check_header_unerry(self,path:str)->bool:
        with open(path,encoding='utf-8')as f:            
            headerLine = f.readline()
            headers = list(filter(None,re.split(',|\n',headerLine)))
            if not((len(dformat.unerry_header_list)>=len(headers)) and (len(headers)>=len(dformat.unerry_essential_list))):                
                return False

            for header in dformat.unerry_essential_list:
                if header in headers:
                    continue
                else:
                    return False            
            
            self.fixed_header_list    = list()
            self.floating_header_list = list()
            
            for header in headers:
                if header in dformat.unerry_header_list:
                    if header in dformat.unerry_timleine_items:
                        self.floating_header_list.append(header)
                    elif header in dformat.unerry_reserved_items:
                        pass
                    else:
                        self.fixed_header_list.append(header)
                    continue
                else:
                    return False
                
            self.len_fixed_headers    = len(self.fixed_header_list)
            self.len_floating_headers = len(self.floating_header_list)
            
            self.header_identifer = ''
            for header in dformat.unerry_identifier_list:
                if header in headers:
                    self.header_identifer = header
            if self.header_identifer == '':
                return False
            
            return True
        
    #============================================================================================
    def check_header_Template(self,path:str)->bool:
        cfg = configparser.RawConfigParser()
        cfg.read(os.getcwd()+INI_FILE,'UTF-8')
        
        with open(path,encoding='utf-8')as f:          
            header = f.readline()
            obj = list(filter(None,re.split(',|\n',header)))            
                    
            for section in dformat.template_essential_list_in_csv:
                if not section in cfg.sections():
                    print(section+' is not Defined')
                    return False
                for key,value in cfg.items(section):
                    if key ==PARAM_PATH:
                        if value in obj:
                            break
                    print(section+' param is not find in '+ os.path.splitext(os.path.basename(path))[0])
                    return False
            return True                      
    

    #Convert Each Row
    #============================================================================================
    def parse_agoop(self,x)->str:
        if self.exitflag == True:
            return
        id = x["dailyid"]
        if not id in self.data_dict:
            new_dict = dict()
            d_list = list()
            new_dict[mf.KEY_PROPERTIES]   = {mf.KEY_NAME: id}
            new_dict[mf.KEY_TYPE]         = mf.CONST_TYPE_MOVINGFEATURES
            new_dict[mf.KEY_TMP_GEOMETRY] ={mf.KEY_INTERPOLATE : mf.CONST_INTERPOLATE_LINEAR, 
                                            mf.KEY_TYPE        : mf.CONST_GEOMETRY_TYPE_POINT,
                                            mf.KEY_COORDINATES : list(),
                                            mf.KEY_DATETIMES   : d_list}
            tmp_property = list() 
            tmp_property.append({mf.KEY_NAME : "os",              mf.KEY_VALUES : x["os"]})#0
            tmp_property.append({mf.KEY_NAME : "home_countryname",mf.KEY_VALUES : x["home_countryname"]})#1
            tmp_property.append({mf.KEY_NAME : "plmn",            mf.KEY_VALUES : x["plmn"]})#2
            tmp_property.append({mf.KEY_NAME : "plmn_countryname",mf.KEY_VALUES : x["plmn_countryname"]})#3
            tmp_property.append({mf.KEY_NAME : "setting_currency",mf.KEY_VALUES : x["setting_currency"]})#4
            tmp_property.append({mf.KEY_NAME : "setting_language",mf.KEY_VALUES : x["setting_language"]})#5
            tmp_property.append({mf.KEY_NAME : "setting_country", mf.KEY_VALUES : x["setting_country"]})#6
            tmp_property.append({mf.KEY_NAME : "logtype_category",mf.KEY_VALUES : x["logtype_category"]})#7
            tmp_property.append({mf.KEY_NAME : "logtype_subcategory",mf.KEY_VALUES : x["logtype_subcategory"]})#8
                        
            if "home_prefcode" in x:
                tmp_property.append({mf.KEY_NAME : "home_prefcode",mf.KEY_VALUES : x["home_prefcode"]})#26
            if "home_citycode" in x:
                tmp_property.append({mf.KEY_NAME : "home_citycode",mf.KEY_VALUES : x["home_citycode"]})#27
            if "workplace_prefcode" in x:   
                tmp_property.append({mf.KEY_NAME : "workplace_prefcode",mf.KEY_VALUES : x["workplace_prefcode"]})#28
            if "workplace_citycode" in x:
                tmp_property.append({mf.KEY_NAME : "workplace_citycode",mf.KEY_VALUES : x["workplace_citycode"]})#29
            if "gender" in x:
                tmp_property.append({mf.KEY_NAME : "gender",mf.KEY_VALUES : x["gender"]})#30
                
            tmp_property.append({mf.KEY_NAME : "accuracy",                mf.KEY_VALUES : list(), mf.KEY_DATETIMES : d_list})#18
            tmp_property.append({mf.KEY_NAME : "speed",                   mf.KEY_VALUES : list(), mf.KEY_DATETIMES : d_list})#19
            tmp_property.append({mf.KEY_NAME : "estimated_speed_flag",    mf.KEY_VALUES : list(), mf.KEY_DATETIMES : d_list})#20
            tmp_property.append({mf.KEY_NAME : "course",                  mf.KEY_VALUES : list(), mf.KEY_DATETIMES : d_list})#21
            tmp_property.append({mf.KEY_NAME : "estimated_course_flag",   mf.KEY_VALUES : list(), mf.KEY_DATETIMES : d_list})#22
            tmp_property.append({mf.KEY_NAME : "prefcode",                mf.KEY_VALUES : list(), mf.KEY_DATETIMES : d_list})#23
            tmp_property.append({mf.KEY_NAME : "citycode",                mf.KEY_VALUES : list(), mf.KEY_DATETIMES : d_list})#24
            tmp_property.append({mf.KEY_NAME : "mesh100mid",              mf.KEY_VALUES : list(), mf.KEY_DATETIMES : d_list})#25
            
            new_dict[mf.KEY_TMP_PROPERTIES] = tmp_property
            self.data_dict[id] = new_dict
            print(id)        
            
        date = datetime(year   = int(x["year"]),
                                 month  = int(x["month"]),
                                 day    = int(x["day"]),
                                 hour   = int(x["hour"]),
                                 minute = int(x["minute"]),
                                 second = 0)
        self.data_dict[id][mf.KEY_TMP_GEOMETRY][mf.KEY_COORDINATES].append([x["latitude"],x["longitude"]])       
        
        tmp_property = self.data_dict[id][mf.KEY_TMP_PROPERTIES]

        tmp_property[self.len_fixed_headers][mf.KEY_DATETIMES].append(date.strftime('%Y-%m-%dT%H:%M:%SZ'))
        
        tmp_property[self.len_fixed_headers][mf.KEY_VALUES].append(x["accuracy"])
        tmp_property[self.len_fixed_headers+1][mf.KEY_VALUES].append(x["speed"])
        tmp_property[self.len_fixed_headers+2][mf.KEY_VALUES].append(x["estimated_speed_flag"])      
        tmp_property[self.len_fixed_headers+3][mf.KEY_VALUES].append(x["course"])
        tmp_property[self.len_fixed_headers+4][mf.KEY_VALUES].append(x["estimated_course_flag"])       
        tmp_property[self.len_fixed_headers+5][mf.KEY_VALUES].append(x["prefcode"])                
        tmp_property[self.len_fixed_headers+6][mf.KEY_VALUES].append(x["citycode"]) 
        tmp_property[self.len_fixed_headers+7][mf.KEY_VALUES].append(x["mesh100mid"])
        
        self.progress = self.progress+1
        self.progress_callback(self.progress/self.rows)
        
        return
 
    
    #============================================================================================
    def parse_blog_watcher(self,x)->str:
        if self.exitflag == True:
            return
        id = x[self.header_identifer]
        if not id in self.data_dict:
            new_dict = dict()
            d_list = list()
            new_dict[mf.KEY_PROPERTIES]   = {mf.KEY_NAME: id}
            new_dict[mf.KEY_TYPE]         = mf.CONST_TYPE_MOVINGFEATURES
            new_dict[mf.KEY_TMP_GEOMETRY] ={mf.KEY_INTERPOLATE : mf.CONST_INTERPOLATE_LINEAR, 
                                            mf.KEY_TYPE        : mf.CONST_GEOMETRY_TYPE_POINT,
                                            mf.KEY_COORDINATES : list(),
                                            mf.KEY_DATETIMES   : d_list}
            tmp_property = list()

            
            for i in range(len(self.floating_header_list)):
                tmp_property.append({mf.KEY_NAME      : self.floating_header_list[i],
                                     mf.KEY_VALUES    : list(), 
                                     mf.KEY_DATETIMES : d_list})#3                
            
            
            for i in range(len(self.fixed_header_list)):    
                tmp_property.append({mf.KEY_NAME   : self.fixed_header_list[i], 
                                     mf.KEY_VALUES : x[self.fixed_header_list[i]]})#0            

            new_dict[mf.KEY_TMP_PROPERTIES] = tmp_property
            self.data_dict[id] = new_dict
            print(id)        
            
        self.data_dict[id][mf.KEY_TMP_GEOMETRY][mf.KEY_COORDINATES].append([x["latitude_anonymous"],x["longitude_anonymous"]])       
        
        tmp_property = self.data_dict[id][mf.KEY_TMP_PROPERTIES]
       
        date = datetime.strptime(str(x["datetime"]), '%Y-%m-%d %H:%M:%S') 
        tmp_property[0][mf.KEY_DATETIMES].append(date.strftime('%Y-%m-%dT%H:%M:%SZ'))
        
        for i in range(len(self.floating_header_list)):
            tmp_property[i][mf.KEY_VALUES].append(x[self.floating_header_list[i]])                  
            
        self.progress = self.progress+1
        self.progress_callback(self.progress/self.rows)
        return
    
    #============================================================================================
    def parse_unerry(self,x)->str:
        if self.exitflag == True:
            return
        id = x[self.header_identifer]
        if not id in self.data_dict:
            new_dict = dict()
            d_list = list()
            new_dict[mf.KEY_PROPERTIES]   = {mf.KEY_NAME: id}
            new_dict[mf.KEY_TYPE]         = mf.CONST_TYPE_MOVINGFEATURES
            new_dict[mf.KEY_TMP_GEOMETRY] ={mf.KEY_INTERPOLATE : mf.CONST_INTERPOLATE_LINEAR, 
                                            mf.KEY_TYPE        : mf.CONST_GEOMETRY_TYPE_POINT,
                                            mf.KEY_COORDINATES : list(),
                                            mf.KEY_DATETIMES   : d_list}
            tmp_property = list()
            if "adid" in x:
                tmp_property.append({mf.KEY_NAME : "adid",         mf.KEY_VALUES : x["adid"]})#0
            if "extra_id_1" in x:
                tmp_property.append({mf.KEY_NAME : "extra_id_1",   mf.KEY_VALUES : x["extra_id_1"]})#1
            if "extra_id_2" in x:
                tmp_property.append({mf.KEY_NAME : "extra_id_2",   mf.KEY_VALUES : x["extra_id_2"]})#2
            tmp_property.append({mf.KEY_NAME : "category_id",  mf.KEY_VALUES : x["category_id"]})#3
            tmp_property.append({mf.KEY_NAME : "category_name",mf.KEY_VALUES : x["category_name"]})#4
            tmp_property.append({mf.KEY_NAME : "brand_id",     mf.KEY_VALUES : x["brand_id"]})#5
            tmp_property.append({mf.KEY_NAME : "brand_name",   mf.KEY_VALUES : x["brand_name"]})#6
            tmp_property.append({mf.KEY_NAME : "poi_id",       mf.KEY_VALUES : x["poi_id"]})#7            
            tmp_property.append({mf.KEY_NAME : "poi_name",     mf.KEY_VALUES : x["poi_name"]})#8
            
            if "prefecture_code" in x:
                tmp_property.append({mf.KEY_NAME : "prefecture",   "code" : list(), "name" : list(), mf.KEY_DATETIMES : d_list})#9
            if "prefecture_name" in x:
                tmp_property.append({mf.KEY_NAME : "city",         "code" : list(), "name" : list(), mf.KEY_DATETIMES : d_list})#10            

            
            new_dict[mf.KEY_TMP_PROPERTIES] = tmp_property
            self.data_dict[id] = new_dict
            print(id)        
            
        date = datetime.strptime(str(x["detected_on_jst"]), '%Y/%m/%d %H:%M')
        self.data_dict[id][mf.KEY_TMP_GEOMETRY][mf.KEY_COORDINATES].append([x["latitude"],x["longitude"]])                       
        self.data_dict[id][mf.KEY_TMP_GEOMETRY][mf.KEY_DATETIMES].append(date.strftime('%Y-%m-%dT%H:%M:%SZ')) 
        
        if self.len_floating_headers >0:
            tmp_property = self.data_dict[id][mf.KEY_TMP_PROPERTIES]
            i = 0
            if "prefecture_code" in x:
                print('fixed='+str(self.len_fixed_headers))
                print('len='+str(len(tmp_property[self.len_fixed_headers+i])))                
                tmp_property[self.len_fixed_headers+i]["code"].append(x["prefecture_code"])
                if "prefecture_name" in x:
                    tmp_property[self.len_fixed_headers+i]["name"].append(x["prefecture_name"])
                i +=1
            if "city_code" in x:
                tmp_property[self.len_fixed_headers+i]["code"].append(x["city_code"])      
                if "city_name" in x:
                    tmp_property[self.len_fixed_headers+i]["name"].append(x["city_name"])
                i +=1
        
        self.progress = self.progress+1
        self.progress_callback(self.progress/self.rows)
        return
    
    #============================================================================================
    def parse_template_csv(self,x)->str:   
        id = x[self.header_identifer]
        if not id in self.data_dict:
            new_dict = dict()
            d_list = list()
            new_dict[mf.KEY_PROPERTIES]   = {mf.KEY_NAME: id}
            new_dict[mf.KEY_TYPE]         = mf.CONST_TYPE_MOVINGFEATURES
            new_dict[mf.KEY_TMP_GEOMETRY] ={mf.KEY_INTERPOLATE : mf.CONST_INTERPOLATE_LINEAR, 
                                            mf.KEY_TYPE        : mf.CONST_GEOMETRY_TYPE_POINT,
                                            mf.KEY_COORDINATES : list(),
                                            mf.KEY_DATETIMES   : d_list}
            tmp_property = list()
            tmp_property.append({mf.KEY_NAME : "id",         mf.KEY_VALUES : x[self.header_identifer]})
            
            if "gender" in self.columnheaders:
                tmp_property.append({mf.KEY_NAME : "gender",  mf.KEY_VALUES : x[self.columnheaders['gender']]})
            if "age" in self.columnheaders:                
                tmp_property.append({mf.KEY_NAME : "age",mf.KEY_VALUES : x[self.columnheaders["age"]]})
            
            
            new_dict[mf.KEY_TMP_PROPERTIES] = tmp_property
            self.data_dict[id] = new_dict
            print(id) 
            
        datestr = str(x[self.columnheaders['year']])
        datestr = datestr +'-'+ str(x[self.columnheaders['month']])
        datestr = datestr +'-'+ str(x[self.columnheaders['day']])
        datestr = datestr +'-'+ str(x[self.columnheaders['hour']])
        datestr = datestr +'-'+ str(x[self.columnheaders['minute']])
        
        if "second" in self.columnheaders:
            datestr = datestr +'-'+ str(x[self.columnheaders['second']])
        else:
            datestr = datestr +'-00'
            
        
        date = datetime.strptime(datestr, self.datetime_format)
        
        self.data_dict[id][mf.KEY_TMP_GEOMETRY][mf.KEY_COORDINATES].append([x[self.columnheaders["latitude"]],x[self.columnheaders["longitude"]]])                       
        self.data_dict[id][mf.KEY_TMP_GEOMETRY][mf.KEY_DATETIMES].append(date.strftime('%Y-%m-%dT%H:%M:%SZ')) 
        
       
        self.progress = self.progress+1
        self.progress_callback(self.progress/self.rows)
        pass

#Convert       
    #============================================================================================
    def convert_agoop(self,path):
        timer = timerClass()
        timer.start() 
       
        self.rows = self.count_csv_rows(path)
        print('Row='+str(self.rows))
        self.export_item_list = list()
        df = pd.read_csv(path)
        df.sort_values([dformat.agoop_header_list[0],
                        dformat.agoop_header_list[1],
                        dformat.agoop_header_list[2],
                        dformat.agoop_header_list[3],
                        dformat.agoop_header_list[5],
                        dformat.agoop_header_list[6]],inplace = True)       
        df.apply(self.parse_agoop,axis=1)
        
        self.export_item_list = list(self.data_dict.values())
        print('collect_time = '+str(timer.lap()))
           
        file_name = os.path.splitext(os.path.basename(path))[0]
        export_file_path = os.path.dirname(path)+'/'+file_name+'.json'
        if os.path.isfile(export_file_path):
            pass
        
        with open(export_file_path, 'w') as f:
            json.dump(self.export_item_list, f, indent=2)
        self.progress_callback(1)
        print('progressTime= '+str(timer.stop()))
        
        return 
    
    #============================================================================================
    def convert_blog_watcher(self,path):
        timer = timerClass()
        timer.start()      
        print('Convert BlogWatcher Format')
        
        if not self.check_header_blog_watcher(path):
            return
        
        self.rows = self.count_csv_rows(path)
        print('Row='+str(self.rows))
        self.export_item_list = list()
        df = pd.read_csv(path)
        df.sort_values([self.header_identifer,dformat.blogwatcer_header_list[3]],inplace = True)
        df.apply(self.parse_blog_watcher,axis=1)
        self.export_item_list = list(self.data_dict.values())
        print('collect_time = '+str(timer.lap()))
        
        file_name = os.path.splitext(os.path.basename(path))[0]
        export_file_path = os.path.dirname(path)+'/'+file_name+'.json'
        
        if os.path.isfile(export_file_path):
            pass
        
        with open(export_file_path, 'w') as f:
            json.dump(self.export_item_list, f, indent=2)
        self.progress_callback(1)    
        print('progressTime= '+str(timer.stop()))
        return
    
    #============================================================================================
    def convert_unerry(self,path):
        timer = timerClass()
        timer.start()  
        print('Convert Unnery Format')
        
        self.export_item_list = list()
        df = pd.read_csv(path)
        self.rows = self.count_csv_rows(path)

        df.apply(self.parse_unerry,axis=1)
        self.export_item_list = list(self.data_dict.values())
        print('collect_time = '+str(timer.lap()))
           
        file_name = os.path.splitext(os.path.basename(path))[0]
        export_file_path = os.path.dirname(path)+'/'+file_name+'.json'
        
        if os.path.isfile(export_file_path):
            pass
        
        with open(export_file_path, 'w') as f:
            json.dump(self.export_item_list, f, indent=2)
        self.progress_callback(1)   
        print('progressTime= '+str(timer.stop()))
        
        return

#Convert Define in IniFile Items
    #============================================================================================
    def write2dict(self,id : str, date : datetime, lat,long,gender,age): 
        if not id in self.data_dict:#read Unlisted ID
            #Initailize MovinfFeature record
            new_dict = dict()
            d_list = list()
            new_dict[mf.KEY_PROPERTIES]   = {mf.KEY_NAME: id}
            new_dict[mf.KEY_TYPE]         =  mf.CONST_TYPE_MOVINGFEATURES
            new_dict[mf.KEY_TMP_GEOMETRY] = {mf.KEY_INTERPOLATE : mf.CONST_INTERPOLATE_LINEAR, 
                                                mf.KEY_TYPE        : mf.CONST_GEOMETRY_TYPE_POINT,
                                                mf.KEY_COORDINATES : list(),
                                                mf.KEY_DATETIMES   : d_list}
                
            new_dict[mf.KEY_TMP_PROPERTIES] = list()     
            self.data_dict[id] = new_dict       
                
        #Required Param
        if date != None:#read Date Param
            if lat!= None and long!=None:#read lat and long
                self.data_dict[id][mf.KEY_TMP_GEOMETRY][mf.KEY_COORDINATES].append([lat,long])   
                self.data_dict[id][mf.KEY_TMP_GEOMETRY][mf.KEY_DATETIMES].append(date.strftime('%Y-%m-%dT%H:%M:%SZ'))
            
        #Optional Param
        if gender != None:#read gender param
            if not "gender" in self.data_dict[id][mf.KEY_TMP_PROPERTIES]:
                self.data_dict[id][mf.KEY_TMP_PROPERTIES].append({mf.KEY_NAME : "gender", mf.KEY_VALUES : gender})#0
        if age != None:#read age Param
            if not "age" in self.data_dict[id][mf.KEY_TMP_PROPERTIES]:
                self.data_dict[id][mf.KEY_TMP_PROPERTIES].append({mf.KEY_NAME : "age",    mf.KEY_VALUES : age})#1
        return

#Convert CSV
    #============================================================================================
    def convert_template_csv(self,path):
        timer = timerClass()
        timer.start()   
        self.rows = self.count_csv_rows(path)        
        self.export_item_list = list()
        df = pd.read_csv(path)
        
        cfg = configparser.RawConfigParser()
        cfg.read(os.getcwd()+INI_FILE,'UTF-8')
        
        i = 0
        self.columnheaders = dict()
        date_formats_dict =dict()
        
        for section in dformat.template_essential_list_in_csv:
            for key,value in cfg.items(section):
                if key==PARAM_PATH:
                    self.columnheaders[section] =value
                if key==DATE_FORMAT:
                    date_formats_dict[section] =value
                
        for section in cfg.sections():
            if section in dformat.template_optionallist_in_csv:
                for key,value in cfg.items(section):
                    if key==PARAM_PATH:
                        self.columnheaders[section] =value
        
        self.header_identifer = self.columnheaders[dformat.template_parameter_list_in_csv[0]]
        
        self.datetime_format = date_formats_dict['year']
        self.datetime_format = self.datetime_format +'-'+ date_formats_dict['month']
        self.datetime_format = self.datetime_format +'-'+ date_formats_dict['day']
        self.datetime_format = self.datetime_format +'-'+ date_formats_dict['hour']
        self.datetime_format = self.datetime_format +'-'+ date_formats_dict['minute']
        
        if 'second' in  cfg.sections():
            self.datetime_format = self.datetime_format +'-'+ date_formats_dict['second']
            df.sort_values([self.header_identifer,
                        self.columnheaders[dformat.template_essential_list_in_csv[1]],
                        self.columnheaders[dformat.template_essential_list_in_csv[2]],
                        self.columnheaders[dformat.template_essential_list_in_csv[3]],
                        self.columnheaders[dformat.template_essential_list_in_csv[4]],
                        self.columnheaders[dformat.template_essential_list_in_csv[5]],
                        self.columnheaders[dformat.template_essential_list_in_csv[6]],
                        ],inplace = True)
        else:
            self.datetime_format = self.datetime_format + '-%S'
            df.sort_values([self.header_identifer,
                        self.columnheaders[dformat.template_essential_list_in_csv[1]],
                        self.columnheaders[dformat.template_essential_list_in_csv[2]],
                        self.columnheaders[dformat.template_essential_list_in_csv[3]],
                        self.columnheaders[dformat.template_essential_list_in_csv[4]],
                        self.columnheaders[dformat.template_essential_list_in_csv[5]],
                        ],inplace = True)
        
        
        df.apply(self.parse_template_csv,axis=1)
        
        self.export_item_list = list(self.data_dict.values())
        print('collect_time = '+str(timer.lap()))
        
        file_name = os.path.splitext(os.path.basename(path))[0]
        export_file_path = os.path.dirname(path)+'/'+file_name+'.json'
        if os.path.isfile(export_file_path):
            pass
        
        with open(export_file_path, 'w') as f:
            json.dump(self.export_item_list, f, indent=2)
        self.progress_callback(1)    
        print('progressTime= '+str(timer.stop()))
        return
    

#Convert XML    
    #============================================================================================
    def check_Xpath(self,xpath,target) ->Boolean:
        if (len(xpath)<=0) or (len(target)<=0):
            return False
        
        xtags = list(filter(None,re.split(r'[\\@]',xpath)))
        ttags = list(filter(None,re.split(r'[\\@]',target)))
        
        root = 0
        tip = 0
        if xpath[:1] == '\\\\':
            for i in range(len(ttags)):
                if xtags[0] == ttags[i]:
                    root = i
                elif i == len(ttags)-1:
                    return False    
                
        if '@' in xpath:
            tip = len(xtags)-1
        else:
            tip = len(xtags)-2
            
        for i in range(0,tip):
            if not (((root +i)<len(ttags)) and ((ttags[root +i] == xtags[i]) or (xtags[i] == '*'))):
                return False
            
        return True
    
    #============================================================================================
    def pase_xml(self, element : Element, path : str, id : str, date : datetime):
        if self.exitflag == True:
            return
        
        this_path = path+ "\\" + element.tag
        if '@' in self.param_path['id']:
            if self.param_identifer['id'] in element.attrib:
                if self.check_Xpath(self.param_path['id'], this_path):
                    id   = element.attrib.get(self.param_identifer['id'])
        else:                
            for child in element:
                if self.param_identifer['id'] == child.tag:
                    if self.check_Xpath(self.param_path['id'],this_path):
                        id   = child.text
                        break
        
        if '@' in self.param_path['date']:
            if self.param_identifer['date']  in element.attrib:
                if self.check_Xpath(self.param_path['date'],this_path):
                    date = element.attrib.get(self.param_identifer['date'])   
        else:
            for child in element:
                if child.tag == self.param_identifer['date']:
                    if self.check_Xpath(self.param_path['date'],this_path):
                        date = datetime.strptime(child.text, self.datetime_format)
                        break
                        
        lat = long = None
        if '@' in self.param_path['latitude']:
            if (self.param_identifer['latitude']  in element.attrib) and (self.param_identifer['longitude']  in element.attrib):
                if self.check_Xpath(self.param_path['latitude'], this_path):
                    lat  = element.attrib.get(self.param_identifer['latitude'] )
                    long = element.attrib.get(self.param_identifer['longitude'] )              
        else:
            for child in element:
                if child.tag == self.param_identifer['latitude']:
                    if self.check_Xpath(self.param_path['latitude'], this_path):
                        lat  = child.text
                elif child.tag == self.param_identifer['longitude']:
                    if self.check_Xpath(self.param_path['longitude'], this_path):
                        long = child.text

        gender = None
        if ('gender' in self.param_path):
            if '@' in self.param_path['gender']:
                if  self.check_Xpath(self.param_path['gender'], this_path):
                    gender = element.attrib.get(self.param_identifer['gender'])
            else:
                for child in element:
                    if child.tag == self.param_identifer['gender']:    
                        gender = child.text
            
        age = None
        if ('age' in self.param_path):
            if '@' in self.param_path['age']:
                if self.check_Xpath(self.param_path['age'], this_path):
                    age = element.attrib.get(age)
            else:
                for child in element:
                    if self.param_identifer['age'] == child.tag:
                        if self.check_Xpath(self.param_path['age'], this_path):
                            age = child.text
                    
        if id!=''  :#read ID
            self.write2dict(id,date,lat,long,gender,age)
            
        for child in element:
            self.pase_xml(child, this_path, id, date)   

    #============================================================================================
    def convert_template_xml(self,path):
        timer = timerClass()
        timer.start()   
        self.data_dict =dict()
        self.export_item_list = list()

        cfg = configparser.RawConfigParser()
        cfg.read(os.getcwd()+INI_FILE,'UTF-8')
        self.param_path  = {}        
        self.param_identifer = {}
        
        for section in cfg.sections():
             for key, value in cfg.items(section):
                if key==PARAM_PATH: 
                    self.param_path[section] = value
                    self.param_identifer[section] = list(filter(None,re.split(r'[\\@]',value)))[-1]   
                elif key==DATE_FORMAT:
                    self.datetime_format = value
                else:
                    pass
                    
        tree = ET.parse(path)    
        root = tree.getroot()       

        self.pase_xml(root, '', '', None)
        self.export_item_list = list(self.data_dict.values())
        print('collect_time = '+str(timer.lap()))

        file_name = os.path.splitext(os.path.basename(path))[0]
        export_file_path = os.path.dirname(path)+'/'+file_name+'.json'
        if os.path.isfile(export_file_path):
            pass

        with open(export_file_path, 'w') as f:
            json.dump(self.export_item_list, f, indent=2)           
        print('progressTime= '+str(timer.stop()))
        return
    
#Convert JSON
    #============================================================================================
    def check_Jsonpath(self,jPath,target : str) ->Boolean:
        def Compare_Segment(seg1 : str ,seg2 : str) -> Boolean:
            if '[' in seg1:
                if not '[' in seg2:
                    return False
                else:
                    l1 = list(filter(None,re.split(r'\[',seg1))) 
                    l2 = list(filter(None,re.split(r'\[',seg2)))
                    if len(l1)!=len(l2):                    
                        return False
                    if not(('[*]' in seg1) or (':' in l1[1])): 
                        if l1[1]!=l2[1]:
                            return False                           
                    if not '*' in l1[0]:
                        return (l1[0]==l2[0])
                    else:
                        return True
            else:
                if '*' == seg1:
                    return not('[' in seg2)         
                else:
                    return (seg1 == seg2)
                  
    #============================================================================================
        if (len(target)<=1):           
            return False
        
        if jPath==target:
            return True    
        
        tSegments = list(filter(None,re.split(r'[.]',target)))
        
        #Detached Segments        
        tip = 0
        if '..' in jPath:#Check Omission
            k=0
            sentences = list(filter(None,jPath.split('..')))  
            for i in range(len(sentences)):
                jSegments = list(filter(None,re.split(r'[.]',sentences[i])))
                for j in range(len(jSegments)):
                    if Compare_Segment(jSegments[j],tSegments[k]):
                        k +=1
                    else:
                        if j ==0:
                            k +=1
                            while k<len(tSegments):
                                if Compare_Segment(jSegments[j],tSegments[k]):  
                                    break
                                else:
                                    k +=1
                                    if k >=len(tSegments):
                                        return False
                        else:
                            return False
            return (k==len(tSegments)-1)
        else:
            jSegments = list(filter(None,re.split(r'[.]',jPath)))        
        
            if len(tSegments)!=len(jSegments):
                return False

            #Check Wildcard       
            for i in range(len(jSegments)):
                if not Compare_Segment(jSegments[i],tSegments[i]):
                    return False        
            return True
    
    #============================================================================================
    def pase_json(self,data,path : str, id : str, date : datetime):                
        if self.exitflag == True:
            return
        
        new_path : str
        lat = long = None
        gender = None
        age = None
        
        
        if self.param_type["id"] == 'key':
            if self.check_Jsonpath(self.param_path["id"],path):
                id = list(filter(None,re.split('.',path)))[-1]
        if self.param_type["date"] == 'key':
            print(path)
            if self.check_Jsonpath(self.param_path["date"],path):
                date = datetime.strptime(list(filter(None,re.split(r'[.]',path)))[-1], self.datetime_format)

        if isinstance(data, dict):
            for key,value in data.items():
                new_path = path+'.'+key
                if not (isinstance(value, list) or isinstance(value, dict)):
                    if key == self.param_identifer["id"]:
                        if self.check_Jsonpath(self.param_path["id"],new_path):
                            id = value
                    elif key == self.param_identifer["date"]:
                        if self.check_Jsonpath(self.param_path["date"],new_path):
                            date = datetime.strptime(value, self.datetime_format)
                    elif key ==  self.param_identifer["latitude"]:
                        if self.check_Jsonpath(self.param_path["latitude"],new_path):
                            lat = value
                    elif key == self.param_identifer["longitude"]:
                        if self.check_Jsonpath(self.param_path["longitude"],new_path):
                            long = value
                    elif ('age' in self.param_path) and (key == self.param_identifer["age"]):
                        if self.check_Jsonpath(self.param_path["age"],new_path):
                            age = value
                    elif ('gender' in self.param_path) and (key == self.param_identifer["gender"]):
                        if self.check_Jsonpath(self.param_path["gender"],new_path):
                            gender = value
                            
                if id!=''  :
                    self.write2dict(id,date,lat,long,gender,age)            

            for key,value in data.items():
                new_path = path+'.'+key
                self.pase_json(value,new_path,id ,date)
                
        elif isinstance(data, list):
            for i in range(len(data)-1):
                new_path = path + '['+str(i)+']'
                key= list(filter(None,re.split(r'[.]',path)))[-1]+'['+str(i)+']'
                if not (isinstance(data[i], list) or isinstance(data[i], dict)):              
                    if key == self.param_identifer["id"]:
                        if self.check_Jsonpath(self.param_path["id"],new_path):
                            id = data[i]
                    elif key == self.param_identifer["date"]:
                        if self.check_Jsonpath(self.param_path["date"],new_path):
                            date = datetime.strptime(data[i], self.datetime_format)
                    elif key ==  self.param_identifer["latitude"]:
                        if self.check_Jsonpath(self.param_path["latitude"],new_path):
                            lat = data[i]
                    elif key == self.param_identifer["longitude"]:
                        if self.check_Jsonpath(self.param_path["longitude"],new_path):
                            long = data[i]
                    elif ('age' in self.param_path) and (key == self.param_identifer["age"]):
                        if self.check_Jsonpath(self.param_path["age"],new_path):
                            age = data[i]
                    elif ('gender' in self.param_path) and  (key == self.param_identifer["gender"]):
                        if self.check_Jsonpath(self.param_path["gender"],new_path):
                            gender = data[i]
                            
                    if id!=''  :#read ID
                        self.write2dict(id,date,lat,long,gender,age)
            
            for i in range(len(data)):
                new_path = path + '['+str(i)+']'
                self.pase_json(data[i],new_path,id ,date)                   
        return
    
    #============================================================================================
    def convert_template_json(self,path):
        #Measure Converting Time
        timer = timerClass()
        timer.start()                
        print('collect_time = '+str(timer.lap()))
        self.data_dict =dict()
        self.export_item_list = list()

        self.param_path = {}
        self.param_path_segments = {}
        self.param_identifer = {}
        self.param_type = {}
        
        #Read IniFile
        cfg = configparser.RawConfigParser()
        cfg.read(os.getcwd()+INI_FILE,'utf-8')
        for section in cfg.sections():
            for key, value in cfg.items(section):
                if key==PARAM_PATH:
                    if (len(value)<=1) or (value[0:2] != '$.'):
                        print(section + ' Json path is not configured correctly')
                        return
                    self.param_path[section] = value
                    self.param_identifer[section] = list(filter(None,re.split(r'[\\@.]',value)))[-1]
                elif key==PARAM_TYPE: 
                    self.param_type[section] = value    
                elif key==DATE_FORMAT:
                    self.datetime_format = value
       
        #Convert
        with open(path,encoding="utf-8") as f:
            obj = json.load(f)
            self.pase_json(obj, '$', '', None)                
        
        #Export Conveted File
        self.export_item_list = list(self.data_dict.values())    
        file_name = os.path.splitext(os.path.basename(path))[0]
        export_file_path = os.path.dirname(path)+'/'+file_name+'_convertedmf.json'
       
        if os.path.isfile(export_file_path):
            pass
        
        with open(export_file_path, 'w') as f:
            json.dump(self.export_item_list, f, indent=2)
        
        #Close Progress Window
        self.progress_callback(1)    
        
        #Displaying Elapsed Time
        print('progressTime= '+str(timer.stop()))
        return
        

        
        
