from typing import (
    Dict,
    List,
    Tuple
)

import numpy as np

import warnings
warnings.filterwarnings('ignore')


class Queue():  # criação da classe fila com o uso da classe lista, já definida do python
    def __init__(self):
        self.queue = []

    def is_empty(self):
        return self.queue == []

    def begin(self):
        if self.is_empty():
            raise ValueError('Begin: queue has no elements')  # se a fila estiver vazia vai dar erro
        else:
            return self.queue[0]

    def length(self):
        return len(self.queue)

    def put(self, element):
        self.queue += [element]
        return self

    def take(self):
        if self.is_empty():
            raise ValueError('Take: queue has no elements')  # se a fila estiver vazia vai dar erro
        else:
            self.queue.pop(0)

    def __repr__(self):
        f = '<'
        for e in self.queue:
            f += e.__repr__() + ','
        f += '<'
        return f


class Queue2():  # criação da classe fila, mas agora com um array do numpy
    def __init__(self):
        self.queue = np.empty((0, 3), dtype=int)  # inicia a fila com um array vazio com forma (0,3), isto é,
        # inicio esta classe para guardar tuplos de 3 elementos, todos do tipo int

    def is_empty(self):
        return self.queue.shape[0] == 0  # se o shape da fila for (0, 3), ou seja, se não houver elementos dá True

    def begin(self):
        if self.is_empty():
            raise ValueError('Begin: queue has no elements')
        else:
            return tuple(self.queue[0])

    def length(self):
        return self.queue.shape[0]

    def put(self, element: tuple[int, int, int]):  # adicionar um elemento, que é um tuplo de 3 números inteiros
        self.queue = np.vstack((self.queue, np.array(element, dtype=int)))  # primeiro converte o tuplo em um array,
        # e depois cria uma matriz com os arrays verticalmente
        return self

    def take(self):
        if self.is_empty():
            raise ValueError('Take: queue has no elements')
        else:
            first_element = tuple(self.queue[0])
            self.queue = np.delete(self.queue, 0, axis=0)
            return first_element

    def __repr__(self):  # ao dar print de um objeto desta clase,
        # a função tolist converte a matriz que é formada pelos tuplos numa lista
        return str(self.queue.tolist())


class Target:  # classe target, onde os resultados são guardados num objeto da classe fila, feita com a lista do python
    def __init__(self) -> None:
        self.target = Queue()

    def persist_delivery(self, payload: Tuple):
        try:
            self.target.put(payload)
            return True
        except:
            return False


class Target2:  # classe target, onde os resultados são guardados num objeto da classe fila, feita com um array do numpy
    def __init__(self):
        self.target = Queue2()

    def persist_delivery(self, payload: Tuple):
        try:
            self.target.put(payload)  # guarda o payload na fila
            return True
        except:
            return False
