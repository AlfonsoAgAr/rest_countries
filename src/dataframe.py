import pandas as pd
from db import DB

database = DB('countries.sqlite')

df = pd.DataFrame(database.get_all_from('countries'), columns = ['Region', 'City', 'Language', 'Time'])
print(df)