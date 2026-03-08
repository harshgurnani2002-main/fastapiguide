from typing import List, Union
from pydantic import AnyHttpUrl, validator
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    Application Settings configuration class.
    This class inherits from Pydantic's BaseSettings to automatically
    load variables from environment variables or a .env file.
    """
    
    # The name of our application
    PROJECT_NAME: str = "FastAPI Production Todo App"
    
    # A list of allowed origins for Cross-Origin Resource Sharing (CORS)
    # This prevents malicious websites from making requests to our API on behalf
    # of an authenticated user.
    BACKEND_CORS_ORIGINS: List[str] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        """
        Validator to ensure CORS origins are correctly parsed from a string
        to a list if they are provided as a single string.
        """
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # JWT Authentication configuration settings
    # The secret key is used to sign the JWTs. Never hardcode this in prod!
    SECRET_KEY: str
    
    # The algorithm used to sign the JWT. HS256 is the standard.
    ALGORITHM: str = "HS256"
    
    # How long an access token is valid for, in minutes.
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # The connection string for the database
    # For SQLite, it usually looks like "sqlite:///./sql_app.db"
    DATABASE_URL: str

    class Config:
        """
        Pydantic config subclass to define settings source and behavior.
        """
        # Tells Pydantic to read these default from the .env file
        env_file = ".env"
        # Since we might be running tests where certain env vars aren't strictly
        # loaded or needed in the same way, we can be case sensitive matching.
        case_sensitive = True

# We create a single instance of settings to be imported and used globally
settings = Settings()
