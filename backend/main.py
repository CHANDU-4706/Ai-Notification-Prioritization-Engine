from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import api
from app.database.db_init import init_db

app = FastAPI(title="CyePro Intelligence - Notification Prioritization Engine")

# CORS and Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize DB on startup
@app.on_event("startup")
async def startup_event():
    init_db()

# Routes
app.include_router(api.router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Welcome to CyePro Notification Prioritization Engine (AI-Native)"}

if __name__ == "__main__":
    import uvicorn
    import sys
    try:
        print("Starting CyePro Backend...")
        uvicorn.run(app, host="0.0.0.0", port=8001)
    except Exception as e:
        print(f"CRITICAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
