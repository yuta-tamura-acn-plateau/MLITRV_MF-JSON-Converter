agoop_header_list = ["dailyid",              #0
                        "year",                 #1
                        "month",                #2 
                        "day",                  #3
                        "dayofweek",            #4
                        "hour",                 #5
                        "minute",               #6
                        "latitude",             #7
                        "longitude",            #8
                        "os",                   #9
                        "home_countryname",     #10
                        "plmn",                 #11
                        "plmn_countryname",     #12 
                        "setting_currency",     #13
                        "setting_language",     #14
                        "setting_country",      #15
                        "logtype_category",     #16
                        "logtype_subcategory",  #17
                        "accuracy",             #18
                        "speed",                #19 
                        "estimated_speed_flag", #20
                        "course",               #21
                        "estimated_course_flag",#22
                        "prefcode",             #23
                        "citycode",             #24
                        "mesh100mid",           #25
                        "home_prefcode",        #26
                        "home_citycode",        #27
                        "workplace_prefcode",   #28
                        "workplace_citycode",   #29
                        "gender"]               #30

agoop_identifier_list = list([agoop_header_list[0],])

agoop_essential_list = list([agoop_header_list[0],
                                agoop_header_list[1],
                                agoop_header_list[2],
                                agoop_header_list[3],
                                agoop_header_list[4],
                                agoop_header_list[5],
                                agoop_header_list[6],
                                agoop_header_list[7],
                                agoop_header_list[8],
                                agoop_header_list[9],
                                agoop_header_list[10],
                                agoop_header_list[11],
                                agoop_header_list[12],
                                agoop_header_list[13],
                                agoop_header_list[14],
                                agoop_header_list[15],
                                agoop_header_list[16],
                                agoop_header_list[17],                                
                                agoop_header_list[18],
                                agoop_header_list[19],
                                agoop_header_list[20],
                                agoop_header_list[21],
                                agoop_header_list[22],
                                agoop_header_list[23],
                                agoop_header_list[24],
                                agoop_header_list[25],])

agoop_reserved_items =list([agoop_header_list[0],
                                agoop_header_list[1],
                                agoop_header_list[2],
                                agoop_header_list[3],
                                agoop_header_list[4],
                                agoop_header_list[5],
                                agoop_header_list[6],
                                agoop_header_list[7],
                                agoop_header_list[8],])

agoop_fixed_items =list([       agoop_header_list[9],
                                agoop_header_list[10],
                                agoop_header_list[11],
                                agoop_header_list[12],
                                agoop_header_list[13],
                                agoop_header_list[14],
                                agoop_header_list[15],
                                agoop_header_list[16],
                                agoop_header_list[17],                                                                                                
                                agoop_header_list[26],
                                agoop_header_list[27],
                                agoop_header_list[28],
                                agoop_header_list[29],
                                agoop_header_list[30]])
 
agoop_timeline_items = list([agoop_header_list[18],
                                agoop_header_list[19],
                                agoop_header_list[20],
                                agoop_header_list[21],
                                agoop_header_list[22],
                                agoop_header_list[23],
                                agoop_header_list[24],
                                agoop_header_list[25]]
                                )


#=============================================================================================
blogwatcer_header_list =["uuid",                #0
                         "adid",                #1
                         "hashed_adid",         #2
                         "datetime",            #3  ex 2022-12-01 10:05:30 ex2024/7/1  0:00:00
                         "timestamp",           #4  ex 2022-12-01 01:05:30 UTC
                         "unixtime",            #5  ex 1669856730
                         "date",                #6  ex 2022-12-01
                         "time",                #7  ex 10:05:30
                         "latitude_anonymous",  #8  ex 35.6809591
                         "longitude_anonymous", #9  ex 139.7673068
                         "accuracy",            #10 ex 13.922
                         "mesh",                #11 ex 53394611324
                         "os",                  #12 ex
                         "geo_name",            #13
                         "poi_home",            #14 ex 53394612144
                         "poi_work",            #15 ex 53394600243
                         "speed",               #16 ex 1.7380251
                         "course",              #17 ex 291.0964
                         "height",              #18
                         "ssid",                #19
                         "bssid",               #20 08:00:23:fd:02:11
                         "level"]               #21 

blogwatcer_identifier_list = list([blogwatcer_header_list[0],
                                   blogwatcer_header_list[1],
                                   blogwatcer_header_list[2],])

blogwatcer_essential_items = list([blogwatcer_header_list[8],
                                   blogwatcer_header_list[9],])

blogwatcer_reserved_items = list([blogwatcer_header_list[3],
                                  blogwatcer_header_list[4],
                                  blogwatcer_header_list[5],
                                  blogwatcer_header_list[6],
                                  blogwatcer_header_list[7],
                                  blogwatcer_header_list[8],
                                  blogwatcer_header_list[9],],)

blogwatcher_fixed_items =list([blogwatcer_header_list[0],
                               blogwatcer_header_list[1],
                               blogwatcer_header_list[2],
                               blogwatcer_header_list[12],
                               blogwatcer_header_list[13],
                               blogwatcer_header_list[14],
                               blogwatcer_header_list[15],
                               blogwatcer_header_list[19],
                               blogwatcer_header_list[20],
                               blogwatcer_header_list[21],])

blogwatcher_timleine_items =list([blogwatcer_header_list[10],
                                  blogwatcer_header_list[11],
                                  blogwatcer_header_list[16],
                                  blogwatcer_header_list[17],
                                  blogwatcer_header_list[18],])    

#=============================================================================================
unerry_header_list =["adid",#0
                     "app_user_id",#1
                     "extra_id_1",#2
                     "extra_id_2",#3
                     "detected_on_jst",#4
                     "latitude",#5
                     "longitude",#6       
                     "category_id",#7
                     "category_name",#8
                     "brand_id",#9
                     "brand_name",#10
                     "poi_id",#11
                     "poi_name",#12
                     "prefecture_code",#13
                     "prefecture_name",#14
                     "city_code",#15
                     "city_name"]#16

unerry_identifier_list = [unerry_header_list[1],                          
                          unerry_header_list[2],
                          unerry_header_list[3],
                          unerry_header_list[0],]

unerry_essential_list = [unerry_header_list[4],
                         unerry_header_list[5],
                         unerry_header_list[6],
                         unerry_header_list[7],
                         unerry_header_list[8],
                         unerry_header_list[9],
                         unerry_header_list[10],
                         unerry_header_list[11],
                         unerry_header_list[12],]

unerry_reserved_items = [ unerry_header_list[1],
                          unerry_header_list[4],
                          unerry_header_list[5],
                          unerry_header_list[6],]

unerry_fixed_items =  [  unerry_header_list[0],                     
                         unerry_header_list[2],
                         unerry_header_list[3],                                                  
                         unerry_header_list[7],
                         unerry_header_list[8],
                         unerry_header_list[9],
                         unerry_header_list[10],
                         unerry_header_list[11],
                         unerry_header_list[12],]

unerry_timleine_items = [unerry_header_list[13],
                         unerry_header_list[14],
                         unerry_header_list[15],
                         unerry_header_list[16],]


#=============================================================================================
template_parameter_list_in_csv =['id',       #0
                                 'year',     #1
                                 'month',    #2
                                 'day',      #3
                                 'hour',     #4
                                 'minute',   #5
                                 'second',   #6
                                 'latitude', #7
                                 'longitude',#8 
                                 'gender',   #9
                                 'age']      #10

template_essential_list_in_csv =[template_parameter_list_in_csv[0],
                                 template_parameter_list_in_csv[1],
                                 template_parameter_list_in_csv[2],
                                 template_parameter_list_in_csv[3],
                                 template_parameter_list_in_csv[4],
                                 template_parameter_list_in_csv[5],
                                 template_parameter_list_in_csv[6],
                                 template_parameter_list_in_csv[7],
                                 template_parameter_list_in_csv[8],]

template_optionallist_in_csv =[template_parameter_list_in_csv[9],
                               template_parameter_list_in_csv[10],]

