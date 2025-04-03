# Smart-scheduler

![Screenshot from 2023-11-20 20-55-54](https://github.com/morikeli/smart-scheduler/assets/78599959/bc57ceb5-b2e8-41ae-b5bb-867273329033)


### Overview
This web application is designed to support our local educational institution by serving both students and administrators. It allows lecturers to schedule lectures, while students receive updates and notifications about these schedules. To minimize time loss and disruptions when searching for suitable venues, the app automatically assigns available venues to lectures scheduled for the current day.

### Technologies used
  - HTML
  - CSS
  - JS
  - jQuery (Calendar integration)
  - Django (backend)

### User instructions
  Click this [link](https://smart-schedule.onrender.com/auth/login) to use and view the website. To use the website you must create an account either as a student, Head of Department (HOD) or a lecturer.

#### Responsibility of a student
  - register units they will be studying in the current semester
  - update their students info, e.g. year of study, semester
  - confirm they will be attending a scheduled lecture
  - provide feedback about the venue of the latest lecture

#### Responsibility of a lecturer
  - schedule lectures they will be teaching on a given date and time

#### Responsibility of the Head of department (HOD)
  - appoints/assigns units a lecturer will be teaching in the current semester
  - schedules a lecture he/she will be teaching in the current semester

### Developer instructions
##### To run the project offline;
  - clone the repo to your desired location, e.g. Desktop, Downloads or Documents
  - Install Python interpreter on your local machine if you don't have one. In this project, Python v3.11.4 was used.
  - Open the project folder using your IDE of choice
  - Create a virtual environment using the command `python -m venv .venv` or `python3 -m venv .venv`. You use this command in your IDE's terminal or your terminal/Command prompt. Make sure you have opened the project folder in your terminal.
  - On your terminal/cmd, type:
    -  `source .venv/bin/activate` (Linux)
    -  `.venv\Scripts\activate`  (Windows)
  - To install modules and libraries used in developing the project, type `pip install -r requirements.txt` or `pip3 install -r requirements.txt`
  - Once all the packages have been installed, type `python manage.py runserver` or `python3 manage.py runserver`. You can view the website on your browser using the link `http://127.0.0.1:8000`.

### Issues
 Feel free to report any issues encountered (create an issue using the `Issues` tab or provide your feedback through the `Discussions` tab. Your feedback is highly appreciated.
