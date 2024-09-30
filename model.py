import os, GPUtil, psutil, customtkinter as ctk
from requestImage import GameImageAPI

class Model:
    gameRepositorios: list[str] = [
        "C:\\joojs",
        "C:\\joojsC",
        "D:\\joojs",
        "D:\\joojsC",
        #Steam
        "C:\\Program Files (x86)\\Steam\\steamapps\\common",
        "D:\\SteamLibrary\\steamapps\\common",
        #Epic
        "C:\\Program Files\\Epic Games",
        #GOG
        "C:\\Program Files (x86)\\GOG Galaxy\\Games",
        #Ubisoft
        "C:\\Program Files (x86)\\Ubisoft\\Ubisoft Game Launcher\\games",
        #EA
        "C:\\Program Files\\EA Games",
        #Battle.net
        "C:\\Program Files (x86)\\Battle.net",
        #Xbox App
        #"C:\\Program Files\\WindowsApps"
    ]

    def __init__(self, api_key: str = ""):
        self.gameApi = GameImageAPI(api_key)
        self.data = "Olá, CustomTkinter!"
    
    def search_game_image(self, game_name):
        return self.gameApi.search_game_image(game_name)
    
    def search_game_repoistorio(self) -> list[str]:
        pastas: list[str] = list()
        for caminho in self.gameRepositorios:
            if not os.path.exists(caminho):
                continue
            if len([nome for nome in os.listdir(caminho) if os.path.isdir(os.path.join(caminho, nome))]) == 0:
                continue

            # pastas.append([nome for nome in os.listdir(caminho) if os.path.isdir(os.path.join(caminho, nome))])

            for nome_pasta in os.listdir(caminho):
                caminho_pasta = os.path.join(caminho, nome_pasta)
                
                # Verificando se é um diretório
                if os.path.isdir(caminho_pasta):
                    # Procurando por arquivos executáveis dentro do diretório
                    for nome_arquivo in os.listdir(caminho_pasta):
                        if nome_arquivo.endswith(".exe"):  # Verificando se o arquivo é um executável
                            caminho_executavel = os.path.join(caminho_pasta, nome_arquivo)
                            pastas.append((nome_pasta, caminho_executavel))
                            break  # Parando após encontrar o primeiro executável

        # print(pastas)

        return pastas

    @staticmethod
    def uso_hadware_porcentagem():
        uso_cpu = psutil
        memoria = psutil.virtual_memory()
        gpus = GPUtil.getGPUs()

        return uso_cpu, memoria, gpus

    def get_data(self):
        return self.data
    
    @staticmethod
    def erro(erro: Exception):
        def fechar_aplicacao():
            root.destroy()

        # Inicializando a aplicação
        root = ctk.CTk()
        root.title(erro.__class__.__name__)
        root.geometry("400x200")

        # Adicionando a Label
        label = ctk.CTkLabel(root, text=f"{erro}", wraplength=350)
        label.pack(pady=20)

        # Adicionando o Botão
        botao = ctk.CTkButton(root, text="OK", command=fechar_aplicacao)
        botao.pack(pady=20)

        root.mainloop()

