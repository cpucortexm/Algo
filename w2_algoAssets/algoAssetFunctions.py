#!/usr/bin/env python3
#
# @Filename:    algoAssetFunctions.py
# @Author:      Yogesh K
# @Date:        16/12/2022
import json
import base64
from dotenv import load_dotenv
import os 
from algosdk.v2client import algod
from algosdk import account, mnemonic, constants
from algosdk.future import transaction
from algosdk.future.transaction import *

#   note: if you have an indexer instance available it may be easier to just search accounts for an asset
#   Utility function used to print created asset for account and assetid
def print_created_asset(algodclient, account, assetid):
    # note: if you have an indexer instance available it is easier to just use this
    # response = myindexer.accounts(asset_id = assetid)
    # then use 'account_info['created-assets'][0] to get info on the created asset
    account_info = algodclient.account_info(account)
    idx = 0
    for my_account_info in account_info['created-assets']:
        scrutinized_asset = account_info['created-assets'][idx]
        idx = idx + 1       
        if (scrutinized_asset['index'] == assetid):
            print("Asset ID: {}".format(scrutinized_asset['index']))
            print(json.dumps(my_account_info['params'], indent=4))
            break

#   Utility function used to print asset holding for account and assetid
def print_asset_holding(algodclient, account, assetid):
    # note: if you have an indexer instance available it is easier to just use this
    # response = myindexer.accounts(asset_id = assetid)
    # then loop thru the accounts returned and match the account you are looking for
    account_info = algodclient.account_info(account)
    idx = 0
    for my_account_info in account_info['assets']:
        scrutinized_asset = account_info['assets'][idx]
        idx = idx + 1
        if (scrutinized_asset['asset-id'] == assetid):
            print("Asset ID: {}".format(scrutinized_asset['asset-id']))
            print(json.dumps(scrutinized_asset, indent=4))
            break

def myEnvironment():
    print(f'account1: {account1}')
    print(f'PrivateKey1: {sk1}')
    print(f'mnemonic1: {mnemonic1}')

    print(f'account2: {account2}')
    print(f'PrivateKey2: {sk2}')
    print(f'mnemonic2: {mnemonic2}')

    print(f'account3: {account3}')
    print(f'PrivateKey3: {sk3}')
    print(f'mnemonic3: {mnemonic3}')

load_dotenv()
account1 = os.getenv("account1")
sk1      = os.getenv("sk1")
mnemonic1= os.getenv("mnemonic1")

account2 = os.getenv("account2")
sk2      = os.getenv("sk2")
mnemonic2= os.getenv("mnemonic2")

account3 = os.getenv("account3")
sk3      = os.getenv("sk3")
mnemonic3= os.getenv("mnemonic3")

algod_address = "https://testnet-api.algonode.cloud"
algod_token = ""
algod_client = algod.AlgodClient(algod_token, algod_address)


# CREATE AN ASSET
print("--------------------------Creating Asset-------------------------")
params = algod_client.suggested_params()
# account1 creates an asset called Encode  and
# sets account2 as the manager, reserve, freeze, and clawback address.
# Asset Creation transaction
txn = AssetConfigTxn(
    sender=account1,
    sp=params,
    total=1000,
    default_frozen=False,
    unit_name="ENCODE",
    asset_name="encode",
    manager=account2,
    reserve=account2,
    freeze=account2,
    clawback=account2,
    url="https://path/to/my/asset/details", 
    decimals=0)

# Sign with secret key of creator
signed_txn = txn.sign(sk1)

# Send the transaction to the network and retrieve the txid.
try:
    txid = algod_client.send_transaction(signed_txn)
    print("Signed transaction with txID: {}".format(txid))
    # Wait for the transaction to be confirmed
    confirmed_txn = wait_for_confirmation(algod_client, txid, 4)
    print("TXID: ", txid)
    print("Result confirmed in round: {}".format(confirmed_txn['confirmed-round']))
except Exception as err:
    print(err)

print("Transaction information: {}".format(
    json.dumps(confirmed_txn, indent=4)))

try:
    # Pull account info for the creator
    # get asset_id from tx
    # Get the new asset's information from the creator account
    ptx = algod_client.pending_transaction_info(txid)
    asset_id = ptx["asset-index"]
    print_created_asset(algod_client, account1, asset_id)
    print_asset_holding(algod_client, account1, asset_id)
except Exception as e:
    print(e)


# CHANGE MANAGER
print("--------------------------Change Manager-------------------------")
params = algod_client.suggested_params()
txn = AssetConfigTxn(
    sender=account2,
    sp=params,
    index=asset_id, 
    manager=account1, # account1 is the new manager
    reserve=account2,
    freeze=account2,
    clawback=account2)

signed_txn = txn.sign(sk2)

try:
    txid = algod_client.send_transaction(signed_txn)
    print("Signed transaction with txID: {}".format(txid))
    # Wait for the transaction to be confirmed
    confirmed_txn = wait_for_confirmation(algod_client, txid, 4) 
    print("TXID: ", txid)
    print("Result confirmed in round: {}".format(confirmed_txn['confirmed-round']))
except Exception as err:
    print(err)

print_created_asset(algod_client, account1, asset_id)

# OPT-IN
print("--------------------------Optin Asset-------------------------")
params = algod_client.suggested_params()
account_info = algod_client.account_info(account3)
holding = None
idx = 0
for my_account_info in account_info['assets']:
    scrutinized_asset = account_info['assets'][idx]
    idx = idx + 1
    if (scrutinized_asset['asset-id'] == asset_id):
        holding = True
        break
if not holding:

    # Use the AssetTransferTxn class to transfer assets and opt-in
    txn = AssetTransferTxn(
        sender=account3,
        sp=params,
        receiver=account3,  #optin account3 as receiver
        amt=0,
        index=asset_id)

    signed_txn = txn.sign(sk3)
    # Send the transaction to the network and retrieve the txid.
    try:
        txid = algod_client.send_transaction(signed_txn)
        print("Signed transaction with txID: {}".format(txid))
        # Wait for the transaction to be confirmed
        confirmed_txn = wait_for_confirmation(algod_client, txid, 4) 
        print("TXID: ", txid)
        print("Result confirmed in round: {}".format(confirmed_txn['confirmed-round']))
    except Exception as err:
        print(err)
    # Now check the asset holding for that account.
    # This should now show a holding with a balance of 0.
    print_asset_holding(algod_client, account3, asset_id)

# TRANSFER ASSET

print("--------------------------Transfer Asset-------------------------")
params = algod_client.suggested_params()
txn = AssetTransferTxn(
    sender=account1,
    sp=params,
    receiver=account3,
    amt=10,
    index=asset_id)

signed_txn = txn.sign(sk1)
# Send the transaction to the network and retrieve the txid.
try:
    txid = algod_client.send_transaction(signed_txn)
    print("Signed transaction with txID: {}".format(txid))
    # Wait for the transaction to be confirmed
    confirmed_txn = wait_for_confirmation(algod_client, txid, 4) 
    print("TXID: ", txid)
    print("Result confirmed in round: {}".format(confirmed_txn['confirmed-round']))
except Exception as err:
    print(err)
# The balance should now be 10.
print_asset_holding(algod_client, account3, asset_id)

# FREEZING ASSET
print("--------------------------Freezing Asset-------------------------")
# The freeze address (Account 2) freezes Account 3's encode holdings.
params = algod_client.suggested_params()

txn = AssetFreezeTxn(
    sender=account2,
    sp=params,
    index=asset_id,
    target=account3,
    new_freeze_state=True
    )
signed_txn = txn.sign(sk2)
# Send the transaction to the network and retrieve the txid.
try:
    txid = algod_client.send_transaction(signed_txn)
    print("Signed transaction with txID: {}".format(txid))
    # Wait for the transaction to be confirmed
    confirmed_txn = wait_for_confirmation(algod_client, txid, 4)  
    print("TXID: ", txid)
    print("Result confirmed in round: {}".format(confirmed_txn['confirmed-round']))
except Exception as err:
    print(err)
# The balance should now be 10 with frozen set to true.
print_asset_holding(algod_client, account3, asset_id)

# REVOKING AN ASSET
print("--------------------------Revoking Asset-------------------------")
# The clawback address (Account 2) revokes 10 encode from Account 3 and places it back with Account 1.
params = algod_client.suggested_params()
# Must be signed by the account that is the Asset's clawback address
txn = AssetTransferTxn(
    sender=account2,
    sp=params,
    receiver=account1,
    amt=10,
    index=asset_id,
    revocation_target=account3
    )
signed_txn = txn.sign(sk2)

# Send the transaction to the network and retrieve the txid.
try:
    txid = algod_client.send_transaction(signed_txn)
    print("Signed transaction with txID: {}".format(txid))
    # Wait for the transaction to be confirmed
    confirmed_txn = wait_for_confirmation(algod_client, txid, 4)
    print("TXID: ", txid)
    print("Result confirmed in round: {}".format(confirmed_txn['confirmed-round']))
except Exception as err:
    print(err)
# The balance of account 3 should now be 0.
# account_info = algod_client.account_info(accounts[3]['pk'])
print("Account 3")
print_asset_holding(algod_client, account3, asset_id)
# The balance of account 1 should increase by 10 to 1000.
print("Account 1")
print_asset_holding(algod_client, account1, asset_id)

# DESTROY ASSET
print("--------------------------Destroying Asset-------------------------")
# With all assets back in the creator's account,
# the manager (Account 1) destroys the asset.
params = algod_client.suggested_params()
txn = AssetConfigTxn(
    sender=account1,
    sp=params,
    index=asset_id,
    strict_empty_address_check=False
    )

# Sign with secret key of creator
signed_txn = txn.sign(sk1)
# Send the transaction to the network and retrieve the txid.

try:
    txid = algod_client.send_transaction(signed_txn)
    print("Signed transaction with txID: {}".format(txid))
    # Wait for the transaction to be confirmed
    confirmed_txn = wait_for_confirmation(algod_client, txid, 4) 
    print("TXID: ", txid)
    print("Result confirmed in round: {}".format(confirmed_txn['confirmed-round']))
except Exception as err:
    print(err)
# Asset was deleted.

try:
    print("For Account 1, nothing should print after this as the asset is destroyed on the creator account")
    print_asset_holding(algod_client, account1, asset_id)
    print_created_asset(algod_client, account1, asset_id)
except Exception as e:
    print(e)