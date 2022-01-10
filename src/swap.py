import time
import alice
import bob


######################################################################
#                                                                    #
#                                                                    #
#              CS251 Project 2: Cross-chain Atomic Swap              #
#                                                                    #
#                                                                    #
#                                                                    #
#              Written by:                                           #
#              November 16, 2021                                     #
#              Version 1.0.1                                         #
#                                                                    #
######################################################################
#
# In this assignment we will implement a cross-chain atomic swap
# between two parties, Alice and Bob.
#
# Alice has bitcoin on BTC Testnet3 (the standard bitcoin testnet).
# Bob has bitcoin on BCY Testnet (Blockcypher's Bitcoin testnet).
# They want to trade ownership of their respective coins securely,
# something that can't be done with a simple transaction because
# they are on different blockchains.
#
# This method also works between other cryptocurrencies and altcoins,
# for example trading n Bitcoin for m Litecoin.
# 
# The idea here is to set up transactions around a secret x, that
# only one party (Alice) knows. In these transactions only H(x) 
# will be published, leaving x secret. 
# 
# Transactions will be set up in such a way that once x is revealed,
# both parties can redeem the coins sent by the other party.
#
# If x is never revealed, both parties will be able to retrieve their
# original coins safely, without help from the other.
#
#
#
######################################################################
#                           BTC Testnet3                             #     
######################################################################
#
# Alice ----> UTXO ----> Bob (with x)
#               |
#               |
#               V
#             Alice (after 48 hours)
#
######################################################################
#                            BCY Testnet                             #
######################################################################
#
#   Bob ----> UTXO ----> Alice (with x)
#               |
#               |
#               V
#              Bob (after 24 hours)
#
######################################################################

######################################################################
#
# Configured for your addresses
# 
# TODO: Fill in all of these fields
#

#BTC
alice_txid_to_spend     = "a743c0266785645c48987c94d46525be3bb483925d7e481bf46eaa57b6ab9600" 
alice_utxo_index        = 2
alice_amount_to_send    = 0.0003

#BCY
bob_txid_to_spend       = "277a8e969e0dda38b4f0c43429aa3f1ed593daf72f707f91d6caf825e6dc191e"
bob_utxo_index          = 2
bob_amount_to_send      = 0.0003

# Get current block height (for locktime) in 'height' parameter for each blockchain (and put it into swap.py):
#  curl https://api.blockcypher.com/v1/btc/test3
btc_test3_chain_height  = 2106460

#  curl https://api.blockcypher.com/v1/bcy/test3
bcy_test_chain_height   = 61090

# Parameter for how long Alice/Bob should have to wait before they can take back their coins
## alice_locktime MUST be > bob_locktime
alice_locktime = 5
bob_locktime = 3

tx_fee = 0.0001

broadcast_transactions = True
# broadcast_transactions = True
# alice_redeems = True
alice_redeems = False

#
#
######################################################################


######################################################################
#
# Read the following function.
# 
# There's nothing to implement here, but it outlines the structure
# of how Alice and Bob will communicate to perform this cross-
# chain atomic swap.
#
# You will run swap.py to test your code.
#
######################################################################

def atomic_swap(broadcast_transactions=True, alice_redeems=True):
    # Alice reveals the hash of her secret x but not the secret itself
    hash_of_secret = alice.hash_of_secret()

    # Alice creates a transaction redeemable by Bob (with x) or by Bob and Alice
    alice_swap_tx, alice_swap_scriptPubKey = alice.alice_swap_tx(
        alice_txid_to_spend,
        alice_utxo_index,
        alice_amount_to_send - tx_fee,
    )

    # Alice creates a time-locked transaction to return coins to herself
    alice_return_coins_tx = alice.return_coins_tx(
        alice_amount_to_send - (2 * tx_fee),
        alice_swap_tx,
        btc_test3_chain_height + alice_locktime,
        alice_swap_scriptPubKey,
    )

    # Alice asks Bob to sign her transaction
    bob_signature_BTC = bob.sign_BTC(alice_return_coins_tx, alice_swap_scriptPubKey)

    # Alice broadcasts her first transaction, only after Bob signs this one
    if broadcast_transactions:
        alice.broadcast_BTC(alice_swap_tx)

    # The same situation occurs, with roles reversed
    bob_swap_tx, bob_swap_scriptPubKey = bob.bob_swap_tx(
        bob_txid_to_spend,
        bob_utxo_index,
        bob_amount_to_send - tx_fee,
        hash_of_secret,
    )
    bob_return_coins_tx = bob.return_coins_tx(
        bob_amount_to_send - (2 * tx_fee),
        bob_swap_tx,
        bcy_test_chain_height + bob_locktime,
    )

    alice_signature_BCY = alice.sign_BCY(bob_return_coins_tx, bob_swap_scriptPubKey)

    if broadcast_transactions:
        bob.broadcast_BCY(bob_swap_tx)

    # if broadcast_transactions:
    #     print('Sleeping for 20 minutes to let transactions confirm...')
    #     time.sleep(60 * 20)

    if alice_redeems:
        # Alice redeems her coins, revealing x publicly (it's now on the blockchain)
        alice_redeem_tx, alice_secret_x = alice.redeem_swap(
            bob_amount_to_send - (2 * tx_fee),
            bob_swap_tx,
            bob_swap_scriptPubKey,
        )
        if broadcast_transactions:
            alice.broadcast_BCY(alice_redeem_tx)

        # Once x is revealed, Bob may also redeem his coins
        bob_redeem_tx = bob.redeem_swap(
            alice_amount_to_send - (2 * tx_fee),
            alice_swap_tx,
            alice_swap_scriptPubKey,
            alice_secret_x,
        )
        if broadcast_transactions:
            bob.broadcast_BTC(bob_redeem_tx)
    else:
        
        # Bob and Alice may take back their original coins after the specified time has passed
        completed_bob_return_tx = bob.complete_return_tx(
            bob_return_coins_tx,
            bob_swap_scriptPubKey,
            alice_signature_BCY,
        )
        completed_alice_return_tx = alice.complete_return_tx(
            alice_return_coins_tx,
            alice_swap_scriptPubKey,
            bob_signature_BTC,
        )
        if broadcast_transactions:
            print('Sleeping for bob_locktime blocks to pass locktime...')
            # time.sleep(10 * 60 * bob_locktime)
            bob.broadcast_BCY(completed_bob_return_tx)

            print('Sleeping for alice_locktime blocks to pass locktime...')
            # time.sleep(10 * 60 * max(alice_locktime - bob_locktime, 0))
            alice.broadcast_BTC(completed_alice_return_tx)

if __name__ == '__main__':
    atomic_swap(broadcast_transactions, alice_redeems)


#成功赎回的
#alice发起
#5aee88324c2c0f08bc9543572917a752c976d7fb30b09ceb5d9dd0dc52db85e9
#bob发起
#f0807d2f40b0914cdae88caa06a1382d82f3a049cb147164083c38854881db7a
#alice赎回
#7089723a5db8334c1a67560cb5c83f42d73dd77c20aae9118e759c04c566a9b0
#bob赎回
#23d7487359e309c25d691664d7af99a162ba0975097dc7d831c78df9f6bd700b
#超时的
#alice发起
#fa9dd2adaf54c7bf34a557fed6e9057301eb0662cadf173020270276b9a1ab48
#bob发起
#25c5f04f8277ac5b1ec6fa34d2d5d5c37ec48d184073e3ed9509e53d6620a712
#bob超时
#5297a58b5c6cac0a4f83d5c9d4c7c0e3b2b3034434456841ee2449c228bbe2b5
#alice超时
#a1e3102f40f74d306f84633bdcb62bb306ffce8b22a1d974bf85e0aa6603f7cd