"""
Configuration package initialization.
"""

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    """
    port: int = Field(..., alias="PORT", description="Port number for the server")
    debug: bool = Field(..., alias="DEBUG", description="Debug mode flag")
    vapi_base_url: str = Field(..., alias="VAPI_BASE_URL", description="Base URL for the VAPI service")
    vapi_api_key: str = Field(..., alias="VAPI_API_KEY", description="API key for VAPI authentication")
    openai_api_key: str = Field(..., alias="OPENAI_API_KEY", description="API key for OpenAI services")
    google_api_key: str = Field(..., alias="GOOGLE_API_KEY", description="API key for Google services")
    
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        case_sensitive=True,
        extra='ignore',
        populate_by_name=True
    )

# Create a singleton settings object
settings = Settings() 

env_file = ".env"