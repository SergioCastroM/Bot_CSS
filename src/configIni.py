
API_TOKEN = '1618570620:AAHa-yq9RYRoZ-FndRjZ_FLCNBQlFzFfRTE'


#Conexiones 
urlLogin = 'https://192.168.1.143:50000/b1s/v1/Login'
urlGetItem = 'http://192.168.1.143:50001/b1s/v1/Items?$filter=SalesItem eq \'tYES\''
#parameters = {"CompanyDB":"","UserName":"","Password":""}
parametersLogin =  { "UserName": "manager", "Password": "manager","CompanyDB": "VISDECOL_PRD", "Language": "23"}
headers = {'content-type': 'application/json'}