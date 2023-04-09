## Python flask app

- *app/* - contains flask .py, html, css, js files. Front-end and api endpoints are set here.
- *src/dbmanager/* - submodule that contains *BibleDB* class that provides methods to access the Data Base. 
- *src/file_handling/* - submodule for handling local json files mostly

    Bible translations are present in .txt files aligned by ids with specific format. 
    
    This module parses all the files in the given directory and yields it. 

    It is being used in *populate_db.py* script. Data provided by parses in then buing inserted into the data base.