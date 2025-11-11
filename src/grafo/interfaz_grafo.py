from abc import ABC, abstractmethod

class Grafo(ABC):

    @abstractmethod
    def add_edge(self, u, v):
        pass

    @abstractmethod
    def add_vertex(self,v):
        pass

    @abstractmethod
    def delete_edge(self, u, v):
        pass

    @abstractmethod
    def exists_edge(self, u, v):
        pass

    @abstractmethod
    def delete_vertex(self, v):
        pass

    @abstractmethod
    def order(self):
        pass

    @abstractmethod
    def get_adjacency_list(self, v):
        pass
