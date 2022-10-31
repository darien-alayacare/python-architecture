from adapters.abstract_repository import AbstractRepository
from domains.batch import Batch

from sqlalchemy import insert, null

from domains.oder_line import OrderLine


class SqlAlchemyRepository(AbstractRepository):

    def __init__(self, session):
        self.session = session

    def add(self, batch: Batch):
        self.session.add(batch)
    
    def get(self, reference) -> Batch:
        return self.session.query(Batch).filter_by(reference=reference).one()
    
    def list(self):
        return self.session.query(Batch).all()

class FakeRepository(AbstractRepository):

    def __init__(self, batches):
        self.batches = batches

    def add(self, batch: Batch):
            self.batches.add(batch)

    def get(self, reference):
        return next(b for b in self.batches if b.reference == reference)

    def list(self):
        return list(self.batches)

    @staticmethod
    def for_batch(ref, sku, qty, eta=None):
        return FakeRepository(set([Batch(ref, sku, qty, eta)]))
