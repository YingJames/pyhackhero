﻿
<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a name="readme-top"></a>

[![LinkedIn][linkedin-shield]][linkedin-url]

<!-- PROJECT LOGO -->
<br />
<div align="center">


<h3 align="center">Hack Hero</h3>

  <p align="center">
    A full-stack app to gamify your programming learning experience!
</div>

<!-- ABOUT THE PROJECT -->
## About The Project

HackHero is a web application, which combines Leetcode problems with a "gamefied" To-do list by structuring
"Quests" as a collection of "levels." HackHero includes an HTML front-end using Python Flask, as well as a
PostgreSQL database for the back-end.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

[![Flask][flask-shield]][flask-url]
[![PostgreSQL][postgres-shield]][postgres-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started on Linux

To get a local copy up and running follow these simple steps.

1. Make sure you have postgres installed
```bash
sudo apt install postgresql
```

2. You only need to run this once to get postgresql running in the background
``` bash
sudo service postgresql start
```

3. Run postgresql and create the database
```bash
psql
CREATE DATABASE hackhero;
\c hackhero
```

4. Make sure the database is connected and run the sql schema file
```bash
\c hackhero
\i path/to/hhh.sql
```

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/YingJames/pyhackhero.git
    ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- Features EXAMPLES -->
## Features

User Subclasses:
* Players: Regular users who solve coding challenges and progress through quests.
* Admins: Users that have access to the Admin Dashboard page to create quests, problems, and topics.

Coding Challenges:
* Problems: A variety of coding challenges using LeetCode problems, with different difficulty levels.
* Topics: Problems are categorized into various programming topics or concepts.

Gamification Elements:
* Quests: Sequences of coding challenges grouped together, created by admins.
* Levels: Individual challenges within quests, linked to specific problems and topics.
* Progress Tracking: Players can track completed levels and quests

  
![image](https://github.com/user-attachments/assets/fc5790a4-c5fa-4213-8c80-65ca52824513)

![image](https://github.com/user-attachments/assets/13bdd8b5-8251-48a4-83a0-d652e6d0fa89)

![image](https://github.com/user-attachments/assets/231bf5f9-af2d-4189-b848-a71d415f49d8)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/james-yab
[flask-shield]: https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=Flask&logoColor=white
[flask-url]: https://flask.palletsprojects.com/en/3.0.x/#
[postgres-shield]: https://img.shields.io/badge/postgresql-4169e1?style=for-the-badge&logo=postgresql&logoColor=white
[postgres-url]: https://www.postgresql.org/
