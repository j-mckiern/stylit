from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")
    app_name: str = "Stylit"
    
    # SUPABASE
    supabase_url: str
    supabase_anon_key: str
    supabase_service_role_key: str

    # FILES
    default_pfp_url: str

settings = Settings()
