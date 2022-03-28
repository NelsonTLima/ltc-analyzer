import requests, json, concurrent.futures
from datetime import datetime
from tqdm import tqdm
from os import system
from time import sleep
system('clear') or None

# After the libraries, we get all the static information. Starting date and counters will be before while.

date = datetime.now()
starting_time = date.strftime('%d/%m/%Y         %H:%M:%S')
check_time = "There wasn't any checkpoints till now"

investment = 0
counter1 = 0
counter2 = 0
counter3 = 0
error_counter = 0

profit_list = []
for i in profit_list:
	if i != max(profit_list):
		profit_list.remove(i)

main = 0
with tqdm(total=6) as bar:
	while main == 0:

# After the while everything changes every second...

# Lists and dictionaires.
		ask_list = []
		bid_list = []
		dic_ask = {}
		dic_bid = {}
		FAIL = []

		urls = ['https://api.binance.com/api/v3/ticker/bookTicker?symbol=LTCUSDT',
                    'https://api.exchange.coinbase.com/products/LTC-USD/ticker',
                    'https://api.coinex.com/v1/market/depth',
                    'https://api.crypto.com/v2/public/get-book?instrument_name=LTC_USDT&depth=10',
                    'https://ftx.com/api/markets/ltc/usdt',
                    'https://api.gateio.ws/api/v4/spot/order_book?currency_pair=LTC_USDT']

		headers = {
			'Accept': 'application/json',
  			'Content-Type': 'application/json',
  			'User-Agent': 'aUserAgent'
		}

		params = ''

#Functions: the fist one is the standard funtion for every exchange to get data. The others are for geting the specific information we need (ask and bid).

		def get_data(url, headers, params):
			if url == urls[2]:
				params = {'market': 'LTCUSDT', 'merge': '0.00001', 'limit': 1}
			request = requests.request(
				"GET", url, headers=headers, params=params, timeout=2)
			response = request.json()
			return response

		def binance():
			ask = float(response['askPrice'])
			bid = float(response['bidPrice'])
			list_update(name, ask, bid)

		def coinbase():
			ask = float(response['ask'])
			bid = float(response['bid'])
			list_update(name, ask, bid)

		def coinex():
			data = (response['data'])
			askslist = data['asks']
			bidslist = data['bids']
			asks = (askslist[0])
			ask = float(asks[0])
			bids = (bidslist[0])
			bid = float(bids[0])
			list_update(name, ask, bid)

		def cro():
			result = response['result']
			data = result['data']
			dic = data[0]
			asks = (dic['asks'])
			lowestask = (asks[0])
			ask = float(lowestask[0])
			bids = (dic['bids'])
			highestbid = (bids[0])
			bid = float(highestbid[0])
			list_update(name, ask, bid)

		def ftx():
			result = response['result']
			ask = float(result['ask'])
			bid = float(result['bid'])
			list_update(name, ask, bid)

		def gateio():
			asks = response['asks']
			lowestask = asks[0]
			ask = float(lowestask[0])
			bids = response['bids']
			highestbid = bids[0]
			bid = float(highestbid[0])
			list_update(name, ask, bid)

# These two next functions are for updating the lists and dictionaires.
		
		def list_update(name, ask, bid):
			ask_list.append(ask)
			bid_list.append(bid)
			ask_update = {name: ask}
			dic_ask.update(ask_update)
			bid_update = {name: bid}
			dic_bid.update(bid_update)

		def list(dictionary, element):
			local_list = []
			for key in dictionary.keys():
				if dictionary[key] == element:
					local_list.append(key)
			return local_list

# These two are the main equations to the software. 
		
		def result():
			total_amount = float(
				(((investment - ltc_fee)*selling_price)/buying_price) - usdt_fee)
			return total_amount

		def profit():
			amount = total_amount - investment
			percentage = (amount/investment)*100
			return amount, percentage

# In the next lines we create 6 simultaneous threads for raising software speed and accuracy. Now we can accces the urls about 5 times faster.

		with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
			future_to_url = {executor.submit(get_data, url, headers, params): url for url in urls}
			for future in concurrent.futures.as_completed(future_to_url):
				url = future_to_url[future]
				bar.update()

# Now we need to put names for thracing where does the results of every "url" come from.

				if url == urls[0]:
					name = 'BINANCE'
				elif url == urls[1]:
					name = 'COINBASE'
				elif url == urls[2]:
					name = 'COINEX'
					params = {'market': 'LTCUSDT', 'merge': '0.00001', 'limit': 1}
				elif url == urls[3]:
					name = 'CRYPTO.COM'
				elif url == urls[4]:
					name = 'FTX'
				else:
					name = 'GATEIO'

# Now we execute the specific tasks for every exchange. I could be more economic if i have done it in the last step, but it would ruin the exception due to not naming the exchanges before "try".			

				try:
					response = future.result()
					if url == urls[0]:
						binance()
					elif url == urls[1]:
						coinbase()
					elif url == urls[2]:
						coinex()
					elif url == urls[3]:
						cro()
					elif url == urls[4]:
						ftx()
					else:
						gateio()
				except:
					FAIL.append(name)
					error_counter += 1

# Now we stablish variables and make some rules.

		try:
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
				amount, percentage = profit()

				if buying_exchanges != selling_exchanges:
					profit_list.append(percentage)

				if percentage >= 0.1:
					counter1 += 1

				if percentage >= 0.15:
					counter2 += 1

				if percentage >= 0.2:
					counter3 = counter3 + 1

				checkpoint = datetime.now()
				check_time = checkpoint.strftime('%d/%m/%Y         %H:%M:%S')

# And finaly we have the prints with all the outputs.

				system('clear') or None

				print(f'Starting time:\n{starting_time}\n')
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
				if len(FAIL) >= 1:
					print("\nWe couldn't connect:")
					for i in FAIL:
						print(i)
				print(f'\nConnecting attempts failed {error_counter} times.')

				print(f'\nLast checkpoint:\n{check_time}\n\n')

# In case of there's no internet.

		except:
			error_counter -= 6
			currentime = datetime.now()
			current_time = currentime.strftime('%d/%m/%Y         %H:%M:%S')

			system('clear') or None
			print("WE COUDN'T LOAD ANY DATA.\nCHECK YOUR CONNECTION.\n\n")
			print(f'Starting time:\n{starting_time}\n')
			print(f'Current time:\n{current_time}\n')
			print(f'Last checkpoint:\n{check_time}\n')
			sleep(0.98)