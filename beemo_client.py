import requests
from urllib.parse import urlparse, parse_qs
import json

api_endpoint = 'https://2y6rc9h109.execute-api.us-east-2.amazonaws.com/Beta/logging'
login_page = 'https://beemo.auth.us-east-2.amazoncognito.com/login?client_id=2tiv9nlod0nab4q48jdnmn6a9a&response_type=token&scope=aws.cognito.signin.user.admin+email+openid+phone+profile&redirect_uri=https://example.com/callback'
username = ''
password = ''
cognitodata = 'eyJwYXlsb2FkIjoie1wiY29udGV4dERhdGFcIjp7XCJVc2VyQWdlbnRcIjpcIk1vemlsbGEvNS4wIChXaW5kb3dzIE5UIDEwLjA7IFdpbjY0OyB4NjQ7IHJ2Ojk1LjApIEdlY2tvLzIwMTAwMTAxIEZpcmVmb3gvOTUuMFwiLFwiRGV2aWNlSWRcIjpcIjljbGV2N3ZvNGttODM3YXB1cjh5OjE2NDAzNjEwNTU1NDJcIixcIkRldmljZUxhbmd1YWdlXCI6XCJlbi1VU1wiLFwiRGV2aWNlRmluZ2VycHJpbnRcIjpcIk1vemlsbGEvNS4wIChXaW5kb3dzIE5UIDEwLjA7IFdpbjY0OyB4NjQ7IHJ2Ojk1LjApIEdlY2tvLzIwMTAwMTAxIEZpcmVmb3gvOTUuMGVuLVVTXCIsXCJEZXZpY2VQbGF0Zm9ybVwiOlwiV2luMzJcIixcIkNsaWVudFRpbWV6b25lXCI6XCItMDU6MDBcIn0sXCJ1c2VybmFtZVwiOlwicXVhZGVcIixcInVzZXJQb29sSWRcIjpcIlwiLFwidGltZXN0YW1wXCI6XCIxNjQwMzYxMTM2OTA3XCJ9Iiwic2lnbmF0dXJlIjoiM1dTYmVkY3V5UUpaVEdjNHNxQzdwRE9PK1ZPd3hTdlRXWDkvSFRjb3NUTT0iLCJ2ZXJzaW9uIjoiSlMyMDE3MTExNSJ9'
#body

def load_local_password():
	myfile = open("secrets.txt", "r")
	global username
	global password
	username = myfile.readline()
	username = username.replace('\n','')
	password = myfile.readline()
	password = password.replace('\n','')
	myfile.close()
	



def get_access_token():

	client = requests.session()
	client.get(login_page)
	csrf = client.cookies['XSRF-TOKEN']

	body = "_csrf={}&username={}&password={}&cognitoAsfData={}&signInSubmitButton=Sign+in".format(csrf,username,password,cognitodata)
	headers = {
		"Host": "beemo.auth.us-east-2.amazoncognito.com",
		"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0",
		"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
		"Accept-Language": "en-US,en;q=0.5",
		"Accept-Encoding": "gzip, deflate, br",
		"Content-Type": "application/x-www-form-urlencoded",
		"Content-Length": "837",
		"Origin": "https://beemo.auth.us-east-2.amazoncognito.com",
		"DNT": "1",
		"Connection": "keep-alive",
		"Referer": login_page,
		"Cookie": "XSRF-TOKEN={}".format(csrf),
		"Upgrade-Insecure-Requests": "1",
		"Sec-Fetch-Dest": "document",
		"Sec-Fetch-Mode": "navigate",
		"Sec-Fetch-Site": "same-origin",
		"Sec-Fetch-User": "?1",
		"TE": "trailers"
	}

	r = client.post(login_page,data=body,headers=headers)

	pq = parse_qs(urlparse(r.url).fragment)
	access_token = pq["access_token"][0]
	#print("{}".format(access_token))

	return access_token

def post_data(access_token,info=None):
	client = requests.session()

	dummy_data = {
    "hive1": {
        "weight": 80,
        "humidity": 77,
        "temp": 34,
        "battery": 99
    },
    "hive2": {
        "weight": 83,
        "humidity": 64,
        "temp": 55,
        "battery": 89
    }
}

	data = json.dumps(dummy_data)
	headers = {
	"Authorization" : access_token
	}


	response = client.get(api_endpoint,headers=headers,data=data)

	data = json.loads(response.text)

	print(data["body"])
	#print(data["requestContext"]["authorizer"]["claims"])


load_local_password()
#print(username)
current_token = get_access_token()
post_data(current_token)


    