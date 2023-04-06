## Python flask app

- *app/* - contains flask .py, html, css, js files. Front-end and api endpoints are set here.
- *dbmanager/* - contains *BibleDB* class that provides methods to access the Data Base. 

    It is being imported by flask and *populate_db.py* script in the project root.
- *dbmanager/parser/* - contains parser code. 

    Bible translations are present in .txt files aligned by ids with specific format. 
    
    This module parses all the files in the given directory and yields it. 

    It is being used in *populate_db.py* script. Data provided by parses in then buing inserted into the data base.