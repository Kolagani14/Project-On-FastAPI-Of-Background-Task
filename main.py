from fastapi import FastAPI,Request,UploadFile,File,BackgroundTasks
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os,shutil,time

app=FastAPI()
templates=Jinja2Templates(directory="templates")
upload_dir="upload_files"
os.makedirs(upload_dir,exist_ok=True)

@app.post("/upload-blocking/",response_class=HTMLResponse)
def upload_blocking(request:Request,file:UploadFile=File(...)):
    file_path=os.path.join(upload_dir,file.filename)
    with open(file_path,"wb") as buffer:
        shutil.copyfileobj(file.file,buffer)
        time.sleep(5)
    return templates.TemplateResponse("upload_blocking.html",{"request":request,"status":"Blocking uploaded successfully"})

def upload_background_file(file:UploadFile):
    try:
        file_path=os.path.join(upload_dir,file.filename)
        with open(file_path,"wb") as buffer:
            shutil.copyfileobj(file.file,buffer)
            time.sleep(5)
            print("File Uploaded Successfully")
    except Exception as e:
        print(f"Error:{e}")

@app.post("/upload-nonblocking/",response_class=HTMLResponse)
def upload_nonblocking(request:Request,background_task:BackgroundTasks,file:UploadFile=File(...)):
    background_task.add_task(upload_background_file,file)
    return templates.TemplateResponse("upload_background1.html",{"request":request,"status":"uploaded successfully in background"})



@app.get("/",response_class=HTMLResponse)
async def blocking(request:Request):
    return templates.TemplateResponse("upload_blocking.html",{"request":request})
@app.get("/background",response_class=HTMLResponse)
async def background_form(request:Request):
    return templates.TemplateResponse("upload_background1.html",{"request":request})
