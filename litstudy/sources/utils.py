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


def aff_is_interesting(aff, skip_country_codes=['CN', 'US', 'HK', 'MO']):
    aff_name = aff.name if not isinstance(aff, str) else aff
    country = uni2country.get(aff_name, 'N/A')
    if country == 'N/A' and ' and ' in aff_name:
        country = uni2country.get(aff_name.replace(' and ', ' & '), 'N/A')
    if country == 'N/A' and ' at ' in aff_name:
        country = uni2country.get(aff_name.replace(' at ', ', '), 'N/A')
    if country == 'N/A' and ' at ' in aff_name:
        country = uni2country.get(aff_name.replace(' at ', ' '), 'N/A')
    if country == 'N/A' and ' at ' in aff_name:
        country = uni2country.get(aff_name.replace(' at ', ' - '), 'N/A')
    if country == 'N/A' and ' - ' in aff_name:
        country = uni2country.get(aff_name.replace(' - ', ', '), 'N/A')
    if country == 'N/A' and ' - ' in aff_name:
        country = uni2country.get(aff_name.replace(' - ', ' '), 'N/A')
    if country == 'N/A' and ' - ' in aff_name:
        country = uni2country.get(aff_name.replace(' - ', ' at '), 'N/A')
    # Beijing University of Technology is sometimes listed as University of Technology,
    # so let's just skip it
    if aff_name.lower() == 'university of technology': return False

    skip = ['N/A']
    skip.extend(skip_country_codes)

    return country not in skip

