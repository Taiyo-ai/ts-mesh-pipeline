import requests

def check_url_status(url):
    try:
        response = requests.head(url)
        if response.status_code == 200:
            return f"The URL {url} is accessible (status code: {response.status_code})."
        else:
            return f"The URL {url} returned a status code: {response.status_code}."
    except requests.exceptions.RequestException as e:
        return f"An error occurred while accessing the URL {url}: {e}"


# # Usage
# result = check_url_status(url_to_check)
# print(result)
