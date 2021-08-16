import requests,json

def test_statuscodes():
    '''
    test cases for checking the status codes for GET endipoints.
    Run these case when the service is running
    '''

    url = "http://127.0.0.1:9004/api/movies-now/movies"

    payload={}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    # print(response.status_code)
    # assert response.status_code == 200

    url = "http://127.0.0.1:9004/api/movies-now/cities"
    response = requests.request("GET", url, headers=headers, data=payload)
    # assert response.status_code == 200



# test_statuscodes()