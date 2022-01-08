import requests
from requests.structures import CaseInsensitiveDict
from urllib.parse import urlparse, parse_qs
import json
import psutil
import time

api_endpoint = 'https://hihvs5039b.execute-api.us-east-1.amazonaws.com/beta/logging'
login_page = 'https://beemo.auth.us-east-1.amazoncognito.com/login?client_id=6umju1m19q2h8prhc3gpsk0cte&response_type=token&scope=aws.cognito.signin.user.admin+profile+openid+email+phone&redirect_uri=https://example.com/callback'
username = ''
password = ''
cognitodata = 'eyJwYXlsb2FkIjoie1wiY29udGV4dERhdGFcIjp7XCJVc2VyQWdlbnRcIjpcIk1vemlsbGEvNS4wIChXaW5kb3dzIE5UIDEwLjA7IFdpbjY0OyB4NjQ7IHJ2Ojk1LjApIEdlY2tvLzIwMTAwMTAxIEZpcmVmb3gvOTUuMFwiLFwiRGV2aWNlSWRcIjpcInBsZ3VmbzU0M21hOXNvcXF3N2ZnOjE2NDA4MzMzNjYwNDhcIixcIkRldmljZUxhbmd1YWdlXCI6XCJlbi1VU1wiLFwiRGV2aWNlRmluZ2VycHJpbnRcIjpcIk1vemlsbGEvNS4wIChXaW5kb3dzIE5UIDEwLjA7IFdpbjY0OyB4NjQ7IHJ2Ojk1LjApIEdlY2tvLzIwMTAwMTAxIEZpcmVmb3gvOTUuMGVuLVVTXCIsXCJEZXZpY2VQbGF0Zm9ybVwiOlwiV2luMzJcIixcIkNsaWVudFRpbWV6b25lXCI6XCItMDU6MDBcIn0sXCJ1c2VybmFtZVwiOlwicXVhZGVcIixcInVzZXJQb29sSWRcIjpcIlwiLFwidGltZXN0YW1wXCI6XCIxNjQwODMzOTU5NjY0XCJ9Iiwic2lnbmF0dXJlIjoicDlBeFdBTlRUSjJNZjJINzh5d1lyYWJNQ2hvR2tYeFlEU0tpRXlqcGNKST0iLCJ2ZXJzaW9uIjoiSlMyMDE3MTExNSJ9'

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
		"Host": "beemo.auth.us-east-1.amazoncognito.com",
		"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0",
		"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
		"Accept-Language": "en-US,en;q=0.5",
		"Accept-Encoding": "gzip, deflate, br",
		"Content-Type": "application/x-www-form-urlencoded",
		"Content-Length": "837",
		"Origin": "https://beemo.auth.us-east-1.amazoncognito.com",
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
	#print(r)
	#print(r.url)

	pq = parse_qs(urlparse(r.url).fragment)
	#print(pq)
	access_token = pq["access_token"][0]
	
	
	#print("{}".format(access_token))


	return access_token

def post_data(access_token,info):
	client = requests.session()

	data = json.dumps(info)
	headers = CaseInsensitiveDict()
	headers["Authorization"] = "Bearer {}".format(access_token)


	response = client.get(api_endpoint,headers=headers,data=data)

	#data = json.loads(response.text)


	#print(data)
	#print(data["body"])
	#print(data["requestContext"]["authorizer"]["claims"]['sub'])
	print(response.text)


def get_cpu():
	fake_temp = int(psutil.cpu_percent())
	dummy_data = {
    "adle0DpAHDjNdiNmswWRVX9N7HVOnH2bHvL7H4UQQH0LlwvKDJ": {
        "weight": 80.22,
        "humidity": 23,
        "temp": fake_temp,
        "battery": 99
				    }
				}
	return dummy_data



load_local_password()
current_token = get_access_token()

while(True):

	post_data(current_token,get_cpu())
	time.sleep(10)
