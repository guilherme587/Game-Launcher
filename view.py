import os
import customtkinter as ctk
from PIL import Image, ImageTk, ImageDraw
import psutil, GPUtil, tkinter as tk
from tkinter import PhotoImage

COR_CANVAS: str = "gray"
FONTE_PESO_TITULO: int = 22
FONTE_PESO_PARAGRAFO: int = 16
LARGURA_DA_IMAGEM: int = 242
ALTURA_DA_IMAGEM: int = 364

class View:
    ultima_coluna: int = 1
    frame_game_list: list = list()

    def __init__(self, resolucao: str = "600x400"):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.window = ctk.CTk()
        self.window.geometry(resolucao)
        self.window.title("Chrono Launch - Game Manager")
        self.window.wm_iconbitmap("./icons/icone.ico")
        
        self.container_main()

        self.dd_caminhos = ctk.CTkOptionMenu(self.scrollable_frame, command=self.selecionar_opcao, width=500)
        self.dd_caminhos.pack(pady=20)
             
        self.container_hadware()
        self.container_game_list()

        self.game_cards = list()
        self.game_cards.append(ctk.CTkLabel(self.frame_games, text=""))
        self.game_cards[0].pack(pady=10)

    def selecionar_opcao(self, escolha):
        print(f"Você selecionou: {escolha}")

    def buscar_jogo(self):
        self.label = ctk.CTkLabel(self.window, text="Digite o nome do jogo e clique em Buscar", font=("Arial", 20))
        self.label.pack(pady=20)

        self.entry = ctk.CTkEntry(self.window, width=300)
        self.entry.pack(pady=10)

        self.button = ctk.CTkButton(self.window, text="Buscar", command=self.on_button_click)
        self.button.pack(pady=10)
    
    def container_main(self):
        # Criando um frame para conter o canvas e a scrollbar
        self.frame_main = ctk.CTkFrame(self.window)
        self.frame_main.pack(fill="both", expand=True)

        # Criando um canvas
        self.canvas_main = tk.Canvas(self.frame_main, background=COR_CANVAS)
        self.canvas_main.pack(side="left", fill="both", expand=True)

        # Adicionando uma scrollbar vertical
        self.scrollbar_main = ctk.CTkScrollbar(self.frame_main, orientation="vertical", width=25, command=self.canvas_main.yview)
        self.scrollbar_main.pack(side="right", fill="y")

        # Configurando o canvas para usar a scrollbar
        self.canvas_main.configure(yscrollcommand=self.scrollbar_main.set)

        # Criando um frame dentro do canvas
        self.scrollable_frame = ctk.CTkFrame(self.canvas_main)
        self.canvas_main.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
    
    def container_hadware(self):
        self.frame_desempenho = ctk.CTkFrame(self.scrollable_frame)
        self.frame_desempenho.pack(padx=20, pady=20, fill="both", expand=True)
        ctk.CTkLabel(self.frame_desempenho, text="Hardware", font=("Arial", 20)).pack(pady=5)

        paddingX = 40
        paddingY = 60
        paddingDetalhes = 20
        paddingFrameDetalhes = 10

        ########## CPU ##########
        self.frame_cpu = ctk.CTkFrame(self.frame_desempenho)
        self.frame_cpu.pack(side="left", padx=20, pady=20, fill="both", expand=True)
        self.lbl_uso_cpu = ctk.CTkLabel(self.frame_cpu, font=("Arial", FONTE_PESO_TITULO), text="CPU:")
        self.lbl_uso_cpu.pack(padx=5, pady=5)

        self.uso_cpu = ctk.CTkLabel(self.frame_cpu, image=View.criar_label_redonda(), font=("Arial", 32), text="0%")
        self.uso_cpu.pack(side="left", padx=10, pady=10)

        self.frame_cpu_detalhes = ctk.CTkFrame(self.frame_cpu, corner_radius=20)
        self.frame_cpu_detalhes.pack(side="left", padx=paddingFrameDetalhes, pady=paddingFrameDetalhes, fill="both", expand=False)
        self.temp_cpu = ctk.CTkLabel(self.frame_cpu_detalhes, font=("Arial", FONTE_PESO_PARAGRAFO), image=View.criar_label_redonda(width=135, height=80, radius=12), text="0 °C")
        self.temp_cpu.pack(padx=10, pady=10)
        self.clock_cpu = ctk.CTkLabel(self.frame_cpu_detalhes, font=("Arial", FONTE_PESO_PARAGRAFO), image=View.criar_label_redonda(width=135, height=80, radius=12), text="0Ghz")
        self.clock_cpu.pack(padx=10, pady=10)



        ########## RAM ##########
        self.frame_ram = ctk.CTkFrame(self.frame_desempenho)
        self.frame_ram.pack(side="left", padx=20, pady=20, fill="both", expand=True)
        self.lbl_uso_ram = ctk.CTkLabel(self.frame_ram, font=("Arial", FONTE_PESO_TITULO), text="RAM:")
        self.lbl_uso_ram.pack(padx=5, pady=5)

        self.uso_ram = ctk.CTkLabel(self.frame_ram, image=View.criar_label_redonda(color="blue"), font=("Arial", 32), text="0%")
        self.uso_ram.pack(side="left", padx=10, pady=10)

        self.frame_ram_detalhes = ctk.CTkFrame(self.frame_ram, corner_radius=20)
        self.frame_ram_detalhes.pack(side="left", padx=paddingFrameDetalhes, pady=paddingFrameDetalhes, fill="both", expand=False)
        self.ram_usada = ctk.CTkLabel(self.frame_ram_detalhes, font=("Arial", FONTE_PESO_PARAGRAFO), image=View.criar_label_redonda(width=135, height=80, radius=12, color="blue"), text="12271 MB")
        self.ram_usada.pack(padx=10, pady=10)
        self.ram_total = ctk.CTkLabel(self.frame_ram_detalhes, font=("Arial", FONTE_PESO_PARAGRAFO), image=View.criar_label_redonda(width=135, height=80, radius=12, color="blue"), text="24496 MB")
        self.ram_total.pack(padx=10, pady=10)

        ########## GPU ##########
        self.frame_gpu = ctk.CTkFrame(self.frame_desempenho)
        self.frame_gpu.pack(side="left", padx=20, pady=20, fill="both", expand=True)
        self.lbl_uso_gpu = ctk.CTkLabel(self.frame_gpu, font=("Arial", FONTE_PESO_TITULO), text="GPU:")
        self.lbl_uso_gpu.pack(padx=5, pady=5)

        self.uso_gpu = ctk.CTkLabel(self.frame_gpu, image=View.criar_label_redonda(color="red"), font=("Arial", 32), text="0%")
        self.uso_gpu.pack(side="left", padx=10, pady=10)

        self.frame_gpu_detalhes = ctk.CTkFrame(self.frame_gpu, corner_radius=20)
        self.frame_gpu_detalhes.pack(side="left", padx=paddingFrameDetalhes, pady=paddingFrameDetalhes, fill="both", expand=False)
        self.vram_usada = ctk.CTkLabel(self.frame_gpu_detalhes, font=("Arial", FONTE_PESO_PARAGRAFO), image=View.criar_label_redonda(width=135, height=80, radius=12, color="red"), text="1227 MB")
        self.vram_usada.grid(row=0, column=0, padx=10, pady=10)
        self.vram_total = ctk.CTkLabel(self.frame_gpu_detalhes, font=("Arial", FONTE_PESO_PARAGRAFO), image=View.criar_label_redonda(width=135, height=80, radius=12, color="red"), text="6128 MB")
        self.vram_total.grid(row=0, column=1,padx=10, pady=10)
        self.temp_gpu = ctk.CTkLabel(self.frame_gpu_detalhes, font=("Arial", FONTE_PESO_PARAGRAFO), image=View.criar_label_redonda(width=135, height=80, radius=12, color="red"), text="0 °C")
        self.temp_gpu.grid(row=1, column=0, padx=10, pady=10)
        self.clock_gpu = ctk.CTkLabel(self.frame_gpu_detalhes, font=("Arial", FONTE_PESO_PARAGRAFO), image=View.criar_label_redonda(width=135, height=80, radius=12, color="red"), text="0Mhz")
        self.clock_gpu.grid(row=1, column=1,padx=10, pady=10)

    def container_game_list(self):
        # Criando um frame para conter o canvas e a scrollbar
        self.frame_games = ctk.CTkFrame(self.scrollable_frame)
        self.frame_games.pack(fill="both", expand=True)
        ctk.CTkLabel(self.frame_games, text="Biblioteca", font=("Arial", 20)).pack(pady=5)

        # Criando um canvas
        self.canvas_game_list = tk.Canvas(self.frame_games, background=COR_CANVAS, height=500)
        self.canvas_game_list.pack(side="left", fill="both", expand=True)

        # Adicionando uma scrollbar vertical
        self.scrollbar_game_list = ctk.CTkScrollbar(self.frame_games, orientation="vertical", width=25, command=self.canvas_game_list.yview)
        self.scrollbar_game_list.pack(side="right", fill="y")

        # Configurando o canvas para usar a scrollbar
        self.canvas_game_list.configure(yscrollcommand=self.scrollbar_game_list.set)

        # Criando um frame dentro do canvas
        self.scrollable_frame_game_list = ctk.CTkFrame(self.canvas_game_list)
        self.canvas_game_list.create_window((0, 0), window=self.scrollable_frame_game_list, anchor="nw")

    def criar_game_card(self, game) -> int:
        if not self.frame_game_list:
            self.frame_game_list.append(ctk.CTkFrame(self.scrollable_frame_game_list))
            self.frame_game_list[-1].pack(fill="x", expand=True)
        
        self.game_cards.append(ctk.CTkLabel(self.frame_game_list[-1], text=game[0], wraplength=100, cursor="hand2"))
        self.game_cards[-1].pack(side="left",padx=10, pady=10, expand=True)
        self.game_cards[-1].bind("<Button-1>", lambda e: View.abrir_jogo(game[1]))

        if self.ultima_coluna >= 7:
            self.ultima_coluna = 0
            self.frame_game_list.append(ctk.CTkFrame(self.scrollable_frame_game_list))
            self.frame_game_list[-1].pack(fill="x", expand=True)
        
        self.ultima_coluna += 1

        return len(self.game_cards) -1

    @staticmethod
    def abrir_jogo(caminho_jogo = "D:\joojsC\Minecraft Dungeons\Dungeons.exe"):
        os.startfile(caminho_jogo)

    @staticmethod
    def criar_label_redonda(width = 300, height = 200, radius = 20, color = "green"):
        image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        draw.rounded_rectangle((0, 0, width, height), radius, fill=color)
        return ImageTk.PhotoImage(image)

    def on_button_click(self):
        if self.button_click_callback:
            self.button_click_callback(self.entry.get())

    def set_button_click_callback(self, callback):
        self.button_click_callback = callback

    def update_image(self, index, image_path, radius = 15) -> None:
        image = Image.open(image_path)
        image = image.resize((LARGURA_DA_IMAGEM, ALTURA_DA_IMAGEM), Image.LANCZOS)
        
        # Criando uma máscara para bordas arredondadas
        mask = Image.new("L", image.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.rounded_rectangle((0, 0) + image.size, radius, fill=255)
        
        # Aplicando a máscara à imagem
        rounded_image = Image.new("RGBA", image.size)
        rounded_image.paste(image, (0, 0), mask)
        
        photo = ImageTk.PhotoImage(rounded_image)
        self.game_cards[index].configure(image=photo)
        self.game_cards[index].image = photo
    
    def update_image_nao_encontrada(self, index):
        photo = View.criar_label_redonda(width=LARGURA_DA_IMAGEM, height=ALTURA_DA_IMAGEM, radius=15, color="gray")
        self.game_cards[index].configure(image=photo)
        self.game_cards[index].image = photo

    def atualiza_uso_hadware(self, cpu: psutil, ram: psutil.virtual_memory, gpu: GPUtil.getGPUs):
        clock_min = cpu.cpu_freq().min 
        clock_max = cpu.cpu_freq().max
        self.lbl_uso_cpu.configure(text=f"CPU: {cpu.cpu_count(False)}/{cpu.cpu_count(True)}")
        self.uso_cpu.configure(text=f"{cpu.cpu_percent(interval=1)}%")
        self.clock_cpu.configure(text=f"{clock_min}/{clock_max}Mhz")
        # if 'coretemp' in cpu.sensors_temperatures():
        #     self.temp_cpu.configure(text=f"{cpu.sensors_temperatures()['coretemp'][0].current} °C")
        # else:
        #     self.temp_cpu.configure(text="Erro")

        self.uso_ram.configure(text=f"{ram.percent}%")
        self.ram_usada.configure(text=f"{round(ram.used / (1024 ** 3), 2)}GB")
        self.ram_total.configure(text=f"{round(ram.total / (1024 ** 3), 2)}GB")

        self.lbl_uso_gpu.configure(text=f"GPU: {gpu[-1].name} \n Driver: {gpu[-1].driver}")
        self.uso_gpu.configure(text=f"{round(gpu[-1].load * 100, 2)}%")
        self.vram_usada.configure(text=f"{gpu[-1].memoryUsed}MB")
        self.vram_total.configure(text=f"{gpu[-1].memoryTotal}MB")
        self.temp_gpu.configure(text=f"{gpu[-1].temperature} °C")
        # self.clock_gpu.configure(text=f"{gpu[-1].clock} Mhz")


    def mainloop(self):
        self.scrollable_frame.update_idletasks()
        self.canvas_main.config(scrollregion=self.canvas_main.bbox("all"))

        self.scrollable_frame_game_list.update_idletasks()
        self.canvas_game_list.config(scrollregion=self.canvas_game_list.bbox("all"))

        self.window.mainloop()
