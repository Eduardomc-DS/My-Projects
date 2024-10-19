class Especie:
    def __init__(self, nome, folhagem, produzfruto, tipo, raioocupado, idade_media):
        if isinstance(nome, str):
            self.__n = nome
        else:
            raise ValueError("O nome da espécie tem de ser uma cadeia de caracteres.")
        if folhagem.lower() in ["persistente", "caduca", "semicaduca"]:
            self.__f = folhagem
        else:
            raise ValueError("O tipo de folhagem não é válida.")
        if isinstance (produzfruto, bool):
            self.__pf = produzfruto
        else:
            raise ValueError("O valor tem de ser um valor boolenao.")
        if tipo.lower() in ["arvore", "árvore", "arbusto"]:
            self.__t = tipo
        else:
            raise ValueError("O tipo não é permitido.")
        if isinstance(raioocupado, float) and raioocupado > 0:
            self.__raio = raioocupado
        else:
            raise ValueError("O raio tem de ser um valor decimal positivo.")
        if isinstance(idade_media, int) and idade_media > 0:
            self.__i = idade_media
        else:
            raise ValueError("A idade tem de ser um valor inteiro positivo.")
        
    @property
    def nome(self):
        return self.__n
    @property
    def folhagem(self):
        return self.__f
    @property
    def produz_fruto(self):
        return self.__pf
    @property
    def tipo(self):
        return self.__t
    @property
    def idade_media(self):
        return self.__i
    
    def raio_ocupado(self):
        return self.__raio
         
    def area_ocupada_especie(self):
        return (self.__raio**2)*math.pi
             
    def __str__(self):
       return str(self.__n) + ", " + str(self.__f) + ", Produz frutos:" + str(self.__pf) + " Tipo:" + str(self.__t) + ", Ocupado um círculo de raio: " + str(self.__raio) + " metros," + str(self.__i) + " anos"
    
    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        else:
            return self.__n == other.__n


class Planta:
    def __init__(self, especie, GPS, anoplantacao):
        if isinstance(especie, Especie):
            self.__e = especie
        else:
            raise ValueError("A espécie introduzida tem de ser da classe Especie.")
        if isinstance(GPS, tuple) and isinstance(GPS[0], float) and isinstance(GPS[1], float):
            self.loc = GPS
        else:
            raise ValueError("A localizacao tem de ser um par de valores decimais.")
        if isinstance(anoplantacao, int) and anoplantacao > 0:
            self.__ap = anoplantacao
        else:
            raise ValueError("O ano de plantação tem de ser um valor inteiro positivo.")
        
    @property
    def especie(self):
        return self.__e
    @property
    def localizacao(self):
        return self.loc
    @property
    def ano_plantacao(self):
        return self.__ap
    
    def area_ocupada_planta(self):
        return self.__e.area_ocupada_especie()
    
    def idade(self, ano):
        return ano - self.__ap
    
    def pertence_area(self, localizacao):
        return self.__e.raio_ocupado() >= ((localizacao[0]-self.loc[0])**2+(localizacao[1]-self.loc[1])**2)**(1/2)
    
    def __str__(self):
        return "Especie: " + str(self.especie) + ", localização: " + str(self.loc) + ", ano de plantação: " + str(self.__ap)
    
    
class Parque:
    def __init__(self, nome, areadeplantacao):
        if isinstance(nome, str):
            self.__np = nome
        else:
            raise ValueError("O nome do parque tem de ser uma cadeia de caracteres.")
        if isinstance(areadeplantacao, float) and areadeplantacao > 0:
            self.__arp = areadeplantacao
        else:
            raise ValueError("A area de plantação tem de ser um valor decimal positivo.")
        self.__plantas = []
    
    @property
    def nome_parque(self):
        return self.__np
    @property
    def area_de_plantacao(self):
        return self.__arp
    
    def add(self, planta):
        for i in self.__plantas:
            distancia_plantas = ((planta.localizacao[0] - i.localizacao[0])**2 + (planta.localizacao[1] - i.localizacao[1])**2)**(1/2)
            if i.localizacao == planta.localizacao or planta.area_ocupada_planta() > self.area_disponivel() or distancia_plantas < planta.especie.raio_ocupado() + i.especie.raio_ocupado():
                    print("Não é possível plantar nesta localização.")
                    return
        self.__plantas.append(planta)
            
    def lista(self):
        return self.__plantas
                        
    def del_planta(self, loc):
        for i in self.__plantas:
            if i.loc == loc:
                self.__plantas.remove(i)
                
    def planta_na_loc(self, loc):
        for i in self.__plantas:
            if i.loc == loc:
                return True
        return False 
            
    def area_total_ocupada(self):
        area = 0
        for i in self.__plantas:
            area += i.area_ocupada_planta()
        return area
    
    def area_disponivel(self):
        return self.__arp - self.area_total_ocupada()
    
    def ha_espaco(self, planta):
        return planta.area_ocupada_planta() <= self.area_disponivel()
    
    def idade_media_plantas(self, ano):
        idade = 0
        for i in self.__plantas:
            idade += i.idade(ano)
        return idade/len(self.__plantas)
    
    def numero_especies(self):
        especies = []
        for i in self.__plantas:
            if i.especie not in especies:
                especies.append(i.especie)
        return len(especies)
    
    def listar_especies(self):
        print("-Espécies no Parque--")
        especies = []
        for i in self.__plantas:
            if i.especie not in especies:
                especies.append(i.especie)
        for i in especies:
            print(i.nome)
    
    def listar_plantas_por_especie(self):
        plantas_ordenadas = {}
        print("--Plantas existentes, ordenadas por espécie--")
        for i in self.__plantas:
            especie = i.especie.nome
            if especie not in plantas_ordenadas:
                plantas_ordenadas[especie] = []
            plantas_ordenadas[especie].append(i)
        for especie, plantas in plantas_ordenadas.items():
            print("Espécie: " + especie)
            for planta in plantas:
                print("Planta em localização:" + str(planta.loc) +", Ano de plantação:" + str(planta.ano_plantacao))
    
    def listar_plantas_por_ano(self):
        plantas_ordenadas = {}
        print("--Plantas existentes, ordenadas por ano de plantação--")
        for i in self.__plantas:
            ano = i.ano_plantacao
            if ano not in plantas_ordenadas:
                plantas_ordenadas[ano] = []
            plantas_ordenadas[ano].append(i)
        for ano, plantas in plantas_ordenadas.items():
            print("Ano de plantação: " + str(ano))
            for planta in plantas:
                print("Espécie:" + str(planta.especie.nome)+", Planta em localização:" + str(planta.loc))
                
    def plantas_com_mais_idademedia(self, ano):
        plantas_velhas = []
        for i in self.__plantas:
            especie = i.especie
            if i.idade(ano) >= especie.idade_media:
                plantas_velhas.append(i)
        if len(plantas_velhas) == 0:
            print("Não existe plantas no parque, cuja idade é igual ou maior ao número médio de anos de vida da sua espécie.")
        else:
            print("--Plantas cuja idade é igual ou maior ao número médio de anos de vida da sua espécie--")
            for p in plantas_velhas:
                print(p)
            

def ler_especies(ficheiro):
    lista_especies = []
    try:
        f = open(ficheiro, "r")
        for line in f:
            nome, folhagem, produzfruto, tipo, raioocupado, idade_media = line.strip().split(",")
            especie = Especie(nome, folhagem, bool(produzfruto), tipo, float(raioocupado), int(idade_media))
            lista_especies.append(especie)
    except FileNotFoundError:
        print("O ficheiro não foi encontrado.")
    for i in lista_especies:
        print(i)
    return lista_especies
        

def gestao_de_um_parque(parque):
    if not isinstance(parque, Parque):
        print("O parque não é válido.")
        return
    opcao = ""
    while opcao != "9":
        print("Menu:")
        print("1. Adicionar planta")
        print("2. Remover planta")
        print("3. Listar plantas existentes")
        print("4. Mostrar a área ocupada")
        print("5. Mostrar a área disponível para plantação")
        print("6. Mostrar o mapa do parque")
        print("7. Estatísticas e informações")
        print("8. Guardar o parque num ficheiro")
        print("9. Sair")
        opcao = input("Escolha uma opção: ")
        if opcao == "1":
            Especie = input("Nome da espécie da planta:")
            especie = ""
            for i in lista_especies:
                if i.nome == Especie:
                    especie = i
            GPS = tuple(float(i) for i in input("Localização da planta:").split(","))
            ano_plantacao = int(input("Ano de plantação:"))
            planta = Planta(especie, GPS, ano_plantacao)
            return parque.add(planta)
        
        elif opcao == "2":
            loc = tuple(float(i) for i in input("Localização da planta a remover:").split(","))
            return parque.del_planta(loc)
        
        elif opcao == "3":
            return parque.listar_plantas_por_especie()
        
        elif opcao == "4":
            return parque.area_total_ocupada()
        
        elif opcao == "5":
            return parque.area_disponivel()
        
        elif opcao == "6":
            largura = float(input("Insira a largura do parque:"))
            comprimento = float(input("Insira o comprimento do parque:"))
            if largura*comprimento == parque.area_disponivel() + parque.area_total_ocupada():
                fig, ax = plt.subplots()
                ax.set_xlim((0, comprimento))
                ax.set_ylim((0, largura))
                ax.set_box_aspect(1)
            loc = []
            raio = []
            for i in parque.lista():
                loc.append(i.localizacao)
                raio.append(i.especie.raio_ocupado())
            for k in range(len(loc)):
                circle = plt.Circle(loc[k], raio[k], color='g', alpha=0.4)
                ax.add_patch(circle)
                ax.text(loc[k][0], loc[k][1], s="x", horizontalalignment='center', verticalalignment='center')
            plt.show()
            
        elif opcao == "7":
            escolha = ""
            while escolha != "9":
                print("Estatísticas e Informações::")
                print("1. Mostrar a média de idades das plantas do parque")
                print("2. Mostrar o número de espécies diferentes")
                print("3. Listar as espécies existentes no parque")
                print("4. Listar todas as plantas organizadas por espécie")
                print("5. Listar todas as plantas organizadas por ano de plantação")
                print("6. Listar as plantas que excederam o tempo médio de vida da sua espécie")
                print("7. Histograma por idade")
                print("8. Histograma por espécie")
                print("9. Sair")
                escolha = input("O que pretende ver: ")
                if escolha == "1":
                    ano = int(input("Qual o ano:"))
                    return parque.idade_media_plantas(ano)
                
                elif escolha == "2":
                    return parque.numero_especies()
                
                elif escolha == "3":
                    return parque.listar_especies()
                
                elif escolha == "4":
                    return parque.listar_plantas_por_especie()
                
                elif escolha == "5":
                    return parque.listar_plantas_por_ano()
                
                elif escolha == "6":
                    ano = int(input("Qual o ano:"))
                    return parque.plantas_com_mais_idademedia(ano)
                
                elif escolha == "7":
                    labels = []
                    values = []
                    ano = int(input("Qual o ano:"))
                    for i in parque.lista():
                        idade = i.idade(ano)
                        if idade not in labels:
                            labels.append(idade)
                            values.append(1)
                        else:
                            posicao = labels.index(idade)
                            values[posicao] += 1
                    plt.bar(labels, values)
                    plt.show()
                    
                elif escolha == "8":
                    labels = []
                    values = []
                    for i in parque.lista():
                        especie = i.especie.nome
                        if especie not in labels:
                            labels.append(especie)
                            values.append(1)
                        else:
                            posicao = labels.index(especie)
                            values[posicao] += 1
                    plt.bar(labels, values)
                    plt.show()
                    
                elif escolha == "9":
                    return 
        
        elif opcao == "8":
            nome_ficheiro = input("Qual é o nome do ficheiro?")
            f = open(nome_ficheiro, "w")
            f.write(f"{parque.nome_parque},{parque.area_de_plantacao}\n")
            f.close()
            for i in parque.lista():
                f = open(nome_ficheiro, "a")
                f.write(f"{i.especie.nome}, {i.localizacao}, {i.ano_plantacao}\n")
            f.close()
                        
def gestao_de_parques():
    opcao = ""
    while opcao != "6":
        print("Menu:")
        print("1. Adicionar parque")
        print("2. Carregar parque de um ficheiro")
        print("3. Remover parque")
        print("4. Listar parques")
        print("5. Gerir parque")
        print("6. Sari")
        opcao = input("Escolha uma opção:")
        if opcao == "1":
            nome = input("Qual o nome do parque, que deseja adicionar:")
            area = float(input("Qual a área do parque, em questão:"))
            nome = Parque(nome, area)
            return nome
            
        elif opcao == "2":
            ficheiro = input("Qual o nome do ficheiro:")
            parque = ""
            try:
                f = open(ficheiro, "r")
                nome_parque, area_plantacao = f.readline().strip().split(",")
                parque = Parque(nome_parque, float(area_plantacao))
                for line in f:
                    nome_especie, localizacao, ano_plantacao = line.strip().split(",")
                    GPS = tuple(float(i) for i in localizacao.split(","))
                    ano_de_plantacao = int(ano_plantacao)
                    especie = ""
                    for i in lista_especies:
                        if i.nome == nome_especie:
                            especie = i
                    if isinstance(especie, Especie):
                        planta = Planta(especie, GPS, ano_de_plantacao)
                        parque.add(planta)
                return parque
            except FileNotFoundError:
                print("O ficheiro não foi encontrado.")
            
        elif opcao == "3":
            return
        
        elif opcao == "4":
            return
        
        elif opcao == "5":
            nome_parque = input("Qual o nome do parque a gerir:")
            gestao_de_um_parque(nome_parque)
        
        elif opcao == "6":
            return 
            

lista_especies = ler_especies("especies.txt")         
Parque1 = Parque("José VII", 2000.0)
        
import math
import matplotlib.pyplot as plt
import numpy as np
