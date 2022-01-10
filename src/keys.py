from bitcoin import SelectParams
from bitcoin.wallet import CBitcoinSecret, P2PKHBitcoinAddress
from bitcoin.core import x

SelectParams('testnet')


######################################################################
# 
# TODO: Fill this in with address secret key for BTC testnet3
#
# Create address in Base58 with keygen.py
# Send coins at https://coinfaucet.eu/en/btc-testnet/

# Only to be imported by alice.py
# Alice should have coins!!
alice_secret_key_BTC = CBitcoinSecret(
    'cNDGzQkvsZN5rigPB9qb2aoTjz9YMR8H18KVCb2wjXJ9i2i4ncar')
# Private key: cR2HMh5oEFX16UoWjs8JutpfgBFoccAQjBmmUm2auQMdaDKMKTb7
# Address: mgdg4Z5H5nGkZoQDLvgEWRcRHqnmvPxbCW
# tx: 6e19b87a0d837fe924c4205b9cffda6abe8d36d653a528bedfb6d405c6bde027
# Only to be imported by bob.py
bob_secret_key_BTC = CBitcoinSecret(
    'cR2HMh5oEFX16UoWjs8JutpfgBFoccAQjBmmUm2auQMdaDKMKTb7')
# Private key: cNDGzQkvsZN5rigPB9qb2aoTjz9YMR8H18KVCb2wjXJ9i2i4ncar
# Address: n3KBoNgtQwViTTdr57r8mHGUZWWPXVdxey
# tx: 7a03c60575610e6d2dca5fc7494099575e71e04087facadf53bd1b40d89f84c3
######################################################################
#
# TODO: Fill this in with address secret key for BCY testnet
#
# Create address in hex with
# curl -X POST https://api.blockcypher.com/v1/bcy/test/addrs?token=2f840eeeb11b4c4389e12dc411de3090
#
# Send coins with 
# curl -d '{"address": "BCY_ADDRESS", "amount": 1000000}' https://api.blockcypher.com/v1/bcy/test/faucet?token=<YOURTOKEN>

# Only to be imported by alice.py
alice_secret_key_BCY = CBitcoinSecret.from_secret_bytes(
    x('96e4085df648e4b158f458bd5cf1cb74f0bed6e64e0484778314f5555645c321'))
# {
#   "private": "c53d838a8577b5e4d1ea9058682f1b3c5d657b2227fd3ae214b2ab902f99de5a",
#   "public": "03ff3efcab293dd89670c5f5ed08828315b4569ae840aee7999f743e0f4e8e3dcf",
#   "address": "CBckY1ZnBWi469baZhDMaoWBJ4Xr4YTDew",
#   "wif": "BuwSUphtgThJPXtYfTVk8cYPjCyZJyLwKJfqGr5hthoWu8B9gRXf"
# }
#curl -d '{"address": "CBckY1ZnBWi469baZhDMaoWBJ4Xr4YTDew", "amount": 1000000}' https://api.blockcypher.com/v1/bcy/test/faucet?token=2f840eeeb11b4c4389e12dc411de3090
# {
#   "tx_ref": "1802bd055fb10f4b7cd5881b26f09446b07b1648d6dfa86298b59bf0277c3b80"
# }
# Only to be imported by bob.py
# Bob should have coins!!
bob_secret_key_BCY = CBitcoinSecret.from_secret_bytes(
    x('c53d838a8577b5e4d1ea9058682f1b3c5d657b2227fd3ae214b2ab902f99de5a'))
# {
#   "private": "96e4085df648e4b158f458bd5cf1cb74f0bed6e64e0484778314f5555645c321",
#   "public": "0322f1222781aa87099c23fc8b0c28d9540fca29712f07c3de95a495c9f592870f",
#   "address": "C8FfY4UhYb7MA3NZ7m2FdDd3dpVtzh7vWY",
#   "wif": "BtPLq2qhUBk5RgMYmAozrNGVXRuWUnqNhcknWTev6W4hFbJwD91r"
# }
#curl -d '{"address": "C8FfY4UhYb7MA3NZ7m2FdDd3dpVtzh7vWY", "amount": 1000000}' https://api.blockcypher.com/v1/bcy/test/faucet?token=2f840eeeb11b4c4389e12dc411de3090
# {
#   "tx_ref": "7984099f4e47525cbd2f7d62da568780bc726c994015c7e6bca53452a8d8d9b5"
# }
# Can be imported by alice.py or bob.py
alice_public_key_BTC = alice_secret_key_BTC.pub
alice_address_BTC = P2PKHBitcoinAddress.from_pubkey(alice_public_key_BTC)

bob_public_key_BTC = bob_secret_key_BTC.pub
bob_address_BTC = P2PKHBitcoinAddress.from_pubkey(bob_public_key_BTC)

alice_public_key_BCY = alice_secret_key_BCY.pub
alice_address_BCY = P2PKHBitcoinAddress.from_pubkey(alice_public_key_BCY)

bob_public_key_BCY = bob_secret_key_BCY.pub
bob_address_BCY = P2PKHBitcoinAddress.from_pubkey(bob_public_key_BCY)
