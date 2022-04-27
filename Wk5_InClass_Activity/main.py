import pandas as pd
import numpy as np


# first method -- drop()
#data = pd.read_csv('books.csv')
#df = pd.DataFrame(data)
#df = df.drop(columns = ['Edition Statement', 'Corporate Author', 'Corporate Contributors',
#                    'Former owner', 'Engraver', 'Issuance type', 'Shelfmarks'])

# second method -- usecols of pands.read_csv()
#data = pd.read_csv('books.csv',
#         usecols = ['Identifier', 'Date of Publication', 'Place of Publication'])
#        usecols = ['Identifier', 'Place of Publication', 'Date of Publication',
#                    'Publisher', 'Title', 'Author', 'Contributors', 'Flickr URL'])

#extr = data['Date of Publication'].str.extract(r'^(\d{4})', expand=False)
#extr.head()
#data['Date of Publication'] = pd.to_numeric(extr)
#data['Date of Publication'].dtype

#pub = data['Place of Publication']
#london = pub.str.contains('London')
#oxford = pub.str.contains('Oxford')
#data['Place of Publication'] = np.where(london, 'London',
#                                np.where(oxford, 'Oxford',
#                                  pub.str.replace('-', ' ')))

#print(data)

# Part C Tidying with applymap()
university_towns = []
with open('uniplaces.txt') as file:
    for line in file:
        if '[edit]' in line:
            state = line
        else:
            university_towns.append((state, line))
university_towns[:5]

towns_df = pd.DataFrame(university_towns, columns=['State', 'RegionName'])

def get_citystate(item):
    if '(' in item:
        return item[:item.find(' (')]
    elif '[' in item:
        return item[:item.find('[')]
    else:
        return item

towns_df = towns_df.applymap(get_citystate)
towns_df.head()

print(towns_df)
