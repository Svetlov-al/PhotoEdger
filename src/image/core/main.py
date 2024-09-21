import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from src.image.config import IMAGE_FILES_PATH
from src.image.entrypoints import healthcheck, image_list, load_image

app = FastAPI(
    title="PhotoEdger",
    docs_url="/swagger",
    redoc_url="/redoc"
)

app.mount(
    f"/api/images/{IMAGE_FILES_PATH}", StaticFiles(directory=f"/{IMAGE_FILES_PATH}"),
    name="image_files"
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

app.add_middleware(
    CORSMiddleware,  # type: ignore
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(healthcheck.router, prefix="/healthcheck", tags=["healthcheck"])
app.include_router(load_image.router, prefix="/api", tags=["Images"])
app.include_router(image_list.router, prefix="/api", tags=["Images"])
