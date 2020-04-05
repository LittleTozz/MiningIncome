from array import array
from datetime import datetime, timedelta
import requests

# online = res['minerCharts'][1]['workerOnline']

def PayMiner(currency, address, time, currencyExchange):

    if (time == 'день')      : time = 1
    elif (time == 'неделя')  : time = 7
    elif (time == 'месяц')   : time = 31
    elif (time == 'год')     : time = 365

    if (currency == 'eth')   : currencyUnit = 9
    elif (currency == 'btg') : currencyUnit = 8

    result = requests.get('https://' + currency + '.2miners.com/api/accounts/' + address)
    res = result.json()
    
    balance = res['stats']['balance']

    balancePay = 0
    paymentsTotal = res['paymentsTotal']
    for pay in range(paymentsTotal):
        timestamp = res['payments'][pay]['timestamp']
        payTime = datetime.utcfromtimestamp(timestamp)
        prevMount = datetime.now() - timedelta(time)
        if payTime > prevMount:
            balancePay += res['payments'][pay]['amount']

    totalBalans = balance + balancePay

    strRotalBalans = str(totalBalans)
    newStrRotalBalans = ''
    helpParam = 0
    for key in range(9):
        if key == 1:
            newStrRotalBalans += '.'
        if key > currencyUnit - len(strRotalBalans):
            newStrRotalBalans += strRotalBalans[helpParam]
            helpParam += 1
        else:
            newStrRotalBalans += '0'

    totalBalans = newStrRotalBalans

    result = requests.get('https://api.binance.com/api/v3/ticker/price?symbol=' + currencyExchange)
    res = result.json()

    price = res['price']

    return float(totalBalans) * float(price)