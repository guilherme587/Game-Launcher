import os, GPUtil, psutil, customtkinter as ctk, clr
from collections import namedtuple
from requestImage import GameImageAPI

clr.AddReference(r'./dll/OpenHardwareMonitor/OpenHardwareMonitorLib')  # Atualize o caminho para o local correto da DLL
from OpenHardwareMonitor.Hardware import Computer

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
    Hardware = namedtuple("Hardware", ["cpu", "gpu"])

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

    def uso_hadware_porcentagem(self):
        uso_cpu = psutil
        memoria = psutil.virtual_memory()
        gpus = GPUtil.getGPUs()

        c = Computer()
        c.CPUEnabled = True
        c.GPUEnabled = True

        c.Open() # Abre a conexão com o hardware

        cpu = {
            "name": c.Hardware[0].Name,
             "load": 0,
             "power": 0,
             "clock": 0,
             "temperature": 0,
             "cores": 0
        }
        gpu = {
            "name": c.Hardware[1].Name,
            "load": 0,
            "power": 0,
            "clock": 0,
            "temperature": 0,
            "memory_clock": 0,
            "memory_used": 0,
            "memory_total": 0
        }
        
        cores = 1

        for sensor in c.Hardware[0].Sensors:
            if str(sensor.Name) == "CPU Total" and "Load" in str(sensor.SensorType):
                cpu["load"] = round(sensor.Value, 2)
            elif str(sensor.Name) == "CPU Core" and "Clock" in str(sensor.SensorType):
                cores += 1
                cpu["clock"] = round(sensor.Value, 2)
            elif  "Temperature" in str(sensor.SensorType):
                cpu["temperature"] = round(sensor.Value, 2)
            elif str(sensor.Name) == "CPU Cores" and "Power" in str(sensor.SensorType):
                cpu["power"] = round(sensor.Value, 2)
            
            # print(f"{sensor.Name} ({sensor.SensorType}): {round(sensor.Value, 2)}")

        cpu["cores"] = cores

        for sensor in c.Hardware[1].Sensors:
            if str(sensor.Name) == "GPU Core" and "Load" in str(sensor.SensorType):
                gpu["load"] = round(sensor.Value, 2)
            elif str(sensor.Name) == "GPU Core" and "Clock" in str(sensor.SensorType):
                gpu["clock"] = round(sensor.Value, 2)
            elif str(sensor.Name) == "GPU Memory" and "Clock" in str(sensor.SensorType):
                gpu["memory_clock"] = round(sensor.Value, 2)
            elif  "Temperature" in str(sensor.SensorType):
                gpu["temperature"] = round(sensor.Value, 2)
            elif str(sensor.Name) == "GPU Power" and "Power" in str(sensor.SensorType):
                gpu["power"] = round(sensor.Value, 2)
            elif str(sensor.Name) == "GPU Memory Total" and "SmallData" in str(sensor.SensorType):
                gpu["memory_total"] = round(sensor.Value, 2)
            elif str(sensor.Name) == "GPU Memory Used" and "SmallData" in str(sensor.SensorType):
                gpu["memory_used"] = round(sensor.Value, 2)
        
        hardware = self.Hardware(cpu=cpu, gpu=gpu)

        return uso_cpu, memoria, gpus, hardware

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

