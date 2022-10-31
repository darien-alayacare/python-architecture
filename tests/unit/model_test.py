from datetime import date, timedelta

import pytest
from domains.batch import Batch

from domains.oder_line import OrderLine 
from domains.model import OutOfStock, allocate


today = date.today()
tomorrow = today + timedelta(days=1)
later = tomorrow + timedelta(days=10)

def create_batch_line(sku, batch_qty, line_qty):
    new_batch = Batch("batch-001", sku, batch_qty, date.today())
    line = OrderLine('order-ref', sku, line_qty)
    return new_batch,line

def test_allocating_to_a_batch_reduces_the_available_quantity():
    new_batch, line = create_batch_line("SMALL-TABLE", 20, 2)
    prev_available_quantity = new_batch.available_quantity
    new_batch.allocate(line)
    assert new_batch.available_quantity == prev_available_quantity - line.qty

def test_cannot_allocate_if_available_smaller_than_required():
    small_batch, line = create_batch_line("SMALL-TABLE", 1, 3)
    assert small_batch.can_allocate(line) is False

def test_can_allocate_if_available_greater_than_required():
    big_batch, line = create_batch_line("SMALL-TABLE", 3, 2)
    assert big_batch.can_allocate(line) is True

def test_can_allocate_if_available_equal_to_required():
   new_batch, line = create_batch_line("SMALL-TABLE", 2, 2)
   assert new_batch.can_allocate(line) is True 

def test_can_only_deallocate_allocated_lines():
    batch, line = create_batch_line("DECORATIVE-TABLE", 20, 2)
    batch.deallocate(line)
    assert batch.available_quantity == 20

def test_allocation_is_idempotent():
    batch, line = create_batch_line("ANGULAR-DESK", 20, 2)
    batch.allocate(line)
    batch.allocate(line)
    assert batch.available_quantity == 18

def test_prefers_earlier_batches():
    earliest = Batch("speedy-batch", "MINIMALIST-SPOON", 100, eta=today)
    medium = Batch("normal-batch", "MINIMALIST-SPOON", 100, eta=tomorrow)
    latest = Batch("slow-batch", "MINIMALIST-SPOON", 100, eta=later)
    line = OrderLine("order1", "MINIMALIST-SPOON", 10)

    allocate(line, [medium, earliest, latest])

    assert earliest.available_quantity == 90
    assert medium.available_quantity == 100
    assert latest.available_quantity == 100

def test_returns_allocated_batch_ref():
    in_stock_batch = Batch("in-stock-batch-ref", "HIGHBROW-POSTER", 100, eta=None)
    shipment_batch = Batch("shipment-batch-ref", "HIGHBROW-POSTER", 100, eta=tomorrow)
    line = OrderLine("oref", "HIGHBROW-POSTER", 10)
    allocation = allocate(line, [in_stock_batch, shipment_batch])
    assert allocation == in_stock_batch.reference


def test_raises_out_of_stock_exception_if_cannot_allocate():
    batch = Batch('batch1', 'SMALL-FORK', 10, eta=today)
    allocate(OrderLine('order1', 'SMALL-FORK', 10), [batch])

    with pytest.raises(OutOfStock, match='SMALL-FORK'):
        allocate(OrderLine('order2', 'SMALL-FORK', 1), [batch])

        