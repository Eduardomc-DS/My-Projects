import  source
import target 
import sort
import time
import matplotlib.pyplot as plt


from source import Source
from target import Target
from target import Target2
from target import Queue
from target import Queue2

import pandas as pd
from typing import (Dict, List, Tuple)

import warnings
warnings.filterwarnings('ignore')

class Sort():
    def __init__(self, list, ascending=True) -> None:
        self.ascending = ascending # irá definir se a ordenação é crescente ou decrescente
        self.list = list

    @staticmethod
    def bubblesort(list):
        n = len(list)
        for i in range(0, n):  # itera sobre todos os elementos da lista
            for e in range(i+1, n):  # itera sobre os elementos após o atual
                if list[i] > list[e]:
                    list[i], list[e] = list[e], list[i] #se o elemento atual for maior que o proximo, troca um com o outro
        return list

    @staticmethod
    def selectionsort(list):
        n = len(list)
        for i in range(0, n):  # itera sobre todos os elementos da lista
            min = i  # define o elemento atual como o minimo
            for e in range(i + 1, n):  # itera sobre os elementos após o atual
                if list[e] < list[min]:
                    min = e  # se o atual for menor que o minimo atualiza o minimo se necessário
            if min != i:
                list[i], list[min] = list[min], list[i]  # se o indice do minimo mudou, troca os elementos
        return list

    def sort(self, type_of_sort):  # ordena a lista dada na criação do objeto atraves do algoritmo que escolher
        list = self.list
        if type_of_sort == "bubblesort":
            sorted_list = self.bubblesort(list)
            if not self.ascending:
                sorted_list.reverse()
            return sorted_list
        if type_of_sort == "selectionsort":
            sorted_list = self.selectionsort(list)
            if not self.ascending:
                sorted_list.reverse()
            return sorted_list



class Main:  #classe main com o target que tem a fila feita com a lista
    def __init__(self, batch_size=int):
        self.batch_size = batch_size
        self.target = Target()
        self.source = Source()
        self.batch_numbers = [] # lista com os batch numbers processados
        self.process_time = [] # lista com o tempo que demora a calcular o minimo e o maximo de cada batch
        self.mean_process_time = 0  # media do tempo que demora a calcular o minimo e o maximo de cada batch
        self.max = 0 # maximo encontrado
        self.min = 0 # minimo encontrado

    def update_last_searched_id(self, new_id):
        self.source.update_last_searched_id(new_id=new_id)

    def update_batch_nr(self):
        self.source.update_batch_nr()

    def persist_delivery(self, payload: Tuple):
        return self.target.persist_delivery(payload=payload) # guarda o payload na fila da target

    @staticmethod
    def fetch_value(batch: List, highest: bool = True):  #metodo estatico para calcular o maximo ou minimo de um batch
        value = None
        for number in batch:
            value = number if value is None else value
            if highest is True and number > value:
                value = number
            if highest is False and number < value:
                value = number
        return value

    def process(self, batch: List) -> Tuple:
        star_timep = time.time()  # comeca a contar o tempo que demora a processar
        lowest_value = self.fetch_value(batch=batch, highest=False) # calcula o minimo atraves do metodo estatico
        highest_value = self.fetch_value(batch=batch, highest=True)  # calcula o maximo atraves do metodo estatico
        payload = (self.source.batch_nr, lowest_value, highest_value)  #cria um tuplo com o batch number, minimo e maximo
        end_timep = time.time()  # para de cronometrar o tempo que demora a processar
        elapsed_timep = end_timep - star_timep # calcula o tempo que demorou
        self.process_time.append(elapsed_timep)  # adiciona o tempo de processamento na lista
        return payload

    def run(self,type_of_sort) -> None:  # é dado o type_of_sort para ordenar a lista com o algoritmo que escolher
        continue_running_process = True
        while continue_running_process:
            batch = self.source.load_state(batch_size=self.batch_size) #  carrega um batch
            if batch is None:
                return
            delivery = self.process(batch=batch[1])  # processa o batch
            result = self.persist_delivery(payload=delivery)

            if result is True:
                self.update_batch_nr()
                self.update_last_searched_id(new_id=batch[0])
                del batch

                batch_numbers = [tuplo[0] for tuplo in self.target.target.queue]  # cria a lista com os batch numbers
                lowest_numbers = [tuplo[1] for tuplo in self.target.target.queue]  # cria a lista com os minimos
                highest_numbers = [tuplo[2] for tuplo in self.target.target.queue] # cria a lista com os maximos
                self.batch_numbers = batch_numbers
                all_numbers = lowest_numbers + highest_numbers # cria uma lista com os maximos e minimos
                all_numbers2 = Sort(list=all_numbers) # cria um objeto da classe Sort para ordenar a lista
                print('Lista com todos os número ordenado:', all_numbers2.sort(type_of_sort)) # da print da lista ordena
                # com o type_of_sort dado na função run
                self.min = all_numbers2.sort(type_of_sort)[0]  # o minimo é o primeiro elemento da lista ordenada
                self.max = all_numbers2.sort(type_of_sort)[-1]  # o maximo é o ultimo elemento da lista ordenada
                print('Minimo:', self.min)
                print('Maximo:', self.max)

                self.mean_process_time = sum(self.process_time) / len(self.process_time)  # calcula  qmedia do tempo que
                # demora a calcular o minimo e o maximo de cada batch
                print(f'Tempo médio que demora a executar cada batch: {self.mean_process_time} segundos.')

            else:
                raise ValueError(
                    f'Batch: unsuccessfully delivered for id: {self.source.last_read_id}')



class Main2:  #classe main com o target que tem a fila feita com array do numpy
    def __init__(self, batch_size=int):
        self.batch_size = batch_size
        self.target = Target2()
        self.source = Source()
        self.batch_numbers = [] # lista com os batch numbers processados
        self.process_time = []  # lista com o tempo que demora a calcular o minimo e o maximo de cada batch
        self.mean_process_time = 0  # media do tempo que demora a calcular o minimo e o maximo de cada batch
        self.max = 0  # maximo encontrado
        self.min = 0  # minimo encontrado

    def update_last_searched_id(self, new_id):
        self.source.update_last_searched_id(new_id=new_id)

    def update_batch_nr(self):
        self.source.update_batch_nr()

    def persist_delivery(self, payload: Tuple):
        return self.target.persist_delivery(payload=payload)

    @staticmethod  #metodo estatico para calcular o maximo ou minimo de um batch
    def fetch_value(batch: List, highest: bool = True):
        value = None
        for number in batch:
            value = number if value is None else value
            if highest is True and number > value:
                value = number
            if highest is False and number < value:
                value = number
        return value

    def process(self, batch: List) -> Tuple:
        star_timep = time.time()  # comeca a contar o tempo que demora a processar
        lowest_value = self.fetch_value(batch=batch, highest=False)  # calcula o minimo atraves do metodo estatico
        highest_value = self.fetch_value(batch=batch, highest=True)  # calcula o maximo atraves do metodo estatico
        payload = (self.source.batch_nr, lowest_value, highest_value)  # cria um tuplo com o batch number, minimo e maximo
        end_timep = time.time()  # para de cronometrar o tempo que demora a processar
        elapsed_timep = end_timep - star_timep  # calcula o tempo que demorou
        self.process_time.append(elapsed_timep)  # adiciona o tempo de processamento na lista
        return payload

    def run(self, type_of_sort) -> None:  # é dado o type_of_sort para ordenar a lista com o algoritmo que escolher
        continue_running_process = True
        while continue_running_process:
            batch = self.source.load_state(batch_size=self.batch_size)  # carrega um batch
            if batch is None:
                return
            delivery = self.process(batch=batch[1])  # processa o batch
            result = self.persist_delivery(payload=delivery)

            if result is True:
                self.update_batch_nr()
                self.update_last_searched_id(new_id=batch[0])
                del batch

                batch_numbers = [tuplo[0] for tuplo in self.target.target.queue]  # cria a lista com os batch numbers
                lowest_numbers = [tuplo[1] for tuplo in self.target.target.queue]  # cria a lista com os minimos
                highest_numbers = [tuplo[2] for tuplo in self.target.target.queue]  # cria a lista com os maximos
                self.batch_numbers = batch_numbers
                all_numbers = lowest_numbers + highest_numbers  # cria uma lista com os maximos e minimos
                all_numbers2 = Sort(list=all_numbers)  # cria um objeto da classe Sort para ordenar a lista
                print(f'Lista com todos os número ordenado: {all_numbers2.sort(type_of_sort)}')  # da print da lista ordena
                # com o type_of_sort dado na função run
                self.min = all_numbers2.sort(type_of_sort)[0]  # o minimo é o primeiro elemento da lista ordenada
                self.max = all_numbers2.sort(type_of_sort)[-1]  # o maximo é o ultimo elemento da lista ordenada
                print('Minimo:', self.min)
                print('Maximo:', self.max)

                self.mean_process_time = sum(self.process_time) / len(self.process_time)  # calcula  qmedia do tempo que
                # demora a calcular o minimo e o maximo de cada batch
                print(f'Tempo médio que demora a executar cada batch: {self.mean_process_time} segundos.')

            else:
                raise ValueError(
                    f'Batch: unsuccessfully delivered for id: {self.source.last_read_id}')




if True:
    process = Main(batch_size=100)
    process.run("selectionsort")
    #process2 = Main2(batch_size=100000)
    #process2.run("selectionsort")

# Grafico do tempo de execução do algoritmo em função do algoritmo de ordenação selectionsort
    #process2 = Main2(batch_size=10000)
    #process2.run("selectionsort")

    #process3 = Main2(batch_size=50000)
    #process3.run("selectionsort")

    #process4 = Main2(batch_size=100000)
    #process4.run("selectionsort")

    #process5 = Main2(batch_size=500000)
    #process5.run("selectionsort")

    #process6 = Main2(batch_size=1000000)
    #process6.run("selectionsort")

    #lista_batch = [process2.batch_size, process3.batch_size, process4.batch_size,
     #              process5.batch_size, process6.batch_size]
    #lista_time = [process2.mean_process_time, process3.mean_process_time,
     #             process4.mean_process_time, process5.mean_process_time, process6.mean_process_time]


    #plt.plot(lista_batch, lista_time)
    #plt.xlabel('Tamanho do Batch')
    #plt.ylabel('Tempo de Execução (s)')
    #plt.title('Tempo de Execução para Calcular Mínimo e Máximo com o selectionsort')
    #plt.show()



# Grafico do tempo de execução do algoritmo em função do algoritmo de ordenação bubblesort
    #process2 = Main2(batch_size=10000)
    #process2.run("bubblesort")

    #process3 = Main2(batch_size=50000)
    #process3.run("bubblesort")

    #process4 = Main2(batch_size=100000)
    #process4.run("bubblesort")

    #process5 = Main2(batch_size=500000)
    #process5.run("bubblesort")

    #process6 = Main2(batch_size=1000000)
    #process6.run("bubblesort")

    #lista_batch = [process2.batch_size, process3.batch_size, process4.batch_size,
     #              process5.batch_size, process6.batch_size]
    #lista_time = [process2.mean_process_time, process3.mean_process_time,
     #             process4.mean_process_time, process5.mean_process_time, process6.mean_process_time]


    #plt.plot(lista_batch, lista_time)
    #plt.xlabel('Tamanho do Batch')
    #plt.ylabel('Tempo de Execução (s)')
    #plt.title('Tempo de Execução para Calcular Mínimo e Máximo com o bubblesort')
    #plt.show()


#Grafico de barras do tempo de execução do algoritmo em função do algoritmo de ordenação
    #process = Main2(batch_size=10000)
    #process.run("selectionsort")

    #process2 = Main2(batch_size=10000)
    #process2.run("bubblesort")



    #plt.bar(["Selectionsort","Bubblesort"], [process.mean_process_time, process2.mean_process_time])
    #plt.xlabel('Tamanho do Batch')
    #plt.ylabel('Tempo de Execução (s)')
    #plt.title('Tempo de Execução em função do algoritmo de ordenação (batch_size = 10000)')
    #plt.show()
