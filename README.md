## Game Munchers

### Summary
A database based application focused on the video game industry. Application is functionally similar to Steam. This application can be run in the form of a web application or a command line interface.

## Project Status
The command line interface is fully functional. The web application is currently in development.

## Project Screen Shot(s)

[ coming soon ]

## Installation and Setup Instructions

Clone this repository. You will need `node` and `npm` installed globally on your machine.  

#### Installation:
---

`pip install -r requirements.txt`

`cd frontend`

`npm install`  

#### Setup:
---

 Setup the `.env` files in `/cli` and `/backend`. 

The `.env` files should be in the following format

For `/cli/.env`:
```bash
SSH_USERNAME=your_username
PASSWORD=your_password
DB_NAME=p320_12
```

For `/backend/.env`:
```bash
SSH_USERNAME=your_username
PASSWORD=your_password
DB_NAME=p320_12
SECRET_KEY=your_secret_key
```

#### Run:
---

##### For the Command Line Interface:
Execute `python application.py` while in the `/cli` directory

##### For the Web Application:

Execute `flask run` while in the `/backend` directory

Execute `npm start` or `npm test` while in the `/frontend` directory

Go to `localhost:3000` in your browser to view the web application