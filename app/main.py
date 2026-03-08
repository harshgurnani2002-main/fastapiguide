from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.core.config import settings

# This create a single, global app instance.
# We configure it with our project name from settings.
app = FastAPI(
    title=settings.PROJECT_NAME,
    # This disables the default OpenAPI schema generation if desired,
    # but by default it provides the beautiful /docs page.
    # docs_url="/docs",
    # openapi_url="/openapi.json"
)

# Set all CORS enabled origins from the configuration.
# This configures our app to ONLY respond to requests originating from these URLs.
# "*" means any origin, which is suitable for dev, but perilous for prod.
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,     # Allow cookies or auth headers with requests cross-origin
        allow_methods=["*"],        # Allow all standard HTTP methods
        allow_headers=["*"],        # Allow all standard HTTP headers
    )

# Registers all of our route endpoints to the FastAPI application.
# Includes the entire router tree starting from our main api_router.
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def root():
    """
    A simple health check root endpoint.
    """
    return {"message": "Welcome to the Production FastAPI Todo App! Visit /docs for the API documentation."}
