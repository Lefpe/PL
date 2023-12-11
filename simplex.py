# PL
Programação Linear
#avaliação n3
#disciplina de programação linear
#implementação do simplex
import numpy as np
import copy
#implementação do simplex

class Simplex:
    def __init__(self):
       self.table = []
        #implementação do simplex, função objetivo
       def F_o (self, fo: list):
        self.table.append(fo)
        #adiciona as restrições
        def add_restriction (self, sa: list):
            self.table.append(sa)
        #procura do pivo
        def entry_column (self,) -> list:
            #o pivo fica localizado na coluna 0, e é o menor valor desta coluna
            pivo_column = min(self.table.[0]):
            index = self.table[0].index(pivo_column)
            return self.table[index]
            def line_exit (self, entry_column: int) -> int:
                result = {}
                for line in range (len(self.table)):
                    #verificar se o pivo é maior que 0
                    if line > 0:
                        if self.table[line][entry_column] > 0:
                            division = self.table[line][-1] / self.table[line][entry_column]
                            result[line] = division
                            index = min(results, key=results.get)

                            return index

                            def calcular_nova_linha (self, linha: list entry_column: int, pivo_line: list) -> list:
                                pivo = line[entry_column] * [-1]
                                #verificação
                                result_line = [value* pivo for value in pivo_line]
                                 nova_line = []

                                
                            for i in range (len(result_line)):
                                soma = result_line[i] + line [i]
                                nova_line.append(soma)
                                return nova_line
                                def negative_verication (self) -> bool:
                                    negative = list(filter(lambda x: x < 0, self.table [0]))
                                    
                                    if len(negative) > 0:
                                        return True
                                        else 
                                        return False

                                        def mostrar_table (self):
                                            for i in range (len(self.table)):
                                                for j in range (len (self.table[0])):
                                                print (f"{self.table[i][j]}\t", end = "")
                                                print ()

                                        def calcular(self):
                                            entry_column = self.entry_column ()
                                            primeira_exit_line = self.line_exit (entry_column)
                                            pivo_line = self.table[new_line_exit]
                                            #substitute line
                                            self.table[new_line_exit] = pivo_line

                                            tableau = self.table.copy()

                                        while index < len (self.table):
                                            if index != new_line_exit:
                                                line = tableau [index]
                                                new_line = self.calcular_nova_linha(line, entry_column, pivo_line)
                                                index += 1

                                                def solve(self):
                                                    self.calculate()
                                                    while self.negative_verication():
                                                        self.calculate()
                                                        self.mostrar_tabela()
                                                        if __name__ == '__simplex de padaria 1.0__':
                                                            """
                                                            MAX : Z = 5x + 8y
                                                            3x + 2y <= 6
                                                            10x + 12y <= 60
                                                            x,y >= 0

                                                            forma simples: 
                                                             z - 5x -2y = 0
                                                             2x + y + f1 = 6
                                                             10x + 12y + f2 = 60

                                                            """
                                                        simplex = Simplex()

                                     # Adicionando a função objetivo
                           simplex.set_objective_function([1, -5, -2, 0, 0, 0])

                          # Adicionando as restrições
                                simplex.add_restrictions([0, 3, 2, 1, 0, 0, 6])
                               simplex.add_restrictions([0, 10, 12, 0, 1, 0, 60])

                             # Resolvendo o problema
                                simplex.solve()

