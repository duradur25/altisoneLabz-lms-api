from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.auth_router import router as auth_router
from routers.mentor_router import router as mentor_router
from routers.admin_router import router as admin_router

app = FastAPI(title="AltisOneLabz LMS API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(mentor_router)
app.include_router(admin_router)