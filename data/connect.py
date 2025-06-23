from supabase import create_client, Client

url: str = "https://alzdutzvdrysfcnklyhe.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFsemR1dHp2ZHJ5c2ZjbmtseWhlIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc0ODM4NTczNSwiZXhwIjoyMDYzOTYxNzM1fQ.FDlfibIPMDqUtrXzpzR9qdX5ZH0Eax2tJCWp1zmhfXM"
supabase: Client = create_client(url, key)