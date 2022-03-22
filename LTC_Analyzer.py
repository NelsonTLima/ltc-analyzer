import requests
import json
from datetime import datetime
from os import system
from tqdm import tqdm

system('clear') or None

date = datetime.now()
date_begining = date.strftime('%d/%m/%Y         %H:%M:%S')

investment = 0
counter1 = 0
counter2 = 0
counter3 = 0

profit_list = []
for i in profit_list:
	if i != max(profit_list):
		profit_list.remove (i)

main = 0
with tqdm(total=7) as bar:
	while main == 0:

		ask_list = []
		bid_list = []
		dic_ask = {}
		dic_bid = {}

		headers = {
			'Accept': 'application/json',
  			'Content-Type': 'application/json',
  			'User-Agent': 'aUserAgent'
			}

		params = ''

		class Exchanges:
			name = 'none'
			params = ''
			def __init__(self, name):
				self.name = name

			def get_data(url, params):
				params = params
				request = requests.request("GET", url, headers=headers, params=params)
				response = request.json()
				return response

			def list_update(name, ask, bid):
				ask_list.append(ask)
				bid_list.append(bid)
				ask_update = {name: ask}
				dic_ask.update(ask_update)
				bid_update = {name: bid}
				dic_bid.update(bid_update)
	
			def ERROR_01(name):
				print(f"There was any problem trying to access {name}'s API.")

		class Binance(Exchanges):
			name = 'BINANCE'
			url = 'https://api.binance.com/api/v3/ticker/bookTicker?symbol=LTCUSDT'
			try:
				response = Exchanges.get_data(url, params)
				ask = float(response['askPrice'])
				bid = float(response['bidPrice'])
				Exchanges.list_update(name, ask, bid)
			except:
				Exchanges.ERROR_01(name)
			bar.update(1)

		class Coinbase(Exchanges):
			name = 'COINBASE'
			url = 'https://api.exchange.coinbase.com/products/LTC-USD/ticker'
			try:
				response = Exchanges.get_data(url, params)
				ask = float(response['ask'])
				bid = float(response['bid'])
				Exchanges.list_update(name, ask, bid)
			except:
				Exchanges.ERROR_01(name)
			bar.update(2)

		class Coinex(Exchanges):
			name = 'COINEX'
			url = 'https://api.coinex.com/v1/market/depth'
			try:
				params = {'market': 'LTCUSDT', 'merge': '0.00001', 'limit': 1}
				response = Exchanges.get_data(url, params)
				data = (response['data'])
				askslist = data['asks']
				bidslist = data['bids']
				asks = (askslist[0])
				ask = float(asks[0])
				bids = (bidslist[0])
				bid = float(bids[0])
				Exchanges.list_update(name, ask, bid)
			except:
				Exchanges.ERROR_01(name)
			bar.update(3)

		class Cro(Exchanges):
			name = 'CRYPTO.COM'
			url = 'https://api.crypto.com/v2/public/get-book?instrument_name=LTC_USDT&depth=10'
			try:
				response = Exchanges.get_data(url, params)
				result = response['result']
				data = result['data']
				dic = data[0]
				asks = (dic['asks'])
				lowestask = (asks[0])
				ask = float(lowestask[0])
				bids = (dic['bids'])
				highestbid = (bids[0])
				bid = float(highestbid[0])
				Exchanges.list_update(name, ask, bid)
			except:
				Exchanges.ERROR_01(name)
			bar.update(4)

		class Ftx(Exchanges):
			name = 'FTX'
			url = 'https://ftx.com/api/markets/ltc/usdt'
			try:	
				response = Exchanges.get_data(url, params)
				result = response['result']
				ask = float(result['ask'])
				bid = float(result['bid'])
				Exchanges.list_update(name, ask, bid)
			except:
				Exchanges.ERROR_01(name)
			bar.update(5)

		class Gateio(Exchanges):
			name = 'GATEIO'
			url = 'https://api.gateio.ws/api/v4/spot/order_book?currency_pair=LTC_USDT'
			try:		
				response = Exchanges.get_data(url, params)
				asks = response['asks']
				lowestask = asks[0]
				ask = float(lowestask[0])
				bids = response['bids']
				highestbid = bids[0]
				bid = float(highestbid[0])
				Exchanges.list_update(name, ask, bid)
			except:
				Exchanges.ERROR_01(name)
			bar.update(6)

		def list(dictionary, element):
			local_list = []
			for key in dictionary.keys():
				if dictionary[key] == element:
					local_list.append(key)
			return local_list

		def result():
			total_amount = float((((investment - ltc_fee)*selling_price)/buying_price) - usdt_fee)
			return total_amount

		def profit():
			percentage = (total_amount - investment)/100
			amount = total_amount - investment
			return percentage, amount
		
		selling_price = float(max(ask_list))
		buying_price = float(min(bid_list))
		element = selling_price
		dictionary = dic_ask
		selling_exchanges = list(dictionary, element)
		element = buying_price
		dictionary = dic_bid
		buying_exchanges = list(dictionary, element)
		if buying_exchanges == selling_exchanges:
			ltc_fee = 0
			usdt_fee = 0
		else:
			ltc_fee = 0.001 * buying_price
			usdt_fee = 1
		fees = ltc_fee + usdt_fee
		
		total_amount = result()

		while total_amount <= float(investment):
			total_amount = result()
			investment = float(investment) + 1
		else:
			amount = result()
			percentage, amount = profit()

			if buying_exchanges != selling_exchanges:
				profit_list.append(percentage)

			if percentage >= 0.1:
				counter1 = counter1 + 1
	
			if percentage >= 0.15:
				counter2 = counter2 + 1

			if percentage >= 0.2:
				counter3 = counter3 + 1

			date = datetime.now()
			date_text = date.strftime('%d/%m/%Y         %H:%M:%S')
			bar.update(7)

			system('clear') or None
			
			print(f'Iniciating time:\n{date_begining}\n')
			print('Buying exchanges:')
			for i in buying_exchanges:
				print(i)
			print('\nSelling exchanges:')
			for i in selling_exchanges:
				print(i)
			print(f'\nBuying price: ${buying_price} USD')
			print(f'Selling price: ${selling_price} USD')
			print(f'Least needed: ${investment} USD')
			print('Total amount gained: $%.2f USD' % total_amount)
			print('Profit: $%.2f USD' % amount)
			print("Percentage: " + format(percentage, '.2f') + str('%'))
			print('Fees: $%.2f USD\n\n' % fees)
			print(f'Profit > 0.10 %: {counter1} times')
			print(f'Profit > 0.15 %: {counter2} times')
			print(f'Profit > 0.20 %: {counter3} times')
			print("Max profit: " + format(max(profit_list), '.2f') + str('%'))
			print(f'\nLast checkpoint\n{date_text}')