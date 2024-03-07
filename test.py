import os
from dotenv import load_dotenv
load_dotenv()

from supabase import create_client

url=os.environ.get('SUPABASE_URL')
key=os.environ.get('SUPABASE_SERVICE_ROLE_KEY')
supabase = create_client(url, key)

res = supabase.storage.from_('image-bucket/Reports').get_public_url('Soil_Test_Report.png')
# res = supabase.storage.from_('image-bucket').upload('Tunnel_specs.png','Tunnel_specs.png',{'content-type':'image/png'})
print(res)