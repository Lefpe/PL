#nesta versão tive bastante dificuldade, pois tive que lidar com erros de indentação com a interface gráfica
# utilizei a biblioteca tkinter para criar a interface gráfica
#e o código base utilizado do simplex revisado
#falta implementações ainda também
import tkinter as tk
from tkinter import ttk

import numpy as np
from scipy.optimize import linprog


class SimplexGUI(tk.Tk):

  def __init__(self):
    super().__init__()
    self.title("--Simplex de Padaria--")

    self.objective_frame = ttk.Frame(self)
    self.objective_frame.pack(pady=10)
#interface de entrada de dados
    ttk.Label(self.objective_frame,
              text="Função Objetivo (F.O)").grid(row=0,
                                                 column=0,
                                                 columnspan=3,
                                                 pady=5)
    self.objective_coefficients = []
    for i in range(3):
      entry = ttk.Entry(self.objective_frame, width=5)
      entry.grid(row=1, column=i, padx=5)
      self.objective_coefficients.append(entry)

    ttk.Label(self.objective_frame, text="Objetivo").grid(row=1,
                                                          column=3,
                                                          padx=5)
    self.objective_type = ttk.Combobox(self.objective_frame,
                                       values=["Maximizar", "Minimizar"])
    self.objective_type.grid(row=1, column=4)
    self.objective_type.set("Maximizar")

    self.constraint_frame = ttk.Frame(self)
    self.constraint_frame.pack(pady=10)

    ttk.Label(self.constraint_frame, text="Restrições").grid(row=0,
                                                             column=0,
                                                             columnspan=3,
                                                             pady=5)
    self.constraint_coefficients = []
    for i in range(3):
      entry = ttk.Entry(self.constraint_frame, width=5)
      entry.grid(row=1, column=i, padx=5)
      self.constraint_coefficients.append(entry)

    ttk.Label(self.constraint_frame, text="Relação").grid(row=1,
                                                          column=3,
                                                          padx=5)
    self.relation = ttk.Combobox(self.constraint_frame, values=["≤", "≥"])
    self.relation.grid(row=1, column=4)
    self.relation.set("≤")

    ttk.Label(self.constraint_frame, text="Valor").grid(row=1,
                                                        column=5,
                                                        padx=5)
    self.constraint_value = ttk.Entry(self.constraint_frame, width=5)
    self.constraint_value.grid(row=1, column=6, padx=5)

    self.add_constraint_button = ttk.Button(self.constraint_frame,
                                            text="Adicionar Restrição",
                                            command=self.add_constraint)
    self.add_constraint_button.grid(row=1, column=7, padx=5)

    ttk.Label(self, text="Método de Solução").pack(pady=5)
    self.method_var = tk.StringVar()
    self.method_combobox = ttk.Combobox(self,
                                        values=["Duas Fases", "Big M"],
                                        textvariable=self.method_var)
    self.method_combobox.pack(pady=5)
    self.method_combobox.set("Duas Fases")

    self.result_text = tk.Text(self, height=10, width=50)
    self.result_text.pack(pady=10)

    self.solve_button = ttk.Button(self,
                                   text="Resolver",
                                   command=self.show_result)
    self.solve_button.pack()

    self.show_result_button = ttk.Button(self,
                                         text="Exibir Resultado",
                                         command=self.show_result_window)
    self.show_result_button.pack()

    # Nova janela para exibir a tabela final e resultado
    self.result_window = tk.Toplevel(self)
    self.result_window.title("Resultado")
    self.result_text_final = tk.Text(self.result_window, height=10, width=50)
    self.result_text_final.pack(pady=10)

  def add_constraint(self):
    # Obter os coeficientes da restrição
    coefficients = [
        entry.get().replace(',', '.') or '0'
        for entry in self.constraint_coefficients
    ]
    # Obter a relação e o valor da restrição
    relation = self.relation.get()
    value = self.constraint_value.get().replace(',', '.') or '0'

    constraint_str = f"{', '.join(coefficients)} {relation} {value}\n"
    self.result_text.insert(tk.END, constraint_str)

    # Limpar campos de entrada
    for entry in self.constraint_coefficients:
      entry.delete(0, tk.END)
    self.relation.set("≤")
    self.constraint_value.delete(0, tk.END)

  def solve(self):
    # Limpar a janela de resultados
    self.result_text_final.delete(1.0, tk.END)

    # Obter o resultado ao resolver
    result = self.solve_linear_programming()

    # Exibir a tabela final e resultado na nova janela
    if isinstance(result, str):
      # Se a solução não foi encontrada
      self.result_text_final.insert(tk.END, result)
    else:
      headers = ["Variável"] + [f"x{i}"
                                for i in range(1,
                                               len(result.x) + 1)] + ["RHS"]
      tableau = np.column_stack((result.x, result.A[:, :-2], result.b))
      self.show_table(self.result_text_final, tableau, headers)

  def solve_linear_programming(self):
    # Obter os coeficientes da função objetivo, tipo de objetivo e restrições
    objective_coefficients = [
        float(entry.get().replace(',', '.') or '0')
        for entry in self.objective_coefficients
    ]
    objective_type = self.objective_type.get()
    constraints = [
        constraint_str.strip() for constraint_str in self.result_text.get(
            "1.0", tk.END).strip().split("\n")
    ]

    # Construir matrizes para resolver o problema de programação linear
    A = []
    b = []
    for constraint in constraints:
      coefficients, relation, value = self.parse_constraint(constraint)
      A.append(coefficients)
      b.append(value)

    A = np.array(A)
    b = np.array(b)

    # Se o tipo de objetivo for "Minimizar", negar os coeficientes
    if objective_type == "Minimizar":
      objective_coefficients = [-x for x in objective_coefficients]

    # Determinar o método de solução selecionado
    solution_method = self.method_var.get()

    # Resolver usando linprog de scipy
    if solution_method == "Duas Fases":
      result = self.two_phase_simplex(A, b, objective_coefficients)
    elif solution_method == "Big M":
      result = self.big_m_simplex(A, b, objective_coefficients)
    else:
      result = "Método não reconhecido"

    return result

  def show_result(self):
    self.solve()

  def show_result_window(self):
    self.solve()
    self.result_window.deiconify()

  def show_table(self, text_widget, tableau, headers):
    text_widget.insert(tk.END, "\nTabela:\n")
    text_widget.insert(tk.END, "\t".join(headers) + "\n")
    for row in tableau:
      text_widget.insert(tk.END, "\t".join(map(str, row)) + "\n")

  def parse_constraint(self, constraint):
    parts = constraint.strip().split()
    coefficients_str = [x.replace(',', '.') for x in parts[:-2]]
    relation = parts[-2]
    value_str = parts[-1]

    coefficients = [float(x) for x in coefficients_str]
    value = float(value_str)

    if relation == "≤":
      return coefficients, "<=", value
    elif relation == "≥":
      return [-x for x in coefficients], ">=", -value
    else:
      raise ValueError("Unsupported constraint relation")

  def two_phase_simplex(self, A, b, c):
    # Adicionar uma coluna de variáveis de folga
    A = np.hstack((A, np.eye(A.shape[0])))
    # Inicializar a tabela
    tableau = np.column_stack((c, A, b))
    # Inicializar variáveis auxiliares
    pivot_row = 0
    pivot_column = 0
    num_original_variables = A.shape[1]
    # Loop principal
    while True:
      # Encontrar a coluna de pivô
      pivot_column = np.argmin(tableau[0, :-1])
      # Verificar se a solução ótima foi encontrada
      if tableau[0, pivot_column] >= 0:
        break
      # Encontrar a linha de pivô
      ratios = tableau[1:, -1] / tableau[1:, pivot_column]
      pivot_row = np.argmin(ratios) + 1
      # Verificar se a solução é ilimitada
      if all(ratio <= 0 for ratio in ratios):
        return "Solução Ilimitada"
      # Atualizar a tabela
      tableau[pivot_row, :] /= tableau[pivot_row, pivot_column]
      for i in range(tableau.shape[0]):
        if i != pivot_row:
          tableau[i, :] -= tableau[i, pivot_column] * tableau[pivot_row, :]
    # Obter a solução ótima
    x = np.zeros(num_original_variables)
    for i in range(num_original_variables):
      column = tableau[1:, i]
      if np.count_nonzero(column) == 1 and np.sum(column) == 1:
        pivot_row = np.argmax(column) + 1
        x[i] = tableau[pivot_row, -1]
    # Calcular o valor da função objetivo
    objective_value = -tableau[0, -1]
    # Retornar a solução ótima e o valor da função objetivo
    return x, objective_value

  def big_m_simplex(self, A, b, c):
    # Adicionar variáveis de folga e excesso
    num_constraints, num_variables = A.shape
    slack_variables = np.eye(num_constraints)
    excess_variables = np.eye(num_constraints)

    A = np.hstack((A, slack_variables, excess_variables))
    c = np.concatenate((c, np.zeros(2 * num_constraints)))

    # Resolver usando linprog de scipy
    result = linprog(c=c, A_ub=A, b_ub=b, method='highs')

    return result


if __name__ == "__main__":
  app = SimplexGUI()
  app.mainloop()
