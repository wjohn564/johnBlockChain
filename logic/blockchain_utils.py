from web3 import Web3
import json

# Connect to Ganache
ganache_url = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))

with open('truffle/build/contracts/CourseRegistration.json') as f:
    contract_data = json.load(f)

contract_address = "0xa26feE6848b273E7ea3e7793F1b14De476Ce75bD"
contract_abi = contract_data['abi']
contract = web3.eth.contract(address=contract_address, abi=contract_abi)


def create_course_blockchain(course_id, name, seats):
    tx_hash = contract.functions.createCourse(course_id, name, seats).transact({'from': web3.eth.accounts[0]})
    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    return {"status": "Course created on blockchain!", "transactionHash": receipt.transactionHash.hex()}


def enroll_in_course_blockchain(course_id, student_address):
    tx_hash = contract.functions.enrollInCourse(course_id).transact({'from': student_address})
    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    return {"status": "Enrolled successfully on blockchain!", "transactionHash": receipt.transactionHash.hex()}


def get_course_details_blockchain(course_id):
    course = contract.functions.getCourseDetails(course_id).call()
    return {"name": course[0], "availableSeats": course[1]}
