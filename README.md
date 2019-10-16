# Currency Converter

Application to convert the currency based on exchangeratesAPI
https://exchangeratesapi.io/
Heroku https://curr-conv.herokuapp.com/

## Code style

- This project is written in python 3.
- Flask framework.
- Bootstrap in front-end

## Project Files

- app.py: application file

- wtform_fields: Contain wtforms class for the form and validator

- Dockerfile: contains all the commands a user could call on the command line to assemble an docker image

- convert_test.py: contain tests

- requirements.txt: Contain a list of items to be installed, use the command to install all of items `pip install -r requirements.txt`

## Run

### Dockerize the App

- To build the image from Dockerfile run on project directory run `$ docker build -t currency-convert:latest . `

- To Run the container run `$ docker run -d -p 3000:3000 currency-convert`

- run `python app.py`

- go to localhost:3000

### Run the tests

- run `python convert_test.py`
