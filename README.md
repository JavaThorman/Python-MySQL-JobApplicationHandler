# Job Application Tracker

A Python application to track and manage job applications. The program allows you to add, update, delete, and view job applications, along with storing responses and notes. 

### User Interface
The application also features a user interface to make interactions easier. Stay tuned for upcoming UI features and updates.

## Features

- Add new job applications
- View all job applications
- Update job application details
- Add application responses and notes
- Delete job applications
- Interactive user interface (UI)

## Requirements

- Python 3.x
- MySQL Database
- `mysql-connector-python` package (used for database interactions)
- `customtkinter` package (used for the graphical user interface)

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/job-application-tracker.git
cd job-application-tracker
```
2. Install required Python packages
Create a virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install mysql-connector-python customtkinter
```
Alternatively, you can install the dependencies directly:
```
pip install mysql-connector-python customtkinter
```
3. Configure Database Connection
Update config.py with your MySQL server credentials:
```
DB_HOST = "localhost"  # or your MySQL host
DB_USER = "root"  # your MySQL username
DB_PASSWORD = "root"  # your MySQL password
```
Note: The program will automatically create the job_tracker_db database if it doesn't exist, so you no longer need to manually create the database.

4. Run the Program
Once everything is set up, run the program:
```
python main.py
```
##### - The program will launch the UI and prompt you to choose actions such as adding job applications, viewing them, updating, or deleting.

UI Controls:
- Add Job Application: Adds a new job application to the database.
-  View Job Applications: Displays all job applications stored in the database.
- Update Job Application: Allows you to update details of an existing job application.
- Delete Job Application: Removes a job application from the database.
Application Response and Notes: You can also update the application response and add additional notes for each job application.
```bash
job-application-tracker/
├── Database/
│   ├── config.py             # Database configuration
│   └── database.py           # Database connection and queries
├── Program/
│   ├── models.py             # Job application model
│   └── program.py            # Program entry point
├── UI/
│   ├── ui.py                 # User interface using customtkinter
├── main.py                   # Entry point for running the program
└── README.md                 # Project documentation
```

License
This project is licensed under the MIT License - see the LICENSE file for details.






