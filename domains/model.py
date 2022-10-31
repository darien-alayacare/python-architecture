from typing import List
from domains.batch import Batch
from domains.oder_line import OrderLine


class OutOfStock(Exception):
    pass

def allocate(line: OrderLine, batches:List[Batch]):
    try:
        batch = next(
            b for b in sorted(batches) if b.can_allocate(line)
        )
    except StopIteration:
        raise OutOfStock(f'Out of stock for sku {line.sku}') 
        
    batch.allocate(line)
    return batch.reference

