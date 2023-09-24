## Python flask 

- [views.py](./views.py) endpoints for website pages. 
    - Does not interact with the DB
    - Interface language is managed here and everything that doesnt require data from the DB.
- [api.py](./api.py) endpoints for api. 
    - These interact with the DB.
    - Front JS uses these.
- [app.py](./app.py) defining flask app class object
- [translations.py](./translations.py) translation data
- [src/](./src/) local modules.
    - "dbmanager" that implements DB interaction.
    - "file_handling" that implements interaction with files.
- [static/](./static/) static files: css, js, fonts
- [templates/](./templates/) html Jinja templates for Flask