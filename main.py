import os

from eth_account import Account
from dotenv import load_dotenv
from mnemonic import Mnemonic
from web3 import Web3

load_dotenv()

# --------------------------------------------------------
def get_private_key_from_mnemonic(mnemonic_words):
    mnemo = Mnemonic("english")
    try:
        # ایجاد حساب از عبارت mnemonic و استخراج کلید خصوصی
        account = Account.from_mnemonic(mnemonic_words)
        private_key = account.key.hex()
        return private_key
    except Exception as e:
        print(f"Error in get_private_key_from_mnemonic: {e}")
        return None

# --------------------------------------------------------

def get_public_key_from_private(privateKey):
    try:
        account = Account.from_key(privateKey)
        private_key = account.key.hex()  
        public_key = account.address
        return private_key, public_key
    except Exception as e:
        print(f"Error in get_public_key_from_private: {e}")
        return None, None

# --------------------------------------------------------

infura = [""] * 100  
balance = [0] * 100   

# مقداردهی آرایه infura
infura[0] = os.getenv("ENDPOINT")
input_string = os.getenv("SECRET_PHRASE")

Account.enable_unaudited_hdwallet_features()
mnemonic_words = input_string

private_key = get_private_key_from_mnemonic(mnemonic_words)
if private_key is None:
    print("Failed to get private key from mnemonic.")
else:
    private_key, public_key = get_public_key_from_private(private_key)
    if public_key is None:
        print("Failed to get public key from private key.")
    else:
        try:
            w3 = Web3(Web3.HTTPProvider(infura[0]))
            if w3.is_connected():
                try:
                    balance[0] = w3.eth.get_balance(public_key)
                    print(f"URL: {infura[0]} \nBalance: {balance[0] / 10**18} ETH\n")
                except Exception as e:
                    print(f"Error getting balance: {e}")
            else:
                print("Failed to connect to the Ethereum network.")
        except Exception as e:
            print(f"Error creating Web3 instance: {e}")
