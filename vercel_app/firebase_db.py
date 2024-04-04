
import firebase_admin 
from firebase_admin import credentials, db

cred = credentials.Certificate("../serviceAccountKey.json") 
firebase_admin.initialize_app(cred,{ 'databaseURL':'https://tunnel-kiln-default-rtdb.asia-southeast1.firebasedatabase.app' })

ref = db.reference("/") 

#get data from firebase db 
data_1 = ref.child('Sensor').get()

#itterate your data 
for x,y in data_1.items():
    print(x,y)