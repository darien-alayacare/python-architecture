
from datetime import date

from sqlalchemy import false

from domains.oder_line import OrderLine


class Batch(object):

    lambda_allocate = lambda available, quantity: available - quantity
    lambda_dont_allocate = lambda available, quantity: available

    allocation_strategy = dict([(True, lambda_allocate), (False, lambda_dont_allocate)])

    def __init__(self, reference, sku, quantity = 0, eta = date.today):
        self.reference = reference
        self.sku = sku
        self.eta = eta
        self.purchased_quantity = quantity
        self._allocations = set()

    def allocate(self, order_line:OrderLine):
        if self.can_allocate(order_line):
            self._allocations.add(order_line)
            print("could allocate")
           
    def deallocate(self, order_line:OrderLine):
        if order_line in self._allocations:
            self._allocations.remove(order_line)

    @property
    def available_quantity(self) -> int:
        return self.purchased_quantity - self.allocated_quantity
    
    @property
    def allocated_quantity(self) -> int:
        return sum(line.qty for line in self._allocations)

    def can_allocate(self, order_line:OrderLine):
        return self.sku == order_line.sku and self.available_quantity >= order_line.qty

    def __eq__(self, other):
        if not isinstance(other, Batch):
            return False
        return other.reference == self.reference

    def __hash__(self):
        return hash(self.reference)

    def __gt__(self, other):
        if self.eta is None:
            return False
        elif other.eta is None:
            return True
        
        return self.eta > other.eta

        