# Import libraries
import requests
from datetime import date, timedelta
import pandas as pd
import pandas_gbq

def accuranker_to_bq():

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
    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    # Extract list of competitors & keyword
    competitors = data['competitor_ranks']
    keyword = data['keyword']

    # Defining table schema
    dates = []
    shop_names = []
    keywords = []
    ranks = []

    # Get data for each competitor
    for competitor in competitors:
        dates.append(yesterday)
        shop_names.append(competitor['competitor']['domain'])
        keywords.append(keyword)
        ranks.append(competitor['rank'])
    
    # Create final dataframe
    table = {'dates': dates, 'shop_names': shop_names, 'keywords': keywords, 'ranks': ranks}
    df = pd.DataFrame(table)

    # Store data in BQ
    project_id = 'iih-sandbox'
    destination_table = 'accuranker_poc.windturbine'
    df.to_gbq(destination_table, project_id=project_id, if_exists='append')