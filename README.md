
<p align="center">
  <h3 align="center">Chat boot</h3>
 </h4>
</p>


<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
  </ol>
</details>


<!-- ABOUT THE PROJECT -->
## About The Project
Application made for the chatBot challenge. It consists of a REST API made with fastAPI and tortoise as ORM.


### Built With

*	Python 3
*	FastAPI
*	Tortoise
*	Unit test(with pytest)
*	Docker and docker-compose
*	Coverage
*   NGNIX

<!-- GETTING STARTED -->
## Getting Started

This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.

### Prerequisites for Local Development
* Python Programming Language
* Postgres version 12


### Installation 

1. Clone the repo
   ```sh
   git clone https://github.com/murtagh95/chat_bot
   ```
2. Change directory to chat_bot
   ```sh
   cd chat_bot
   ```
3. Copy the .env.example file to the root of the project and name it .env.
   ```sh
   cp .env.example .env
   ```
   - Modify the variables as you consider necessary.


### Run Locally

1. Install poetry which is used to handle dependencies https://python-poetry.org/
   ```sh
   pip install poetry
   ```
2. Install python module dependencies
   ```sh
   poetry install
   ```
3. Activate virual env
   ```sh
   poetry shell
   ```
4. Run migrations and api server
   ```sh
    uvicorn app.main:app --host 0.0.0.0 --reload
   ```

### Using Docker Compose

1. Build containers with docker-compose
   ```sh
   docker-compose build
   ```
2. Start containers
   ```sh
   docker-compose up -d
   ```

<!-- USAGE EXAMPLES -->
## Usage
Go to the browser and type the following url:

### With Docker
[http://localhost:8080/docs](http://localhost:8080/docs)

### In local
[http://localhost:8000/docs](http://localhost:8000/docs)


In the fastAPI interface you will be able to test the different EndPoints

<!-- CONTACT -->
## Contact

Nicolas Catalano - nec.catalano@gmail.com