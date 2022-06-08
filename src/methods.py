def get_by_language(self, language: str = None) -> dict:
    """
    Get countries from a language
    
    E.g.
    
    ```
    :: MyClientObject().get_language('spa') :: -> return details of countries that speaks spanish
    ```
    """
    if language is None:
        path = '/v3.1/lang/spa'
    else:
        path = f'/v3.1/lang/{language}'

    return self.get(path=path)

def get_by_region(self, region: str = None) -> dict:
    """
    Get details from countries from a region.
    
    E.g.
    
    ```
    :: MyClientObject().get_region('ame') :: -> return details of countries from america
    ```
    """
    path = f'/v3.1/region/{region}'

    return self.get(path=path)

def get_all(self) -> dict:
    """
    Get all countries.
    
    E.g.
    
    :: MyClientObject().get_all_countries() :: -> return details of all countries
    """
    path = '/v3.1/all'

    return self.get(path=path)