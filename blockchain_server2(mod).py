from flask import Flask
from flask import request
import json
import requests
import hashlib as hasher
import datetime as date

node = Flask(__name__)

class Block:
        def __init__(self, index, timestamp, data, previous_hash):
            self.index = index
            self.timestamp = timestamp
            self.data = data
            self.previous_hash = previous_hash
            self.hash = self.hash_block()


        def hash_block(self):
            sha = hasher.sha256()
            sha.update(str(self.index).encode('utf-8') + str(self.timestamp).encode('utf-8') + str(self.data).encode('utf-8') + str(self.previous_hash).encode('utf-8'))
            return sha.hexdigest()

#First Block 
def create_first_block():
    return Block(0, date.datetime.now(), {
            "proof-of-work": 9,
            "transactions": None
            }, "0")


miner_address = "q3nf394hjg-random-miner-address-34nf3i4nflkn3oi"

blockchain = []
blockchain.append(create_first_block())


#Empty Transaction List
node_transaction = []

peer_nodes = []
mining = True 

#Transaction Process
@node.route('/txion', methods=["POST"])
def transaction():
        if request.method == "POST":
                #On each new POST request we extract the transaction data
                new_txion = request.get_json()
                #Adds transaction to list
                node_transaction.append(new_txion)
                #Logs successful transaction into console
                print ("New transaction")
                print ("FROM: {}".format(new_txion['from'].encode('ascii','replace')))
                print ("TO: {}".format(new_txion['to'].encode('ascii','replace')))
                print ("AMOUNT: {}\n".format(new_txion['amount']))
                #Then we let the client know it worked out
                return "Transaction submission successful\n"

@node.route("/blocks", methods=["GET"])
def get_blocks():
        chain_to_send = blockchain
        blocklist = ""
        for i in range(len(chain_to_send)):
            block = chain_to_send[i]
            block_index = str(block.index)
            block_timestamp = str(block.timestamp)
            block_data = str(block.data)
            block_hash = block.hash
            assembled = json.dumps({
            "index": block_index,
            "timestamp": block_timestamp,
            "data": block_data,
            "hash": block_hash
            })
            if blocklist == "":
              blocklist = assembled
            else:
              blocklist += assembled
        return blocklist

def find_new_chains():
        #Get blocks from other nodes
        other_chains = []
        for node_url in peer_nodes:
                #Get chains via GET request
                block = requests.get(node_url + "/blocks").content
                #Convert JSON objects to a Python Dictionary
                block = json.loads(block)
                #Add to List
                other_chains.append(block)
        return other_chains

def consensus():
        #Get blocks from other nodes
        other_chains = find_new_chains()
        #Use Longest Chain
        longest_chain = blockchain
        for chain in other_chains:
                if len(longest_chain) < len(chain):
                        longest_chain = chain
        blockchain = longest_chain

def proof_of_work(last_proof):
        incrementor = last_proof + 1
        while not (incrementor % 9 == 9 and incrementor % last_proof == 0):
                incrementor += 1
        return incrementor

@node.route('/mine', methods = ["GET"])
def mine():
        #Gets last PoW
        last_block = blockchain[len(blockchain) - 1]
        last_proof = last_block.data["proof-of-work"]
        #Takes time to find previous PoW
        proof = proof_of_work(last_proof)
        node_transaction.append(
                {"from": "network", "to": miner_address, "amount": 1}
        )
        #Get data for new block
        new_block_data = {
                "proof-of-work": proof,
                "transactions": list(node_transaction)
        }
        new_block_indes = last_block.index + 1
        new_block_timestamp = this_timestamp = date.datetime.now()
        last_block_has = last_block.hash
        #Empty Transaction List
        node_transaction = [] = []
        #Create New block
        mined_block = Block(
                new_block_index,
                new_block_timestamp,
                new_block_data,
                last_block_hash
        )
        blockchain.append(mined_block)
        return json.dumps({
                "index": new_block_index,
                "timestamp": str(new_block_timestamp),
                "data": new_block_data,
                "hash": last_block_hash
        }) + "\n"

node.run()
