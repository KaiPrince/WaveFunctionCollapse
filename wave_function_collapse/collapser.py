from abc import ABCMeta, abstractmethod


class Collapser(metaclass=ABCMeta):
    @abstractmethod
    def compute_wave_collapse_queue(self):
        pass

    @abstractmethod
    def get_entropy(self, cell):
        pass

    @abstractmethod
    def is_collapsed(self, cell):
        pass

    @abstractmethod
    def compute_possible_states(self, cell):
        pass

    @abstractmethod
    def set_cell_state(self, cell, state):
        pass

    @abstractmethod
    def cell_is_invalid(self, cell):
        pass

    @abstractmethod
    def revert(self):
        pass

    @abstractmethod
    def get_coefficient_cells(self, cell):
        pass
