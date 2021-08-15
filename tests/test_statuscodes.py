import requests,json

def test_statuscodes():
    url = "http://127.0.0.1:9004/api/movies-now/movies"

    payload={}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    # print(response.status_code)
    assert response.status_code == 200

    url = "http://127.0.0.1:9004/api/movies-now/cities"
    response = requests.request("GET", url, headers=headers, data=payload)
    assert response.status_code == 200



# test_statuscodes()