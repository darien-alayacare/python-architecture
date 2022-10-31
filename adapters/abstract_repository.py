import abc

from domains.batch import Batch

class AbstractRepository(abc.ABC):

    @abc.abstractmethod  
    def add(self, batch: Batch):
        raise NotImplementedError 

    @abc.abstractmethod
    def get(self, reference) -> Batch:
        raise NotImplementedError 

    @abc.abstractmethod
    def list(self):
        raise NotImplementedError