import psutil
import pygetwindow as gw

def encontrar_jogo(nome_jogo):
    for proc in psutil.process_iter(['pid', 'name']):
        if nome_jogo.lower() in proc.info['name'].lower():
            return proc
    return None

def obter_janela_jogo(nome_jogo):
    janelas = gw.getWindowsWithTitle(nome_jogo)
    if janelas:
        return janelas[0]
    return None

# Nome do processo do jogo (ajuste conforme necessário)
nome_jogo = "KingdomTwoCrowns"

# Encontrar o processo do jogo
processo_jogo = encontrar_jogo(nome_jogo)
if processo_jogo:
    print(f"Processo do jogo encontrado: {processo_jogo.info['name']} (PID: {processo_jogo.info['pid']})")
    
    # Encontrar a janela do jogo
    janela_jogo = obter_janela_jogo(nome_jogo)
    if janela_jogo:
        print(f"Janela do jogo encontrada: {janela_jogo.title}")
    else:
        print("Janela do jogo não encontrada.")
else:
    print("Processo do jogo não encontrado.")






# import customtkinter as ctk
# import os

# # Função para abrir o jogo
# def abrir_jogo():
#     caminho_jogo = "D:\joojsC\Minecraft Dungeons\Dungeons.exe"  # Substitua pelo caminho do seu jogo
#     os.startfile(caminho_jogo)

# # Inicializando a aplicação
# root = ctk.CTk()
# root.geometry("600x300")
# root.title("Game Launcher")

# # Adicionando uma Label que abre o jogo ao ser clicada
# label = ctk.CTkLabel(root, text="Clique aqui para abrir o jogo", cursor="hand2")
# label.pack(pady=20)
# label.bind("<Button-1>", lambda e: abrir_jogo())

# # Adicionando um Botão para fechar o launcher
# botao = ctk.CTkButton(root, text="Fechar", command=root.destroy)
# botao.pack(pady=20)

# root.mainloop()




# import customtkinter as ctk
# import tkinter as tk

# class App:
#     def __init__(self, root):
#         self.window = root
#         self.window.title("Exemplo de Scrollbar Moderna")
#         self.window.geometry("600x400")

#         # Criando um frame para conter o canvas e a scrollbar
#         frame = ctk.CTkFrame(self.window)
#         frame.pack(fill="both", expand=True)

#         # Criando um canvas
#         self.canvas = tk.Canvas(frame)
#         self.canvas.pack(side="left", fill="both", expand=True)

#         # Adicionando uma scrollbar vertical
#         scrollbar = ctk.CTkScrollbar(frame, orientation="vertical", command=self.canvas.yview)
#         scrollbar.pack(side="right", fill="y")

#         # Configurando o canvas para usar a scrollbar
#         self.canvas.configure(yscrollcommand=scrollbar.set)

#         # Criando um frame dentro do canvas
#         self.scrollable_frame = ctk.CTkFrame(self.canvas)
#         self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

#         # Adicionando widgets ao frame rolável com 5 colunas
#         colunas = 5
#         linhas = 20  # Número de linhas desejadas
#         for i in range(linhas):
#             row_frame = ctk.CTkFrame(self.scrollable_frame)
#             row_frame.pack(fill="x", expand=True)
#             for j in range(colunas):
#                 label = ctk.CTkLabel(row_frame, width=200, height=300, text=f"Jogo {i * colunas + j + 1}")
#                 label.pack(side="left", padx=10, pady=10, expand=True)

#         # Atualizando a região rolável do canvas
#         self.scrollable_frame.update_idletasks()
#         self.canvas.config(scrollregion=self.canvas.bbox("all"))

# # Inicializando a aplicação
# root = ctk.CTk()
# app = App(root)
# root.mainloop()
