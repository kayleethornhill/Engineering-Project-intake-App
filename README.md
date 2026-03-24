# Engineering Project Intake App

A FastAPI web application for submitting, storing, viewing, and exporting engineering project intake records.

Problem: 
Engineering teams lacked a standardized way to submit new projects to Document Control and keep record of the submission.

Solution:
I designed and built a system that: 
- captures project submissions through a structured form
- automates data entry into a centralized system
- Enables visibility into project staus and workload

## Application Screenshots

 ### Project Intake Form
![Project Intake Form](screenshots/form-page.png)

### Submission Success Page
![Submission Success Page](screenshots/success-page.png)

### Saved Projects Page
![Saved Projects Page](screenshots/saved-projects-page.png)

## Features

- Submit new engineering projects through a web form
- Store project records in a SQLite database
- View all saved projects in a table
- Track project status
- Export project data to CSV for reporting and Power BI

## Tech Stack

- Python
- FastAPI
- SQLite
- HTML
- CSS

## Project Structure

```text
engineering-project-intake-app/
│
├── main.py
├── requirements.txt
├── .gitignore
├── static/
│   └── style.css
└── templates/
    ├── form.html
    ├── success.html
    └── projects.html


## How to Run

Clone the repository.

Create a virtual environment.

Activate the virtual environment.

Install dependencies:

pip install -r requirements.txt

Run the app:

uvicorn main:app --reload

Open in browser:

http://127.0.0.1:8000/form

http://127.0.0.1:8000/projects

