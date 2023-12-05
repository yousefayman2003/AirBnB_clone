<h1 align="center"> Welcome to the AirBnB clone project! </h1>
<img src="https://techstory.in/wp-content/uploads/2021/05/1_puERGSOrHj7Fuw6I8dJC7g.png"/>

# AirBnb Clone
The goal of the project is to deploy on a server a simple copy of the [AirBnB website](https://www.airbnb.com/). We didn't implement all the features, 
only some of them to cover all fundamental concepts of the higher level programming track ([Holberton SE Internship](https://www.holbertonschool.com/)).

### The web application composed by:
- A command interpreter to manipulate data without a visual interface, like in a Shell (perfect for development and debugging)
- A website (the front-end) that shows the final product to everybody: static and dynamic
- A database or files that store data (data = objects)
- An API that provides a communication interface between the front-end and the database (retrieve, create, delete, update them)

# Table of Contents
- [Development Approach](#development-approach)
- [Features](#features)
- [Dependencies](#dependencies)
- [Getting Started](#getting-started)

<a id="development-approach"></a>
## Development Approach
We didn't build this application all at once. We divided it into six stages and used agile methodology to develop it, so we analyzed, designed, and implemented each stage.
#### Stages:
1. The console:
    - Create a data model
    - Manage (create, update, destroy, etc) objects via a console / command interpreter
    - Store and persist objects to a file (JSON file)
3. Web static:
    - Create the HTML of the application
    - Create template of each object
5. MySQL storage:
    - Replace the file storage by a Database storage
    - Map the models to a table in database by using an O.R.M.
7. Web framework - templating:
    - Create a web server in Python
    - Make a static HTML file dynamic by using objects stored in a file or database
9. RESTful API:
    - Expose all objects stored via a JSON web interface
    - Manipulate objects via a RESTful API
11. Web dynamic:
    - Load objects from the client side by using our RESTful API

<a id="features"></a>
## Features

<a id="dependencies"></a>
## Dependencies
The Airbnb Clone relies on the following technologies and dependencies:

### Backend:
- Python
- Flask
- MySql

### Frontend:
- HTML
- CSS
- JavaScript

Additional libraries and tools:
- Redux (for state management)
- Flask (for API requests)
- Babel (for transpiling)
- Webpack (for bundling)
- Unittest (for testing)

<a id="getting-started"></a>
## Getting Started
To get started with the Airbnb Clone, follow these steps:<br>
**1. Clone the repository:** Begin by cloning this repository to your local machine.

    $ git clone https://github.com/mohammed112025/airbnb-clone.git

**2. Set up the environment:** Install the necessary dependencies and configure the environment variables.

**3. Database setup:** Set up the database and run the necessary migrations.

**4. Start the server:** Launch the server application.

**5. Access the website:** Open your browser and navigate to http://localhost:3000 to access the Airbnb Clone website.
