class CoinAcceptor :
    __amount: int 
    __value: float

    def __init__(self):
        self.__amount = 0
        self.__value = 0.0

    def insertCoin(self) -> None:
        self.__amount += 1
        return None
    
    def getAmount(self) -> int:
        return self.__amount
    
    
    def returnCoins(self) -> int:
        val = self.__amount
        self.__amount = 0
        return val
    
