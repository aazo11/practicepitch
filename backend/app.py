from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, HttpUrl
from typing import Optional
import requests
from bs4 import BeautifulSoup
import json
from sqlmodel import Field, Session, SQLModel, create_engine

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Application(BaseModel):
    company_name: str
    website: HttpUrl
    linkedin: HttpUrl
    pitch_deck: HttpUrl
    github: Optional[HttpUrl] = None
    email: EmailStr
    meeting_time: str

class ApplicationEntry(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    company_name: str
    website: str
    linkedin: str
    pitch_deck: str
    github: Optional[str] = None
    email: str
    meeting_time: str

engine = create_engine("sqlite:///applications.db")
SQLModel.metadata.create_all(engine)

@app.post("/api/apply")
async def apply(application: Application, background_tasks: BackgroundTasks):
    with Session(engine) as session:
        entry = ApplicationEntry(**application.model_dump())
        session.add(entry)
        session.commit()
    background_tasks.add_task(crawl_company, application)
    zoom_link = create_zoom_meeting(application)
    send_invite_email(application.email, zoom_link, application.meeting_time)
    return {"zoom": zoom_link}

def crawl_company(app_data: Application):
    info = {}
    try:
        resp = requests.get(app_data.website)
        soup = BeautifulSoup(resp.text, "html.parser")
        info["title"] = soup.title.string if soup.title else ""
    except Exception as e:
        info["error"] = str(e)
    with open(f"crawl_{app_data.company_name}.json", "w") as f:
        json.dump(info, f)

def create_zoom_meeting(app_data: Application) -> str:
    """Placeholder Zoom meeting creation"""
    # TODO: Integrate with Zoom's API
    return "https://example.com/zoom-meeting"

def send_invite_email(to_email: str, zoom_link: str, meeting_time: str) -> None:
    """Placeholder email sender"""
    # TODO: use smtplib or an email service
    print(f"Send invite to {to_email} for {meeting_time} -> {zoom_link}")
