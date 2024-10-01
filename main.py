import customtkinter as ctk
from tkinter import PhotoImage
from controller import Controller

if __name__ == "__main__":
    API_KEY = "e5472db761a14f029c156877863019b9"
    RESOLUCAO = "960x540"
    
    # app = Controller(API_KEY, RESOLUCAO)
    # app.load_games()
    # app.run()

    try:
        app = Controller(API_KEY, RESOLUCAO)
        app.load_games()
        app.run()
    except Exception as err:
        def fechar_aplicacao():
            root.destroy()

        # Inicializando a aplicação
        root = ctk.CTk()
        root.geometry("400x200")
        root.title(err.__class__.__name__)
        root.wm_iconbitmap("./icons/icone.ico")

        # Adicionando a Label
        label = ctk.CTkLabel(root, text=f"{err}", wraplength=350)
        label.pack(pady=20)

        # Adicionando o Botão
        botao = ctk.CTkButton(root, text="OK", command=fechar_aplicacao)
        botao.pack(pady=20)

        root.mainloop()

