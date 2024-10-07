
<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a name="readme-top"></a>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->

<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">


<h3 align="center">Hack Hero</h3>

  <p align="center">
    A full-stack app to gamify your programming learning experience!
</div>



<!-- TABLE OF CONTENTS -->
<details>
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
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



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

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/othneildrew
[flask-shield]: https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=Flask&logoColor=white
[flask-url]: https://flask.palletsprojects.com/en/3.0.x/#
[postgres-shield]: https://img.shields.io/badge/postgresql-4169e1?style=for-the-badge&logo=postgresql&logoColor=white
[postgres-url]: https://www.postgresql.org/
