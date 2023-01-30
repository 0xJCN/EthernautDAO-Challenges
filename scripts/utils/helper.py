from ape import chain
from ape.pytest.contextmanagers import RevertsContextManager as reverts
import subprocess

w3 = chain.provider.web3


def fork(block_number):
    chain.provider.reset_fork(block_number)


def get_storage(account, slot):
    return chain.provider.get_storage_at(account, slot).hex()


def mine_block(num_blocks):
    chain.mine(num_blocks)


def get_balance(account):
    return chain.provider.get_balance(account)


def get_code(account):
    return chain.provider.get_code(w3.toChecksumAddress(account)).hex()


def get_timestamp():
    return chain.pending_timestamp


def get_block():
    return chain.blocks[-1].number


def prep_blueprint_deployment(contract_name):
    bytecode = subprocess.run(
        ["vyper", "-f", "blueprint_bytecode", "./contracts/" + contract_name + ".vy"],
        text=True,
        capture_output=True,
    ).stdout[:-1]
    blueprint_address = send_tx("", bytecode).contractAddress
    deployment_code = (
        chain.project_manager.get_contract(contract_name)
        .contract_type.get_deployment_bytecode()
        .hex()
    )
    return blueprint_address, deployment_code


def send_tx(recipient, calldata):
    w3.eth.default_account = w3.eth.accounts[0]
    tx = w3.eth.send_transaction(dict(to=recipient, data=calldata))
    return w3.eth.wait_for_transaction_receipt(tx)
