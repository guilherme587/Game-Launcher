from model import Model
from view import View
import os, threading
import requests
from io import BytesIO
from PIL import Image

class Controller:
    def __init__(self, api_key, resolucao: str = "600x400"):
        self.model = Model(api_key)
        self.view = View(resolucao)
        self.view.dd_caminhos.configure(values=self.model.gameRepositorios)
        self.view.set_button_click_callback(self.on_button_click)

    def load_games(self):
        games: list[tuple] = self.model.search_game_repoistorio()

        for gamesLit in games:
            print(gamesLit)
            self.busca_game(gamesLit, carregar_jogos=True)

    def on_button_click(self, game_name):
        self.busca_game(game_name)
    
    def busca_game(self, game: tuple, carregar_jogos: bool = False) -> None:
        if carregar_jogos:
            # Criar a pasta "gameImages" se não existir
            if not os.path.exists("gameImages"):
                os.makedirs("gameImages")

            index = self.view.criar_game_card(game)

            # Verificar se a imagem já existe
            safe_game_name = game[0].replace(" ", "_").replace("/", "_")
            image_path = os.path.join("gameImages", f"{safe_game_name}.png")
            if os.path.isfile(image_path):
                # Exibir a imagem existente
                self.view.update_image(index, image_path)
            else:
                # Fazer a chamada à API e salvar a imagem
                try:
                    image_url = self.model.search_game_image(game[0])
                    if image_url:
                        response = requests.get(image_url)
                        image = Image.open(BytesIO(response.content))
                        image.save(image_path)
                        self.view.update_image(index, image_path)
                except Exception as err:
                    Model.erro(err)
                    return
                else:
                    self.view.update_image_nao_encontrada(index)

    def atualiza_uso_hadware(self):
        cpu, ram, gpu, hardware = self.model.uso_hadware_porcentagem()
        print(hardware)
        self.view.atualiza_uso_hadware(cpu, ram, gpu, hardware)

        threading.Timer(0.45, self.atualiza_uso_hadware).start()

    def run(self):
        self.atualiza_uso_hadware()
        self.view.mainloop()
