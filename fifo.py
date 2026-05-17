from collections import deque
from data import Allocation, Lot, Consumed

class FIFO:
    def __init__(self) -> None:
        self._storage: deque[Allocation] = deque()

    def buy(self, shares: float, price: float, time: str, rate: float) -> None:
        purchase = Allocation(action="BUY", shares=shares, price=price, time=time, rate=rate)
        self._storage.append(purchase)

    def sell(self, shares: float, price: float, time: str, rate: float) -> Lot:
        sale = Allocation(action="SELL", shares=shares, price=price, time=time, rate=rate)
        lot = Lot(purchases=[], sale=sale)
        shares_to_allocate = shares

        while shares_to_allocate > 0:
            if not self._storage:
                break

            oldest_purchase = self._storage[0]
            taken = min(oldest_purchase.shares, shares_to_allocate)
            
            lot.purchases.append(Consumed(shares=taken, price=oldest_purchase.price, time=oldest_purchase.time, rate=oldest_purchase.rate))
            shares_to_allocate -= taken
        
            if taken == oldest_purchase.shares:
                self._storage.popleft()
            else:
                oldest_purchase.shares -= taken

        return lot
