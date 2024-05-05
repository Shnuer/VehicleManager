import requests
from requests.exceptions import HTTPError


def check_status_code(expected_status_codes):
    def decorator(func):
        def wrapper(*args, **kwargs):
            response = func(*args, **kwargs)
            if response.status_code not in expected_status_codes:
                raise HTTPError(
                    f"Unexpected status code: {response.status_code}"
                )
            return response
        return wrapper
    return decorator


class HTTPClient():

    def __init__(self) -> None:
        self.session = requests.Session()

    @check_status_code([requests.codes.ok])
    def get(self, url) -> requests.Response:
        return self.session.get(url)

    @check_status_code([requests.codes.created])
    def post(self, url, data) -> requests.Response:
        return self.session.post(url, data)

    @check_status_code([requests.codes.ok])
    def put(self, url, data) -> requests.Response:
        return self.session.put(url, data)

    @check_status_code([requests.codes.no_content])
    def delete(self, url) -> requests.Response:
        return self.session.delete(url)
