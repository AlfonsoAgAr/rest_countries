import dataclasses, json, time, hashlib, os
import sys; sys.path.append('../')
from request import Client
from db import DB

@dataclasses.dataclass
class Country:
    region: str
    city: str
    language: str
    time: float
    
class MainObject(Client):
    def __init__(self) -> None:
        super().__init__()        

    @property
    def all_data(self) -> list:
        return json.loads(self.get_all().text)

    def generate_hashes(self) -> None:
        """
        Generate a json file with hashes of language by country.
        """
        countries = [{x['name']['common'] : list(x['languages'])[:len(x['languages'])] if 'languages' in x else None} for x in self.all_data]
        hashed = {}

        for country in countries:
            _time = time.time()
            # To convert again in readable -> f_unhash(hash).strip('[]')
            for country, lang in country.items():
                hashed.update(
                    {country : 
                        {
                            'hash' : hashlib.sha1(str(lang).encode('utf-8')).hexdigest(),
                            'time' : (time.time() - _time) * 1000
                        }
                    })

        with open('hashes.json', 'w', encoding='utf-8') as f:
            json.dump(hashed, f, indent=4, separators=(',', ' : '), ensure_ascii=False)
        
        return None

    def creator(self) -> list:
        """
        Instance Country for every country in all_data.
        """
        if 'hashes.json' not in os.listdir():
            self.generate_hashes()
            
        with open('hashes.json', 'r', encoding='utf-8') as f:
            lang_sha1 = json.load(f)
            return [
                    Country(
                        region = x['region'],
                        city = x['name']['common'],
                        language = lang_sha1[x['name']['common']]['hash'],
                        time = lang_sha1[x['name']['common']]['time']
                        ).__dict__
                    for x in self.all_data
                    ]
    
    def save_in_json(self, path: str = None) -> None:
        """
        Store countries data in json file.
        """
        if path is None:
            path = ''
        
        with open(f'{path}coutries.json', 'w', encoding='utf-8') as f:
            json.dump(self.creator(), f, indent=4, separators=(',', ' : '), ensure_ascii=False)
        
        return None

    def save_in_db(self, db_name: str) -> None:
        """
        Store countries data in csv file.
        """
        if db_name not in os.listdir():
            database = DB(db_name)
            for element in self.creator():
                database.add(
                    region = element['region'],
                    city = element['city'],
                    lang = element['language'],
                    time = str(element['time']) + ' ms'
                )

        return None 


    
init = time.time()

a = MainObject()
a.generate_hashes()
a.save_in_json()
a.save_in_db('countries.sqlite')


# database = DB('example.sqlite')
# database.add(
#     region="America", 
#     city="Mexico City", 
#     lang="5af3a9fef0624e2d653fa183e5ac23b8a3d49ca1", 
#     table="countries"
#     )

# print(database.get_all_from('countries'))

finish = time.time()
print('Time {} s'.format(finish - init))