# Chore application name here

<a name="readme-top"></a>

<br />

  <h3 align="center">SDEV265 Group 3 Project</h3>

  <p align="center">
    A household chore application.
    <br />
    <a href="#about-the-project"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://youtube.com/">View Demo</a>
    ·
    <a href="https://github.com/Mitchell7685/SDEV-265-Group-3/issues">Report Bug</a>
    ·
    <a href="https://github.com/Mitchell7685/SDEV-265-Group-3/issues">Request Feature</a>
  </p>
</div>

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
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

## About The Project

The goal of this project is to gamify household management by transforming common tasks into engaging RPG-style quests. Users will receive experience points for every task that they complete and will be ranked among others in this system.


<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With

These are the frameworks, libraries, and software used in this Project.

* [![Python][Python.com]][Python-url]
* [![Django][Django.com]][Django-url]
* [![SQLite][SQLite.com]][SQLite-url]
* [![HTML][HTML.com]][HTML-url]
* [![CSS][CSS.com]][CSS-url]
* [![Bootstrap][Bootstrap.com]][Bootstrap-url]
* [![Javascript][Javascript.com]][Javascript-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Getting Started

To get the project up and running follow these steps.

* Start by cloning the repository
    ```sh
    git clone https://github.com/Mitchell7685/SDEV-265-Group-3.git
    ```
* Navigate into the project directory
    ```sh
    cd SDEV-265-Group-3/
    ```
* Set up python virtual environment
    ```sh
    # Windows
    python -m venv venv
    # macOS/Linux
    python3 -m venv venv
    ```
* Activate python virtual environment
    ```sh
    # On Linux/macOS use:
    source venv/bin/activate
    # On Windows use: 
    venv\Scripts\activate
    ```
* Install dependencies
    ```sh
    pip install -r requirements.txt
    ```
* Apply Database Migrations
    ```sh
    python manage.py migrate
    ```
* Run the Application
    ```sh
    python manage.py runserver
    ```
* Open your browser and enter this local address
    ```sh
    http://127.0.0.1:8000/
    ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Prerequisites

System Requirements?

## Usage

Once the server is running, you can access the default homepage. 

1.  **Admin Panel:** Navigate to `http://127.0.0.1:8000/admin/` to access the Django administration interface.
2.  **Create Superuser:** To log in to the admin, run:
    ```sh
    python manage.py createsuperuser
    ```
3.  **App Views:** The main application logic is located in the `main/` directory.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Roadmap
- [x] Project Planning
- [ ] Initial Project Setup
- [ ] Virtual Environment Configuration
- [ ] Base App Creation (`main`)
- [ ] Create Database Models


<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Contact

Team
- Collin Congleton - [Collin's LinkedIn](https://www.linkedin.com/in/) - [Collin's GitHub](https://github.com/Satori15)
- Jacob Lee - [Jacob's LinkedIn](https://www.linkedin.com/in/) - [Jacob's GitHub](https://github.com/)
- Mitchell Kehler - [Mitchell's LinkedIn](https://www.linkedin.com/in/) - [Mitchell's GitHub](https://github.com/Mitchell7685)
- Stephen Littman - [Stephen's LinkedIn](https://www.linkedin.com/in/stephen-littman/) - [Stephen's GitHub](https://github.com/anarchking)
- Yverson Louis - [Yverson's LinkedIn](https://www.linkedin.com/in/) - [Yverson's GitHub](https://github.com/)


Project Link - [Repo Link](https://github.com/Mitchell7685/SDEV-265-Group-3/)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Acknowledgments

This is a list of some useful tools and resources used in the setup of this project.

* [Django Documentation](https://docs.djangoproject.com/)
* [Bootstrap 5](https://getbootstrap.com/)
* [Django Snippets](https://djangosnippets.org/)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

[Python.com]: https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54
[Python-url]: https://www.python.org/

[Django.com]: https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white
[Django-url]: https://www.djangoproject.com/

[SQLite.com]: https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white
[SQLite-url]: https://sqlite.org/

[HTML.com]: https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white
[HTML-url]: https://www.w3.org/html/

[CSS.com]: https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white
[CSS-url]: https://www.w3.org/Style/CSS/Overview.en.html

[Javascript.com]: https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E
[Javascript-url]: https://www.javascript.com/

[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.compile
