# SpectralWorkbenchCrawler
Crawl SpectralWorkbench website  to get the spectrum image and its information by ID number. 

Version 1.0.0

<br>

### Simple Description :

* The target URL is https://spectralworkbench.org/spectra/TargetID and the TargetID is a
  number represents the order of whole uploaded spectrum image, the larger number means
  the newer uploaded spectrum.

* This program will crawl(scan) the webpage based on TargetID you inputed, and check 
  the title of the spectrum using custom keyword filter to confirm its valuable or not. 
  There are about 100 words in the filter currently, you can modify it by yourself. Finally,
  saving the spectrum image and information if valuable.

* #### The two functions of the program :

  - Fuction1 - Set one or more TargetIDs and the number of counting backwards.<br>
   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Ex: Set ID = 90000,5000 and counting backwards number = 1000, the program will crawl the webpage<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;from ID 90000 to 89001 and 5000 to 4001. 
  - Fuction2 - Get the latest ID of the uploaded spectrum.<br>

<br>

### User Guide :

* Step 1 - Check requirements.txt file to confirm all required packages have been installed.

* Step 2 - Just run swc_main.py file by python3 
    ```bash
    $ python3 swc_main.py
    ```
* Step 3 - Following the instructions enter the parameters.
* Note : The downloaded image, data table, log file will be stored under Save directory.<br>

<br>

### Snapshots:

- The snapshot of program running<br>

  ![](https://lcycblog.files.wordpress.com/2018/09/swc_cmd.png "Program snapshot")

<br>

- The snapshot of created  DataTable<br>

  ![](https://lcycblog.files.wordpress.com/2018/09/swc_datatable.png "DataTable snapshot")



   
