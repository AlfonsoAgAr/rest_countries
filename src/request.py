import http.client, ssl
from typing import NewType, Union
from collections import namedtuple

url = NewType('url', str)
ResponseType = namedtuple('ResponseType', 'headers text status')

class Request(http.client.HTTPSConnection):
    """
    Simple HTTPS class wrapper inherited from HTTPSConnection.
    `https://docs.python.org/3/library/http.client.html#http.client.HTTPSConnection`

    Not third party dependencies according to mail instructions. :)

    ```
    Params:
        base_url: str
        
    E.g.
        
    :: Request(some_url) :: -> return an object that can interact with API's via HTTPS.
    ```
    """
    
    def __init__(self, base_url: Union[None, url] = None) -> None:
        self.ssl: ssl.SSLContext = ssl.create_default_context(purpose=ssl.Purpose.CLIENT_AUTH)
        self.base_url: Union[None, url] = base_url
        self.response: ResponseType = None
        self.port: int = 443
        self.timeout: int = 3
        self.headers: dict =  {
            "Content-Type": "application/json",
            "Accept":"*/*"
        }

        if self.base_url is not None:
            super().__init__(host=self.base_url, context=self.ssl, port=self.port, timeout=self.timeout)

    def get(self, path: str, url: url = None) -> Union[http.client.HTTPResponse, dict, str, None]:
        if url is not None:
            self.__init__(url)

        self.request(
            method='GET',
            url=path,
            headers=self.headers
            )

        _r = self.getresponse()

        self.response = ResponseType(
            headers = _r.getheaders(), 
            text = _r.read().decode('utf-8'), 
            status = [_r.code]
            )

        self.close()

        return self.response

class Client(Request):
    """
    Client class with readable methods to interact with restcountries.com
    """
    def __init__(self, **kwargs) -> None:
        if 'base_url' not in kwargs:
            kwargs['base_url'] = "restcountries.com"
        super().__init__(**kwargs)

    from src.methods import get_by_language
    from src.methods import get_by_region
    from src.methods import get_all