import os
import json
import requests
from dotenv import load_dotenv

# Load environment variables first
load_dotenv(".env.local" if os.getenv("ENVIRONMENT", "local") == "local" else ".env.production")

from fastapi import FastAPI, BackgroundTasks, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, HttpUrl
from sqlalchemy.orm import Session
from typing import Optional
from bs4 import BeautifulSoup
from .database import get_db, create_tables, Application as DBApplication
from .config import settings

app = FastAPI()

# Create database tables on startup
create_tables()

# CORS configuration - more specific for production
if settings.is_production:
    allowed_origins = [f"https://{host}" for host in settings.allowed_hosts if host != "*"]
else:
    allowed_origins = ["http://localhost:5173", "http://localhost:5174", "http://127.0.0.1:5173", "http://127.0.0.1:5174"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins if settings.is_production else ["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

class ApplicationRequest(BaseModel):
    company_name: str
    website: HttpUrl
    linkedin: HttpUrl
    pitch_deck: HttpUrl
    github: Optional[HttpUrl] = None
    email: EmailStr
    meeting_time: str

class ApplicationResponse(BaseModel):
    id: int
    company_name: str
    website: str
    linkedin: str
    pitch_deck: str
    github: Optional[str] = None
    email: str
    meeting_time: str
    zoom_link: Optional[str] = None
    status: str
    created_at: str

@app.get("/")
async def root():
    return {"message": "Practice Pitch API", "environment": settings.environment}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "environment": settings.environment}

@app.post("/api/apply")
async def apply(
    application: ApplicationRequest, 
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    try:
        # Create Zoom meeting first
        zoom_link = create_zoom_meeting(application)
        
        # Save to database
        db_application = DBApplication(
            company_name=application.company_name,
            website=str(application.website),
            linkedin=str(application.linkedin),
            pitch_deck=str(application.pitch_deck),
            github=str(application.github) if application.github else None,
            email=application.email,
            meeting_time=application.meeting_time,
            zoom_link=zoom_link,
            status="scheduled"
        )
        
        db.add(db_application)
        db.commit()
        db.refresh(db_application)
        
        # Background tasks
        background_tasks.add_task(crawl_company, application, db_application.id)
        background_tasks.add_task(send_invite_email, application.email, zoom_link, application.meeting_time)
        
        return {"zoom": zoom_link, "application_id": db_application.id}
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error processing application: {str(e)}")

@app.get("/api/applications")
async def get_applications(db: Session = Depends(get_db)):
    """Get all applications (for admin use)"""
    applications = db.query(DBApplication).all()
    return [ApplicationResponse(
        id=app.id,
        company_name=app.company_name,
        website=app.website,
        linkedin=app.linkedin,
        pitch_deck=app.pitch_deck,
        github=app.github,
        email=app.email,
        meeting_time=app.meeting_time,
        zoom_link=app.zoom_link,
        status=app.status,
        created_at=app.created_at.isoformat()
    ) for app in applications]

@app.get("/api/applications/{application_id}")
async def get_application(application_id: int, db: Session = Depends(get_db)):
    """Get specific application"""
    application = db.query(DBApplication).filter(DBApplication.id == application_id).first()
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    
    return ApplicationResponse(
        id=application.id,
        company_name=application.company_name,
        website=application.website,
        linkedin=application.linkedin,
        pitch_deck=application.pitch_deck,
        github=application.github,
        email=application.email,
        meeting_time=application.meeting_time,
        zoom_link=application.zoom_link,
        status=application.status,
        created_at=application.created_at.isoformat()
    )

def crawl_company(app_data: ApplicationRequest, application_id: int):
    """Background task to crawl company information"""
    info = {}
    try:
        resp = requests.get(str(app_data.website), timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        
        info["title"] = soup.title.string.strip() if soup.title else ""
        info["description"] = ""
        
        # Try to get meta description
        meta_desc = soup.find("meta", attrs={"name": "description"})
        if meta_desc:
            info["description"] = meta_desc.get("content", "")
        
        # Get some basic info
        info["url"] = str(app_data.website)
        info["company"] = app_data.company_name
        
    except Exception as e:
        info["error"] = str(e)
        print(f"Error crawling {app_data.website}: {str(e)}")
    
    # Save crawl data to database
    try:
        from database import SessionLocal
        db = SessionLocal()
        application = db.query(DBApplication).filter(DBApplication.id == application_id).first()
        if application:
            application.crawl_data = json.dumps(info)
            db.commit()
        db.close()
    except Exception as e:
        print(f"Error saving crawl data: {str(e)}")

def create_zoom_meeting(app_data: ApplicationRequest) -> str:
    """Create Zoom meeting - placeholder implementation"""
    # TODO: Integrate with Zoom's API using settings.zoom_api_key
    # For now, return a placeholder
    company_safe = app_data.company_name.replace(" ", "-").lower()
    meeting_id = f"practice-pitch-{company_safe}"
    return f"https://zoom.us/j/{meeting_id}"

def send_invite_email(to_email: str, zoom_link: str, meeting_time: str) -> None:
    """Send invite email - improved implementation"""
    if settings.email_backend == "console":
        print(f"""
=== EMAIL INVITE ===
To: {to_email}
Subject: Your Practice Pitch Session is Scheduled!

Hi there!

Your practice pitch session has been scheduled for {meeting_time}.

Join here: {zoom_link}

Best of luck with your pitch!

The Practice Pitch Team
===================
        """)
    else:
        # TODO: Implement actual email sending with SMTP
        # Use settings.smtp_host, settings.smtp_user, etc.
        print(f"Would send email to {to_email} via SMTP")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=settings.debug)
