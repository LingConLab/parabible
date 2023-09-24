## Python flask app

- [app/](./app/) - contains flask .py, html, css, js files. Front-end and api endpoints are set here. Database interaction is also here.
- [conf.env](./conf.env) - env file. Here is used to set debug and prodoction variables. 
**!IMPORTANT!** Don't forget to set `DEBUG` variable to 'False' before commiting any changes to main branch.
- [Dockerfile](./Dockerfile) - Dockerfile for python backend app. In container the app is deployed with uwsgi.

