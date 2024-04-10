import blockcypher

bitcoin_addresses = []

def add_address(address):
    if address not in bitcoin_addresses:
        bitcoin_addresses.append(address)

def remove_address(address):
    if address in bitcoin_addresses:
        bitcoin_addresses.remove(address)

def sync_transactions():
    transactions_info = {}
    for address in bitcoin_addresses:
        address_info = blockcypher.get_address_details(address, coin_symbol='btc')
        balance = address_info['balance'] / 10**8
        transactions = len(address_info['txrefs'])
        transactions_info[address] = {'balance': balance, 'transactions': transactions}
    return transactions_info

