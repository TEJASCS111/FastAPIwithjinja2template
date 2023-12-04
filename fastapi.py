# Importing all the necessary modules
from fastapi import FastAPI, Request, File, UploadFile
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import pandas as pd
import sqlite3

# Create the FastAPI app
app = FastAPI()

# Create the Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Create the SQLite database and the Users table
conn = sqlite3.connect("users.db")
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS Users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)")
conn.commit()

# Define the root endpoint with Jinja template
@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    # Render the index.html template
    return templates.TemplateResponse("index.html", {"request": request})

# Define the upload endpoint to handle the csv file
@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    # Read the csv file into a pandas dataframe
    df = pd.read_csv(file.file)

    # Get the column names of the dataframe
    columns = list(df.columns)

    # Render the upload.html template with the column names
    return templates.TemplateResponse("upload.html", {"request": request, "columns": columns})

# Define the submit endpoint to save the data into the database
@app.post("/submit")
async def submit(name: str, age: str):
    # Convert the name and age parameters into integers
    name = int(name)
    age = int(age)

    # Read the csv file into a pandas dataframe
    df = pd.read_csv(file.file)

    # Select the name and age columns from the dataframe
    df = df.iloc[:, [name, age]]

    # Rename the columns to name and age
    df.columns = ["name", "age"]

    # Insert the dataframe into the Users table
    df.to_sql("Users", conn, if_exists="append", index=False)

    # Render the submit.html template with a success message
    return templates.TemplateResponse("submit.html", {"request": request, "message": "Data saved successfully!"})