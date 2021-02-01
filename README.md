# Coffee Shop Full Stack

This project is designed to be able to register new users, authenticate and authorize them using Auth0 as 3rd party authentication service.
The project enables you to do the following:
  1. Sign up for a certain user using Auth0 authentication service
  2. Option to Sign up using Google mail
  3. Ability to login through the site and have access to it after you are authenticated
  4. The project has 2 roles:
      4.1. Manager, who can display all drinks, add drink, update drink and delete any drink
      4.2. Barista, who can only display drinks but without the ability to do any further action
  5. Drinks are added and displayed by their titles and recipes, each recipe shall have a list of components from which it is composed
  6. Drinks are displayed in colors corresponding to their recipes
  7. Users have the ability to Logout and Login and each time they are authenticated


## Pre-requisites to run the project

1. Python 3.7 should be installed at the machine
  Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. Clone the project's repo

3. Setup Virtual Enviornment
  It is recommended to be working within a virtual environment whenever using Python for projects. This keeps the dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

4. Navigate to `'/backend'` and install all project's dependencies by running this command at your CMD:
```bash
  pip install -r requirements.txt
```
##### Key Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database used in that project.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

5. Check `'/backend'` READMe to know how to setup and run the backend environment

6. Check `'/frontend'` READMe to know how to setup and run the frontend environment


## Tests

Under `'/backend'` there exist postman_collection.json file which include test cases for testing the backend endpoints and also included the latest test_run resulsts


## API Reference

Please check the 'README' file included in `'/backend'` folder for reference


## Authors

Software Engineer: Yousif Elhady


## Acknowledgements

Thanks to all my mentors at Udacity Web development nano-degree program
