import os
import pandas as pd
import re
dir_path = os.path.dirname(os.path.realpath(__file__))
df = pd.read_csv(os.path.join(dir_path, 'resources/world-universities.csv'), header=None, names=['country', 'name', 'website'])

# university to country mapping
uni2country = {}
d = df.to_dict()
for k in d['name'].keys():
    university = d['name'][k].lower()
    country = d['country'][k]
    uni2country[university] = country


# normalize university name
unilist = [re.escape(x) for x in df.name.tolist()]
uniregex = '('+'|'.join(unilist)+')'
def normalize_university(text, lower=True):
    results = re.findall(uniregex, text)
    university = results[0] if results else None
    if university is not None and lower: university = university.lower()
    return university if university is not None else text


