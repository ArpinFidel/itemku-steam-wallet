import requests
from config import *

def get_exchange_rate(from_currency, to_currency) : 
    base_url = "https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE"
    main_url = base_url + "&from_currency=" + from_currency + "&to_currency=" + to_currency + "&apikey=" + currency_api_key
    req_ob = requests.get(main_url) 
    json = req_ob.json()
    return float(json["Realtime Currency Exchange Rate"]['5. Exchange Rate'])

opts_response = requests.post("https://wrapapi.com/use/Arpin/itemku/options/0.0.1", json={
    "wrapAPIKey": wrap_api_key
})
opts = opts_response.json()['data']['options']


data = {}
exc_rates = {}
n = len(opts)
for i, op in enumerate(opts):
    val_response = requests.post("https://wrapapi.com/use/Arpin/itemku/values/0.0.5", json={
        "q_item": op,
        "wrapAPIKey": wrap_api_key
    })
    val = val_response.json()['data']
    print('Loading %.1f%%'%((i+1)/n*100), val, sep='\n')

    cur = val['name'].split(' ')[0]
    nom = val['nom']
    price = val['price']

    val['name'] = cur

    if cur not in data:
        data[cur] = {}
        exc_rates[cur] = get_exchange_rate(cur, 'IDR')

    data[cur][nom] = {
        'price': price,
        'value': nom * exc_rates[cur],
        'ratio': nom * exc_rates[cur] / price
    }

print('=====================================================================')
print(' Currency ||   Nominal   ||    Value    ||    Price    ||   Ratio   ')
print('=====================================================================')
for cur, cur_data in data.items():
    print(' %-8s ||%13s||%13s||%13s||%10.2f'%(cur, '', '', '', exc_rates[cur]))
    for nom, val in cur_data.items():
        print('%10s||%12d ||Rp. %8d ||Rp. %8d ||%10.2f'%('', nom, val['value'], val['price'], val['ratio']))
    print()
input('Press enter to continue...')