# Entry point for the FastAPI application.
# Registers routers and configures middleware.

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import CORS_ORIGINS
from app.routes.explain_routes import router as explain_router
from app.routes.file_routes import router as file_router
from app.routes.history_routes import router as history_router
from app.routes.report_routes import router as report_router
from app.routes.summary_routes import router as summary_router
from app.routes.upload_routes import router as upload_router
from app.routes.similarity_routes import router as similarity_router

app = FastAPI(
    title="Code Plagiarism Detector",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload_router, prefix="/api")
app.include_router(similarity_router, prefix="/api")
app.include_router(file_router, prefix="/api")
app.include_router(report_router, prefix="/api")
app.include_router(explain_router, prefix="/api")
app.include_router(summary_router, prefix="/api")
app.include_router(history_router, prefix="/api")


@app.get("/")
def health_check():
    return {"status": "ok"}
