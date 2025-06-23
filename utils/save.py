import services.async_service.cronJob as CJ
from data.connect import supabase
from datetime import datetime

hoje = str(datetime.now().date())

res = supabase.table("series").select("*").or_(f"ultima_checagem.neq.{hoje},ultima_checagem.is.null").execute()
series = res.data

series