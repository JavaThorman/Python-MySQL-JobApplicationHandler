# Job Application Tracker

A Python application to track and manage job applications. The program allows you to add, update, delete, and view job applications, along with storing responses and notes.
#### Interface coming soon
## Features

- Add new job applications
- View all job applications
- Update job application details
- Add application response and notes
- Delete job applications

## Requirements

- Python 3.x
- MySQL Database
- `mysql-connector-python` package (used for database interactions)

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/job-application-tracker.git
cd job-application-tracker
```
### 2. Install required Python packages
Create a virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt
```
#### Alternatively, you can install the dependencies directly:
```bash
pip install mysql-connector-python
```

#### 3. Setup Database
Ensure that you have a MySQL server running, and create the database specified in config.py (job_tracker_db). You can do this via MySQL command line or MySQL Workbench:
```sql
CREATE DATABASE job_tracker_db;
```

#### 4. Configure Database Connection
Update config.py with your MySQL server credentials:
```python
DB_HOST = "localhost"  # or your MySQL host
DB_USER = "root"  # your MySQL username
DB_PASSWORD = "root"  # your MySQL password
DB_NAME = "job_tracker_db"  # the database name
```

#### 5. Run the Program
Once everything is set up, run the program:
```bash
python main.py
```
#### The program will prompt you to choose actions such as adding job applications, viewing them, updating, or deleting.
#
### File Structure
```bash
job-application-tracker/
├── config.py             # Database configuration
├── database.py           # Database connection and queries
├── main.py               # Entry point for running the program
├── models.py             # Job application model
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation
```

# License
This project is licensed under the MIT License - see the LICENSE file for details.
