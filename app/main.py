from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from app.db import init_db, fetch_rows_by_query
from app.routers.data_explorer import router as date_explorer_router
from app.exceptions_handler import register_exception_handlers
from app.constants import DB_TABLES

# Initialize Database
init_db()

origins = ["*"]
app = FastAPI()

# Middleware for CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount the templates directory
templates = Jinja2Templates(directory="templates")

register_exception_handlers(app)

app.include_router(date_explorer_router)


@app.get("/", tags=["root"])
async def root():
    return {"DataExplorer": "Welcome to DataExplorer API"}


@app.get("/health", tags=["health-check"])
async def root():
    return {"data-explorer": "I am Batman!"}


# Route to render the upload.html
@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard_page(request: Request):
    data = fetch_rows_by_query(f"SELECT * FROM {str(DB_TABLES.GAME_ANALYTICS)}")
    return templates.TemplateResponse(
        "dashboard.html", {"request": request, "data": data}
    )


# Route to render the upload.html
@app.get("/upload", response_class=HTMLResponse)
async def upload_page(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})
