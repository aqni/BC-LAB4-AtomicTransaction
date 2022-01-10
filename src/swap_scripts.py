from bitcoin.core.script import *


######################################################################
# This function will be used by Alice and Bob to send their respective
# coins to a utxo that is redeemable either of two cases:
# 1) Recipient provides x such that hash(x) = hash of secret
#    and recipient signs the transaction.
# 2) Sender and recipient both sign transaction
#
# TODO: Fill this in to create a script that is redeemable by both
#       of the above conditions.
#
# See this page for opcode: https://en.bitcoin.it/wiki/Script
#
#

# This is the ScriptPubKey for the swap transaction


def coinExchangeScript(public_key_sender, public_key_recipient, hash_of_secret):
    return [
        OP_DEPTH,  # 使用栈深度(即ScriptSig长度作为分支判断条件)
        2, OP_EQUAL,  # 一种ScriptSig长度为2，另一种长度为3
        OP_IF,
        OP_HASH160,
        hash_of_secret,
        OP_EQUALVERIFY,  # 检验Hash(x)的秘密x
        public_key_recipient,
        OP_CHECKSIG,  # 检验接收者签名
        OP_ELSE,
        OP_2,
        public_key_sender,
        public_key_recipient,
        OP_2,
        OP_CHECKMULTISIG,  # 对接收者签名和发送者签名进行多校验
        OP_ENDIF,
    ]

# This is the ScriptSig that the receiver will use to redeem coins


def coinExchangeScriptSig1(sig_recipient, secret):
    return [
        sig_recipient,
        secret,
    ]

# This is the ScriptSig for sending coins back to the sender if unredeemed


def coinExchangeScriptSig2(sig_sender, sig_recipient):
    return [
        OP_0,
        sig_sender,
        sig_recipient,
    ]
#
#
######################################################################
