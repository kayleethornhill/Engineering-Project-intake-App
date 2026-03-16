import sqlite3
import csv
import io
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

DB_NAME = "projects.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_name TEXT NOT NULL,
            work_order_number TEXT NOT NULL,
            project_engineer TEXT NOT NULL,
            project_status TEXT NOT NULL,       
            external_contractor_assigned TEXT NOT NULL,
            contractor_name TEXT,
            estimated_construction_start TEXT NOT NULL,
            project_description TEXT
        )
    """)

    conn.commit()
    conn.close()


init_db()


@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI"}


@app.get("/form")
def show_form(request: Request):
    return templates.TemplateResponse(
        "form.html",
        {"request": request}
    )


@app.post("/submit")
def submit_form(
    request: Request,
    project_name: str = Form(...),
    work_order_number: str = Form(...),
    project_engineer: str = Form(...),
    project_status: str = Form(...),
    external_contractor_assigned: str = Form(...),
    contractor_name: str = Form(""),
    estimated_construction_start: str = Form(...),
    project_description: str = Form("")
):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO projects (
            project_name,
            work_order_number,
            project_engineer,
            project_status,
            external_contractor_assigned,
            contractor_name,
            estimated_construction_start,
            project_description
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        project_name,
        work_order_number,
        project_engineer,
        project_status,
        external_contractor_assigned,
        contractor_name,
        estimated_construction_start,
        project_description
    ))

    conn.commit()
    conn.close()

    return templates.TemplateResponse(
        "success.html",
        {
            "request": request,
            "project_name": project_name,
            "work_order_number": work_order_number,
            "project_engineer": project_engineer,
            "project_status": project_status,
            "external_contractor_assigned": external_contractor_assigned,
            "contractor_name": contractor_name,
            "estimated_construction_start": estimated_construction_start,
            "project_description": project_description
        }
    )

@app.get("/export/csv")
def export_csv():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, project_name, work_order_number, project_engineer,
               project_status, external_contractor_assigned, contractor_name,
               estimated_construction_start, project_description
        FROM projects
        ORDER BY id DESC
    """)

    projects = cursor.fetchall()
    conn.close()

    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow([
        "ID",
        "Project Name",
        "Work Order Number",
        "Project Engineer",
        "Project Status",
        "External Contractor Assigned",
        "Contractor Name",
        "Estimated Construction Start",
        "Project Description"
    ])

    writer.writerows(projects)

    output.seek(0)

    return StreamingResponse(
        output,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=projects_export.csv"}
    )

@app.get("/projects")
def view_projects(request: Request):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, project_name, work_order_number, project_engineer,
               project_status, external_contractor_assigned, contractor_name,
               estimated_construction_start, project_description
        FROM projects
        ORDER BY id DESC
    """)

    projects = cursor.fetchall()
    conn.close()

    return templates.TemplateResponse(
        "projects.html",
        {
            "request": request,
            "projects": projects
        }
    )

