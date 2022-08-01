# SCore
Compound database and analysis 
# SCore_datahandler
#### Description:

This project is a back-end for a database system, with some function for supporting a assay production and data handling. 
As the project is for internal use only, with a minimum amount of users, I have not taken extra step to ensure the safety of the data. 
A lot of the system is depending on I/O files as the system needs to send files out that can be imported to different equipment, and import files from different equipment. 
If this was meant to go out to a larger amount of people, there would need to be written extra code, to ensure the all data is the correct data in the right format. 
For now the system assume that the data it gets, its in the right format, with all needed information. 

I have chosen to split the project up into multiple modules, that each handle different part of the system. to make it easier to work with. 
I have tried to prepare the set-up for a later integration with a GUI. so a lot of the information is default values, that will either be pulled from list/dropdown menus or written in text boxes.
So for now, the system is depended on the user, to change the code, and hard-code in different settings. 

###Abbreviation:
MP = MotherPlates (Main plates that can produce multiple other plates)
DP = DaugtherPlates (Plates that comes from MP’s and are used for assays
PB = PlateButler (A robotic arm connected to different equipment, that can do liquids transferees, incubations, analyzing data and so on.


##Folders and files
There is a lot of extra files and folders in the sytem. this is both test files, and finish production files from the system. 


##Using the system
There are 6 main functions that the system can do.
Most of the data is typed in as default. This can be changed in the code. 
All of the functions are access with "python project.py function"
Where "function" is the name of one the following:

####start_up_database:
To setup the database, write "python project.py start_up_database"
This will setup the database SCore.db with the tables listed in layout.py. 
It is important that layout.py have no additional code, as "eval" is used, to execute the code in layout.py. 
adds compounds from vendor_compounds.txt to the database. (8483 compounds added)

####mp_production:
Generatores a list of 7680 (20 plates) of compounds
Produces a csv file for getting compounds from a comPOUND freezer
Produces CSV files for PB

####mp_production_tube_to_pb:
Concert comPOUND freezer files to PB files 
test files are created by "mp_production"

####dp_production:
Produces dp files for the PB system
test files are created by "mp_production"

####purity_handler:
Gets purity data from LC/MS/MS raw data
test files are found in: "LC_MS_DATA/P1"


####update_database
Update the database with data. Both for adding data to the different tables, but updating tables with new values
needs the data file, the table where the data is going and evt file_type. If this is not important type "none"



#Modul information

##main database functions:

###chem_operators.py
This module handles different chemical operations that can be calculated using rdkit. 
It is used to get structures out from a mol code and convert it into a png-string, to be able to draw the structures in the database.
(The base is implemented and tested in small scale, but with no front end for this system, the functions are not used)
There are three different functions to calculate how similar to different compounds are to each other, this is used to do a similarity search, to make sure that the compounds picked from the database, have specific structure. 


###database_handler.py
This module, is the main way that the system is using sqlite3. As sqlite3 uses mostly text-based entries to add, find and delete data. 
This handler is written to make it possible to avoided writing out the different lines of code, to get what is needed, but transform it into easy to use functions. 

###database_controller.py 
This module is the main access point to the database. I choose to split the database handling up into two different files. one to handle the sqlite3 code and one to handle the data that needed to interact with the database. 

###database_startup.py
This is the initail start up of the database, setting all the table importat from layout.py, and setting everything up. 


###plate_formatting.py
This format plates correctly based on data from other modules, to get it in a standard format, that  then can be used by different modules. 


##I/O handling

###csv_handler.py
This module handles all csv related operations. Writing and reading of data.

####Writer:
comPOUND is a storage system that needs CSV files to pick-up specific compounds, based on a 2D barcode
MP productions set-up to pb. as pb needs a specific CSV layout to operate. 
DP productions set-up for pb. as pb needs a specific CSV layout to operate.  DP's are not a complete copy of an MP. but can have a different layout, amount of samples and from different plates

####Reader:
Gets different data in to the system. There is a controller as the main access point to the csv-reader that sends the files to the right functions to handle the data.
Gets data from 2D scanner, that can scan plates, and re-format the data. 

####Converter
Handles conversion of one csv-setup to another incase something goes wrong. This is a back-up system that should not be needed. 

###excel_handler.py
This module is written to deal with setting up a specific layout for DP's. As each experiment demands different amount of samples, blanks, references and how they are placed.
This make it possible to take a specific excel-sheet "Destination.xlsx" and plan the experiment this way, fill in samples, blanks and references if needed. then import the sheet to the functions that handles DP production. 
This module is a temporary solution. In the long term, there needs to be a front-end setup where you can draw this, to avoid having to import sheet to the system.

###sdf_handler.py
A lot of companies that sells compounds in bulk are sending their data in sdf-format. 
This module takes compound data from vendors, pull out the data that is needed. 
There is a vendor.sdf file that can be used to test this module. 

###xml_handler.py
We have a liquid handler that produces xml.data that tells what well have been transferred to what well, from what plate to what plate and how much. And if there are any transferees that are not complete. 
This module takes that data, and writes in a format that can be used by other modules to update the database, and give a dictionary of missing transferees. 


##LC modules
These modules are handling different part of the LC/MS/MS data process.

###data_miner.py
This module takes raw data from an LC/MS/MS and writes in into tensors, for UV and MS. The UV-tensor issued to calculating area of peaks, combined with the information from the MS data, the system can calculate purity of a compound, and check the status. 
This is needed to make sure that the compounds  that are being used are clean and not degraded. 

###lc_data_handler.py
the main access point to all the LC/MS/MS data handling. Importing data, and making sure that the data is formatted correctly.

###lcms_ms_search.py
This module searches for the right mass based on data for each compound. and includes the use of the config.txt where all ions are listed, for both negative and positive MS signals. 

###lcms_uv_integration.py
This module takes a UV-tensor and calculate the how many peaks a samples have, the area for each peak and puts it in a dict. 


##support moduls
###info.py
This module contains information of how a plate is layout for 96 and 384 well plates. and is needed for different set-ups to get the right data written to files and the database. 

###layouts.py
This is all the tables for the database, their layout, headlines, what type they are using and key-values. 
This module is import during the start-up of the database. 



##test_project.py
This module test 3 function in the main function to see if they work as intended. 



TODO
There is missing a front end for the system. 
There is missing the data analyst for bio-logical data. 

