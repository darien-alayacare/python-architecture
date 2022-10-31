from __future__ import annotations
from datetime import date
from typing import Optional
from adapters.abstract_repository import AbstractRepository
from domains.batch import Batch

from domains.model import allocate as _allocate
from domains.oder_line import OrderLine
from service_layer.unit_of_work import AbstractUnitOfWork



class InvalidSku(Exception):
    pass


def is_valid_sku(sku, batches):
    return sku in {b.sku for b in batches}


def allocate(ref, sku, qty, 
    uow: AbstractUnitOfWork) -> str:
    line = OrderLine(orderid=ref, sku=sku, qty=qty)

    with uow:
        batches = uow.batches.list()
        if not is_valid_sku(line.sku, batches):
            raise InvalidSku(f'Invalid sku{line.sku}')
        batchref = _allocate(line, batches)
        uow.commit()

    return batchref

def add_batch(
    ref: str, sku: str, qty: int, eta: Optional[date],
    uow: AbstractUnitOfWork):
    with uow:
        uow.batches.add(Batch(ref, sku, qty, eta))
        uow.commit()