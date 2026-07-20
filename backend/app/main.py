from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import jobs
from .routers import resume
from .routers import auth
from .routers import career_assistant
from .routers import chat
from .database import Base, engine
from . import models
from .routers import interview
from .routers import analytics
from .routers import resume_ai
from .routers import interview

Base.metadata.create_all(bind=engine)


app = FastAPI()

app.include_router(auth.router)
app.include_router(career_assistant.router)
app.include_router(chat.router)
app.include_router(interview.router)
app.include_router(analytics.router)
app.include_router(resume_ai.router)
from .routers import dashboard

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(jobs.router)
app.include_router(resume.router)
app.include_router(dashboard.router)

@app.get("/")
def home():
    return {"message": "HireSense AI"}


print("\n========== ALL ROUTES ==========")
for route in app.router.routes:
    if hasattr(route, "path"):
        print(route.path)
print("================================")