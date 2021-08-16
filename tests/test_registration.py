import requests, json

def test_user_registration():
    '''
    test cases checking the user registration service.
    Run these case when the service is running
    '''
    
    url = "http://127.0.0.1:9004/api/movies-now/register"

    payload = json.dumps({
    "username": "sasi",
    "password": "090702",
    "email": "gofourcrazy@gmail.com",
    "phone": 8106283277,
    "city": 1
    })
    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    # print(response.text)
    # assert response.text == '{"data": {"message": "Account already exists !"}, "status": false}'

    payload_2 = json.dumps({
    "username": "RaviT",
    "password": "090702",
    "email": "atmravi@gmail.com",
    "phone": 8106283277,
    "city": 1
    })
    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    # print(response.text)
    # assert response.text == '{"data": {"message": "You have successfully registered !"}, "status": True}'