# -*- coding: utf-8 -*-
"""
This is a PYTHON3 script file.
"""
import os
import requests
import urllib
import re
from bs4 import BeautifulSoup as bs
from datetime import datetime
import time
import numpy as np
from PIL import Image  
import pandas as pd              

def get_id_from_page(page='1'): 
    url = 'https://spectralworkbench.org/spectra/search/?page='+page
    req = requests.get(url)
    html_text = bs(req.text, 'lxml') #'html.parser'
    id_list = [item.attrs["href"][-6:] for item in html_text.find_all("a",{"class":"image hidden-phone"})]
    return int(id_list[0])


def download_img(imgUrl,download_path):   
    urllib.request.urlretrieve(imgUrl,download_path)
    return


class key_word():
      general = ['cfl','ccfl','fluorescent','fluorescence',
                'incandescent','halogen','quartz','discharge',
                'led','sun','sky','solar','gas','light','star','stellar',
                'lamp','tube','bulb','laser','hid','bunsen',
                'nano','calibrate','calibrated','calibration','blank','reference','flat',
                'absorption','absorbed','abs.','reflection','reflected','standard','filter']                
      brands = ['osram','philips','panasonic','ikea']
      molecules = ['alcohol','methanol','glucose','acetone','hcl,''etoh','ethanol',
                   'cuso4','cucl2','kcl','nacl','tio2','salt','h2o','water','urea']
      compounds = ['oil','wood','glass','diamond','pearl','candle','wine','solution','tea','coffee'] 
      elements = ['h','hydrogen','he','helium','ne','neon','xe','xenon','ar','argon','na','sodium',
                  'hg','mercury','al','aluminium','ti','titanium','cu','copper','pb','lead','zn','zinc',
                  'fe','iron','au','gold','ag','silver','cadmium','tungsten','iodine','nitrogen',
                  'oxygen','oxide','chloride']
      all_words = general+brands+molecules+compounds+elements


def title_filter(title,log_file):
    the_words = set(title.lower().replace(' ','_').split("_"))  
    if 'test' in the_words:
       match = []   
    else:        
       match = list(the_words & words_filter)   
    print ('  Match  : %d'%len(match), match, file=log_file)   
    return match
    

def get_data(id_range, log_file): #input is numpy int array
    id_list = np.asarray(id_range,dtype=str)
    total_size = id_list.size
    imgfolder_path = os.path.join(os.getcwd(),'Save','Image',id_list[0]+'-'+id_list[-1])              
    if not os.path.exists(imgfolder_path): os.makedirs(imgfolder_path)   
    class ImgUrlError(Exception): pass
   
    dataID_list = []
    title_list = []
    author_list = []
    u_date_list = []
    descri_list = []
    img_name_list = []
    img_xsize_list = []
    img_ysize_list = []
    keyword_list = []
    
    i = 0
    for the_id in id_list:
        start_time = time.time()
        i += 1
        print("Progress : %d / %d ......"%(i, total_size), file=log_file)
        print("  ID     : %s"%(the_id), file=log_file)

        url = 'https://spectralworkbench.org/spectrums/'+the_id
        req = requests.get(url)
        req_scode = req.status_code
        if req_scode != 200:
           print("  Status : Page Not exist! Code : %d \n"%(req_scode), file=log_file)
        else:        
           html_text = bs(req.text, 'lxml')
           title = html_text.find("a",href=re.compile(the_id)).text
           title = title.replace("\n","").rstrip().lstrip()
           match_words = title_filter(title,log_file)          
           if len(match_words) > 0:              
              try:
                 #---------------------#
                 author = html_text.find("a",href=re.compile("profile")).text
                 #---------------------#
                 u_date = html_text.find("i",text=re.compile("UTC")).text[12:-4]
                 u_date = datetime.strptime(u_date, '%B %d, %Y %H:%M').strftime("%Y-%m-%d %H:%M:%S")
                 #---------------------#
                 descri_p = html_text.find_all("p")
                 if len(descri_p[4].text) == 0:
                    descri = descri_p[5].text   
                 else:
                    descri = 'None' 
                 #---------------------#            
                 imgUrl = html_text.find("div","swb-spectrum-img-container").findChildren()[0].attrs
                 if 'src' in imgUrl :                    
                    imgUrl = "https://spectralworkbench.org" + imgUrl['src']
                    img_fmt = '.'+imgUrl.split('.')[-1]                                      
                    download_path = os.path.join(imgfolder_path,the_id+img_fmt) 
                    download_img(imgUrl,download_path)                                   
                 else:
                    raise ImgUrlError("No image for this spectrum")
                 #---------------------# 
                 xsize, ysize = Image.open(download_path).size 
                 #---------------------# 
                 is_ok = True
              except Exception as e:  
                 is_ok = False
                 print("  Status : ",type(e).__name__,"-",e,"\n", file=log_file)                 
                 
              if is_ok :    
                 dataID_list.append(the_id)
                 title_list.append(title)
                 author_list.append(author)
                 u_date_list.append(u_date)
                 descri_list.append(descri)
                 img_name_list.append(download_path.replace('\\', '/').split('/')[-1])
                 img_xsize_list.append(xsize)
                 img_ysize_list.append(ysize)              
                 keyword_list.append(match_words)
                 print("  Status : Done!!! \n", file=log_file)                                         
           else:
              print("  Status : No match keyword! \n", file=log_file)   
              
        time.sleep(1)
        dt = time.time()-start_time
        print("\r"+"Progress    : %d / %d in %.5f sec."%(i, total_size, dt), end="\r")

    print("----ALL Finished----", file=log_file)
    print("Recorded : %d data"%(len(dataID_list)), file=log_file)   
    return (dataID_list, title_list, author_list, 
            u_date_list, descri_list, img_name_list,
            img_xsize_list, img_ysize_list, keyword_list)    


#########################################################################
if __name__ == '__main__':
   def select_the_function():
       mode_i = input('\nSelect the function [1=Fuction1 / 2=Fuction2] : ')
       while mode_i != '1' and mode_i != '2':        
             mode_i = input('Select the function [1=Fuction1 / 2=Fuction2] : ') 
       return mode_i

   def input_the_id():
       id_input = input('\nInput the starting ID [use "," to separate if input multiple IDs]:\n')
       chk = [i.isdigit() for i in id_input.split(',')]
       while all(chk) != True:
             id_input = input('Input the starting ID [use "," to separate if input multiple IDs]:\n')
             chk = [i.isdigit() for i in id_input.split(',')]
       return id_input 

   def input_the_range(id_input):
       range_input = input('\nInput the counting backwards number [1 - 5000]:\n')
       while range_input.isdigit() != True:             
             range_input = input('Input the counting backwards number [1 - 5000]:\n')
       while int(range_input) > 5000 or int(range_input) == 0 :             
             range_input = input('Input the counting backwards number [1 - 5000]:\n')                     
       chk = min([int(i) for i in id_input.split(',')])
       while chk-int(range_input) < 0 :             
             range_input = input('Input the counting backwards number [1 - 5000]:\n')                     
       return range_input  

   def input_fun1_chk():
       chk = input('\nPress s to start, r to re-enter, q to exit [s/r/q]?')   
       while chk != 's' and chk != 'r' and chk != 'q':        
             chk = input('Press s to start, r to re-enter, q to exit [s/r/q]?')               
       return chk 
   
   def input_fun2_chk():
       chk = input('\nPress r to re-enter, q to exit [r/q]?')   
       while chk != 'r' and chk != 'q':        
             chk = input('Press r to re-enter, q to exit [r/q]?')               
       return chk 

   def get_input():
       mode_i = select_the_function()
       if mode_i == '1': 
          id_input = input_the_id()
          range_input = input_the_range(id_input)                    
          final_chk = input_fun1_chk()
          if final_chk == 's':
             return [id_input, range_input]
          elif final_chk == 'r':
             return get_input()
          else:
             return ['','']         
       if mode_i == '2':
          print('wait...') 
          first_id = get_id_from_page('1')
          print('The newest ID : %d'%first_id)
          final_chk = input_fun2_chk()
          if final_chk == 'r':
             return get_input()
          else:
             return ['',''] 
       
   print ('------------------------------------------------------------------------')     
   print ('------------ Welcome to use SpectralWorkbench WebCrawler v1 ------------')
   print ('------------------------------------------------------------------------\n') 
   print ("Simple Description : \n")
   print (" The target URL is <https://spectralworkbench.org/spectra/TargetID> and ")
   print (" the TargetID is a number represents the order of whole uploads, the  ")
   print (" larger number means the newer uploaded spectrum image.\n")
   print (" This program will crawl(scan) the webpage based on TargetID you inputed,")   
   print (" and check the title of the spectrum using keyword filter to confirm its ")  
   print (" valuable or not. Saving the spectrum image and information if valuable.\n") 
   print ('------------------------------------------------------------------------\n')
   print ("User Guide : \n")     
   print (" Fuction1- Set the starting ID and the number of counting backwards.")
   print ("           Ex: ID is 9000 and counting backwards number is 1000, the ")
   print ("               program will crawl the webpage from ID 9000 to 8001.\n")    
   print (" Fuction2- Get the latest ID of the uploads.\n") 
   print (" The image, data table, log file will be stored under Save directory.\n")
   print ('-----------------------------------------------------------------------\n') 
   chk = input('Do you want to continue [y/n]?') 
   while chk != 'y' and chk != 'n':        
         chk = input('Do you want to continue [y/n]?') 
         
   if chk == 'y':
      the_input = get_input() #list have 2 item
      if the_input[0] != '':        
         first_id_list = [int(i) for i in the_input[0].split(',')]
         id_counts = int(the_input[1])
         words_filter = set(key_word.all_words) 
         #chk directory 
         if not os.path.exists(os.path.join(os.getcwd(),'Save')): 
            os.makedirs(os.path.join(os.getcwd(),'Save')) 
         if not os.path.exists(os.path.join(os.getcwd(),'Save','Image')): 
            os.makedirs(os.path.join(os.getcwd(),'Save','Image')) 
         if not os.path.exists(os.path.join(os.getcwd(),'Save','DataTable')): 
            os.makedirs(os.path.join(os.getcwd(),'Save','DataTable')) 
         if not os.path.exists(os.path.join(os.getcwd(),'Save','Log')): 
            os.makedirs(os.path.join(os.getcwd(),'Save','Log'))               
         print ('-----------------------------------------------------------------------')
         for first_id in first_id_list:
            id_range = np.arange(first_id,first_id-id_counts,-1)
            #id_range = [141726,141148,128211]
            StartTime = datetime.now().strftime("%Y%m%d%H%M")
            log_file_path = os.path.join(os.getcwd(),'Save','Log',str(id_range[0])+'-'+str(id_range[-1])+'-'+StartTime+'.log') 
            log_file = open(log_file_path, 'w+')
            print ('ID          : %d - %d'%(first_id,id_range[-1]))
            print ('StartTime   : %s'%(StartTime))
            #########################################################################
            orignal_data = get_data(id_range,log_file)    
            #########################################################################            
            data = pd.DataFrame({
                    "ID": orignal_data[0],  
                    "Title": orignal_data[1],
                    "Author": orignal_data[2],
                    "UploadDate": orignal_data[3],
                    "Description": orignal_data[4],
                    "ImageName": orignal_data[5],
                    "ImageXsize": orignal_data[6],
                    "ImageYsize": orignal_data[7],
                    "keyword": orignal_data[8],        
                   })    
            filename = str(id_range[0])+'-'+str(id_range[-1])+'-'+StartTime+'.csv'
            data_path = os.path.join(os.getcwd(),'Save','DataTable',filename) 
            data.to_csv(data_path,sep=',')    
            print("DataTable saved : %s"%(filename), file=log_file)   
            #########################################################################
            EndTime = datetime.now().strftime("%Y%m%d%H%M")
            log_file.write('Start Time : %s \n'%StartTime) 
            log_file.write('  End Time : %s \n'%EndTime)
            log_file.write('Delta Time : %s \n'%str(datetime.strptime(EndTime,'%Y%m%d%H%M')-
                                                    datetime.strptime(StartTime,'%Y%m%d%H%M')))
            log_file.close()
            #########################################################################
            print ("") 
            print ('EndTime     : %s'%(EndTime))
            print ('ElapsedTime : %s'%str(datetime.strptime(EndTime,'%Y%m%d%H%M')-
                                       datetime.strptime(StartTime,'%Y%m%d%H%M')))
            print ('DataCounts  : %d'%(data["ID"].size))
            print ('-----------------------------------------------------------------------')         
      else: 
         print ("ByeBye")     
   else: 
      print ("ByeBye")      
     
      