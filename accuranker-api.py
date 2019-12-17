import requests
from datetime import date, timedelta

## get current date -1
yesterday = (date.today() - timedelta(1)).strftime('%Y-%m-%d')

## get particular keyword
headers = {'Authorization': 'Token 03e2bc4cf602beade89277c2ced9932331a4df34'}
url = 'http://app.accuranker.com/api/v4/domains/149964/keywords/25047693/'
params = {
    'fields': 'domain,keyword,ranks,competitor_ranks',
    'period_from': yesterday,
    'period_to': yesterday
}
r = requests.get(url, headers=headers, params=params)
d = r.json()
l = [] # This is going to be a list of tuples sent to BQ
competitors = d['competitor_ranks']

l.append((yesterday, 'shop.vestas.com', d['keyword'], d['ranks'][0]['rank']))
for competitor in competitors:
    l.append((yesterday, competitor['competitor']['domain'], d['keyword'], competitor['rank']))

print(l)