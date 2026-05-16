from collections import deque
from dataclasses import dataclass

@dataclass
class Allocation:
    shares: float
    price: float

class FIFO:
    def __init__(self) -> None:
        self._storage: deque[Allocation] = deque()

    def buy(self, shares: float, price: float) -> None:
        self._storage.append(Allocation(shares, price))

    def sell(self, shares: float) -> float:
        shares_to_allocate = shares
        current_sales_cost = 0

        while shares_to_allocate > 0:
            if not self._storage:
                break

            oldest_purchase = self._storage[0]
            if oldest_purchase.shares <= shares_to_allocate:
                taken_shares = oldest_purchase.shares
                current_sales_cost += taken_shares * oldest_purchase.price
                shares_to_allocate -= taken_shares
                self._storage.popleft()
            else:
                current_sales_cost += shares_to_allocate * oldest_purchase.price
                oldest_purchase.shares -= shares_to_allocate
                shares_to_allocate = 0

        return current_sales_cost
