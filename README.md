# SpectralWorkbenchCrawler
Crawl SpectralWorkbench website  to get the spectrum image and its information by ID number. 

Version 1.0.0


Simple Description :

   The target URL is https://spectralworkbench.org/spectra/TargetID and the TargetID is a
   number represents the order of whole uploaded spectrum image, the larger number means
   the newer uploaded spectrum. 
   
   This program will crawl(scan) the webpage based on TargetID you inputed, and check 
   the title of the spectrum using custom keyword filter to confirm its valuable or not. 
   There are about 100 words in the filter currently, you can modify it by yourself. Finally,
   saving the spectrum image and information if valuable.

   
User Guide :

   Step 1 - Check requirements.txt file to confirm all required packages have been installed.
   Step 2 - Just run swc_main.py file by python3 
            Ex. $ python3 swc_main.py
   Step 3 - Following the instructions enter the parameters. 
   
   Note:
   The program has two functions: 
   Fuction1 - Set one or more starting-IDs and the number of counting backwards.
              Ex: Set IDs = 90000,5000 and counting backwards number = 1000, the 
                  program will crawl the webpage from ID 90000 to 89001 and 5000 to 4001.    
   Fuction2 - Get the latest ID of the uploaded spectrum.   
   The downloaded image, data table, log file will be stored under Save directory.
   
   
   
   
   
 