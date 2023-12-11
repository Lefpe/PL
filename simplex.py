# PL
# Programação Linear
# Avaliação n3
# Disciplina de programação linear
# Implementação do simplex
import numpy as np
import copy

class Simplex:
    def __init__(self):
        self.table = []

    # Implementação do simplex, função objetivo
    def F_o(self, fo: list):
        self.table.append(fo)

    # Adiciona as restrições
    def add_restriction(self, sa: list):
        self.table.append(sa)

    # Procura do pivo
    def entry_column(self) -> int:
        # O pivo fica localizado na coluna 0, e é o menor valor desta coluna
        pivo_column = min(self.table[0])
        index = self.table[0].index(pivo_column)
        return index
#linha  que sai
    def line_exit(self, entry_column: int) -> int:
        result = {}
        for line in range(len(self.table)):
            # Verificar se o pivo é maior que 0
            if line > 0:
                if self.table[line][entry_column] > 0:
                    division = self.table[line][-1] / self.table[line][entry_column]
                    result[line] = division
        index = min(result, key=result.get)
        return index
    #calcular a nova linha que entra
    def calcular_nova_linha(self, line: list, entry_column: int, pivo_line: list) -> list:
        pivo = line[entry_column] * -1
        # Verificação
        result_line = [value * pivo for value in pivo_line]
        #a nova_line (nova linha) estava com erro de identação
        nova_line = [sum(value) for value in zip(result_line, line)]
        return nova_line

    def negative_verification(self) -> bool:
        negative = list(filter(lambda x: x < 0, self.table[0]))
        return True if len(negative) > 0 else False
#a função serve para mostrar a tabela
    def mostrar_table(self):
        for i in range(len(self.table)):
            for j in range(len(self.table[0])):
                print(f"{self.table[i][j]}\t", end="")
            print()
#calculando a nova coluna que entra e o pivo
    def calcular(self):
        entry_column = self.entry_column()
        primeira_exit_line = self.line_exit(entry_column)
        pivo_line = self.table[primeira_exit_line]
        # Substituir linha
        self.table[primeira_exit_line] = pivo_line
#optei por fazer uma cópia da tabela também, para que fosse mais preciso
        tableau = self.table.copy()
# o tableau é somente para mostrar a cópia
        index = 0
        while index < len(self.table):
            if index != primeira_exit_line:
                line = tableau[index]
                nova_line = self.calcular_nova_linha(line, entry_column, pivo_line)
                self.table[index] = nova_line
            index += 1

# Exemplo de uso
if __name__ == '__main__':
    simplex = Simplex()
    #um exemplo a seguir
    """MAX : Z = 5x + 8y
                                                            3x + 2y <= 6
                                                            10x + 12y <= 60
                                                            x,y >= 0

                                                            forma simples: 
                                                             z - 5x -2y = 0
                                                             2x + y + f1 = 6
                                                             10x + 12y + f2 = 60

                                                            """

    # Adicionando a função objetivo
    simplex.F_o([1, -5, -2, 0, 0, 0])

    # Adicionando as restrições
    simplex.add_restriction([0, 3, 2, 1, 0, 0, 6])
    simplex.add_restriction([0, 10, 12, 0, 1, 0, 60])

    # Resolvendo o problema
    simplex.calcular()
    simplex.mostrar_table()
    

