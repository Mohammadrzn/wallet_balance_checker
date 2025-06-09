import os

from web3 import Web3
from dotenv import load_dotenv
from eth_account import Account

load_dotenv()

# === HARD-CODED MNEMONIC ===
mnemonic_phrase = os.getenv("SECRET_PHRASE")

# === Derive Address from Mnemonic ===
Account.enable_unaudited_hdwallet_features()
try:
    account = Account.from_mnemonic(mnemonic_phrase)
    wallet_address = account.address
    print(f"\n🔑 Wallet Address: {wallet_address}")
except Exception as e:
    print(f"Error: {e}")
    exit(1)

# === List of EVM-Compatible Chains ===
chains = {
    "Ethereum": {
        "rpc": "https://mainnet.infura.io/v3/a5bc4afbdb2b4513bec2a518396ecbb5",
        "symbol": "ETH"
    },
    "Binance Smart Chain": {
        "rpc": "https://bsc-dataseed.binance.org/",
        "symbol": "BNB"
    },
    "Polygon": {
        "rpc": "https://polygon-rpc.com",
        "symbol": "MATIC"
    },
    "Core DAO": {
        "rpc": "https://rpc.coredao.org",
        "symbol": "CORE"
    },
    "Avalanche": {
        "rpc": "https://api.avax.network/ext/bc/C/rpc",
        "symbol": "AVAX"
    },
    "Arbitrum One": {
        "rpc": "https://arb1.arbitrum.io/rpc",
        "symbol": "ETH"
    },
    "Optimism": {
        "rpc": "https://mainnet.optimism.io",
        "symbol": "ETH"
    },
    "Fantom": {
        "rpc": "https://rpc.ankr.com/fantom/cf1e29b95c620a84a0798a58332389e0570f3d1af77ee50d7f024413d9948e00",
        "symbol": "FTM"
    },
    "Base": {
        "rpc": "https://mainnet.base.org",
        "symbol": "ETH"
    },
    "zkSync Era": {
        "rpc": "https://mainnet.era.zksync.io",
        "symbol": "ETH"
    }
}

# === Scan for Native Balances ===
print("\n🔍 Scanning for native coin balances across chains...\n")
found_any = False

for name, info in chains.items():
    try:
        w3 = Web3(Web3.HTTPProvider(info["rpc"]))
        if not w3.is_connected():
            print(f"❌ {name}: RPC not reachable.")
            continue
        balance_wei = w3.eth.get_balance(wallet_address)
        balance = Web3.from_wei(balance_wei, 'ether')
        if balance > 0:
            found_any = True
            print(f"✅ {name}: {balance:.6f} {info['symbol']}")
        else:
            print(f"{name}: 0 {info['symbol']}")
    except Exception as e:
        print(f"❌ {name}: Error - {e}")

if not found_any:
    print("\n🕵️ No coins found across scanned networks.")
else:
    print("\n🎉 Done scanning! Native balances found.")
