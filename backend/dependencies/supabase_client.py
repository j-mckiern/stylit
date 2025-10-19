from supabase import create_client
from settings import settings

supabase = create_client(settings.supabase_url, settings.supabase_service_role_key)
