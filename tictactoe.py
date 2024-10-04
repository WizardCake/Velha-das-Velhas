import tkinter as tk
from tkinter import messagebox


def criar_tabuleiro():
    return [[' ' for _ in range(3)] for _ in range(3)]


def criar_tabuleiros_menores():
    return [[criar_tabuleiro() for _ in range(3)] for _ in range(3)]


def verificar_vitoria(tabuleiro, simbolo):
    for i in range(3):
        if all([cell == simbolo for cell in tabuleiro[i]]):
            return True
        if all([tabuleiro[j][i] == simbolo for j in range(3)]):
            return True
    if all([tabuleiro[i][i] == simbolo for i in range(3)]) or all([tabuleiro[i][2 - i] == simbolo for i in range(3)]):
        return True
    return False


def tabuleiro_cheio(tabuleiro):
    return all([cell != ' ' for row in tabuleiro for cell in row])


class VelhaDasVelhas:
    def __init__(self, root):
        self.root = root
        self.root.title("Velha das Velhas")
        self.root.geometry("800x600")  # Define um tamanho inicial
        self.root.minsize(600, 400)    # Define um tamanho mínimo

        # Variável para armazenar o modo de jogo
        self.modo_avancado = False

        # Tela inicial para mostrar as regras
        self.tela_inicial()

    def tela_inicial(self):
        # Cria a tela inicial com as regras e botões para iniciar
        self.frame_inicial = tk.Frame(self.root, padx=20, pady=20)
        self.frame_inicial.pack(fill="both", expand=True)

        # Configura pesos para as linhas e colunas do frame inicial
        self.frame_inicial.columnconfigure(0, weight=1)
        self.frame_inicial.rowconfigure(0, weight=1)
        self.frame_inicial.rowconfigure(1, weight=0)

        regras = (
            "Regras do Velha das Velhas:\n\n"
            "Visão Geral do Jogo:\n"
            "- O jogo é composto por um grande tabuleiro (3x3), no qual cada célula contém um tabuleiro menor (também de 3x3).\n"
            "- O objetivo principal é vencer o grande tabuleiro, conquistando três tabuleiros menores em sequência, seja na horizontal, vertical ou diagonal.\n\n"
            "Regras Detalhadas:\n"
            "1. Estrutura do Jogo:\n"
            "   - O grande tabuleiro é formado por 9 tabuleiros menores, cada um com 9 células (3x3).\n"
            "   - Cada jogador é representado por um símbolo (X ou O).\n\n"
            "2. Como Jogar:\n"
            "   - O primeiro jogador pode escolher qualquer célula disponível em qualquer um dos tabuleiros menores.\n"
            "   - A célula escolhida determina em qual tabuleiro menor o próximo jogador deve jogar. Por exemplo, se você jogar em uma célula na posição central do tabuleiro menor, o próximo jogador precisará jogar no tabuleiro central do grande tabuleiro.\n\n"
            "3. Direcionamento das Jogadas:\n"
            "   - Se o tabuleiro menor indicado já tiver sido vencido por algum jogador ou empatado, o próximo jogador pode escolher qualquer tabuleiro menor disponível.\n"
            "   - Caso o tabuleiro menor esteja cheio e ainda não tenha sido vencido, ele será marcado como 'Empatado' (V).\n\n"
            "4. Como Vencer:\n"
            "   - Vencer um tabuleiro menor é similar ao jogo da velha tradicional: alinhe três símbolos iguais na horizontal, vertical ou diagonal.\n"
            "   - Quando um jogador vence um tabuleiro menor, ele 'conquista' a célula correspondente no grande tabuleiro.\n"
            "   - O objetivo final é vencer o grande tabuleiro, alinhando três tabuleiros menores conquistados na horizontal, vertical ou diagonal.\n\n"
            "5. Modo Avançado (Opcional):\n"
            "   - Quando uma jogada direciona para um tabuleiro já ganho, o jogador que venceu esse tabuleiro escolhe onde o próximo jogador deve jogar.\n"
            "   - Isso cria uma camada adicional de estratégia, permitindo que o jogador vencedor oriente a partida a seu favor.\n"
        )

        # Substitui o Label por um Text para melhor responsividade
        text_regras = tk.Text(self.frame_inicial, wrap="word", font=("Helvetica", 12))
        text_regras.insert("1.0", regras)
        text_regras.config(state="disabled")  # Torna o Text somente leitura
        text_regras.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # Adiciona uma barra de rolagem
        scrollbar = tk.Scrollbar(self.frame_inicial, command=text_regras.yview)
        scrollbar.grid(row=0, column=1, sticky='ns')
        text_regras.config(yscrollcommand=scrollbar.set)

        # Frame para os botões
        frame_botoes = tk.Frame(self.frame_inicial)
        frame_botoes.grid(row=1, column=0, columnspan=2, pady=20, sticky="nsew")

        frame_botoes.columnconfigure(0, weight=1)
        frame_botoes.columnconfigure(1, weight=1)

        botao_normal = tk.Button(frame_botoes, text="Jogo Normal", font=("Helvetica", 14),
                                 command=lambda: self.iniciar_jogo(avancado=False))
        botao_normal.grid(row=0, column=0, padx=10, sticky="nsew")

        botao_avancado = tk.Button(frame_botoes, text="Jogo Avançado", font=("Helvetica", 14),
                                   command=lambda: self.iniciar_jogo(avancado=True))
        botao_avancado.grid(row=0, column=1, padx=10, sticky="nsew")

    def iniciar_jogo(self, avancado):
        # Destrói a tela inicial e inicia o jogo
        self.frame_inicial.destroy()

        # Define o modo de jogo
        self.modo_avancado = avancado

        self.tabuleiro_maior = criar_tabuleiro()
        self.tabuleiros_menores = criar_tabuleiros_menores()
        self.jogador_atual = 'X'
        self.prox_linha_macro = -1
        self.prox_coluna_macro = -1

        self.frames = [[None for _ in range(3)] for _ in range(3)]
        self.buttons = [[None for _ in range(9)] for _ in range(9)]

        self.label_jogada = tk.Label(self.root, text=f"Jogada de: {self.jogador_atual}", font=("Helvetica", 16))
        self.label_jogada.pack(pady=10)

        self.create_buttons()

    def create_buttons(self):
        main_frame = tk.Frame(self.root, padx=10, pady=10)
        main_frame.pack(fill="both", expand=True)

        # Configurar pesos para as linhas e colunas do main_frame para que se expandam
        for i in range(3):
            main_frame.grid_rowconfigure(i, weight=1)
            main_frame.grid_columnconfigure(i, weight=1)

        for macro_linha in range(3):
            for macro_coluna in range(3):
                frame = tk.Frame(main_frame, relief=tk.RAISED, borderwidth=5, bg='black')
                frame.grid(row=macro_linha, column=macro_coluna, padx=5, pady=5, sticky="nsew")
                self.frames[macro_linha][macro_coluna] = frame

                frame.grid_rowconfigure(0, weight=1)
                frame.grid_columnconfigure(0, weight=1)

                sub_frame = tk.Frame(frame, relief=tk.RAISED, borderwidth=1)
                sub_frame.grid(row=0, column=0, sticky="nsew", padx=3, pady=3)

                # Configurar pesos para as linhas e colunas do sub_frame
                for i in range(3):
                    sub_frame.grid_rowconfigure(i, weight=1)
                    sub_frame.grid_columnconfigure(i, weight=1)

                for micro_linha in range(3):
                    for micro_coluna in range(3):
                        button = tk.Button(
                            sub_frame, text=" ", font=("Helvetica", 12),
                            command=lambda ml=macro_linha, mc=macro_coluna, mrl=micro_linha, mrc=micro_coluna: self.on_button_click(ml, mc, mrl, mrc)
                        )
                        button.grid(row=micro_linha, column=micro_coluna, padx=1, pady=1, sticky="nsew")
                        # Armazenar referência ao botão
                        self.buttons[macro_linha * 3 + micro_linha][macro_coluna * 3 + micro_coluna] = button

    def on_button_click(self, macro_linha, macro_coluna, micro_linha, micro_coluna):
        # Verifica se a jogada é válida
        if self.prox_linha_macro != -1:
            if (self.prox_linha_macro != macro_linha or self.prox_coluna_macro != macro_coluna) and not tabuleiro_cheio(self.tabuleiros_menores[self.prox_linha_macro][self.prox_coluna_macro]) and self.tabuleiro_maior[self.prox_linha_macro][self.prox_coluna_macro] == ' ':
                messagebox.showinfo("Movimento inválido", "Você deve jogar no tabuleiro designado!")
                return

        if self.tabuleiros_menores[macro_linha][macro_coluna][micro_linha][micro_coluna] != ' ':
            messagebox.showinfo("Movimento inválido", "Essa célula já está ocupada!")
            return

        # Atualiza o tabuleiro menor e o botão correspondente
        self.tabuleiros_menores[macro_linha][macro_coluna][micro_linha][micro_coluna] = self.jogador_atual
        self.buttons[macro_linha * 3 + micro_linha][macro_coluna * 3 + micro_coluna].config(text=self.jogador_atual)

        # Verifica se o jogador venceu o tabuleiro menor
        if verificar_vitoria(self.tabuleiros_menores[macro_linha][macro_coluna], self.jogador_atual):
            self.tabuleiro_maior[macro_linha][macro_coluna] = self.jogador_atual
            for child in self.frames[macro_linha][macro_coluna].winfo_children():
                child.destroy()
            label = tk.Label(self.frames[macro_linha][macro_coluna], text=self.jogador_atual, font=("Helvetica", 24), bg='white')
            label.pack(expand=True, fill="both")
        # Verifica se houve empate no tabuleiro menor
        elif tabuleiro_cheio(self.tabuleiros_menores[macro_linha][macro_coluna]):
            self.tabuleiro_maior[macro_linha][macro_coluna] = 'V'
            for child in self.frames[macro_linha][macro_coluna].winfo_children():
                child.destroy()
            label = tk.Label(self.frames[macro_linha][macro_coluna], text='V', font=("Helvetica", 24), bg='white')
            label.pack(expand=True, fill="both")

        # Verifica se o jogador venceu o jogo maior
        if verificar_vitoria(self.tabuleiro_maior, self.jogador_atual):
            messagebox.showinfo("Vitória!", f"Jogador {self.jogador_atual} venceu o jogo!")
            self.root.quit()

        # Atualiza para o próximo jogador
        self.prox_linha_macro, self.prox_coluna_macro = micro_linha, micro_coluna

        # No modo avançado, se o próximo tabuleiro já estiver ganho, o jogador que venceu escolhe o próximo
        if self.modo_avancado and self.tabuleiro_maior[self.prox_linha_macro][self.prox_coluna_macro] != ' ':
            if self.tabuleiro_maior[self.prox_linha_macro][self.prox_coluna_macro] == self.jogador_atual:
                self.escolher_proximo_tabuleiro()
            else:
                self.prox_linha_macro = -1
                self.prox_coluna_macro = -1
        elif tabuleiro_cheio(self.tabuleiros_menores[self.prox_linha_macro][self.prox_coluna_macro]):
            self.prox_linha_macro = -1
            self.prox_coluna_macro = -1

        self.jogador_atual = 'O' if self.jogador_atual == 'X' else 'X'
        self.atualizar_destacamento()

    def escolher_proximo_tabuleiro(self):
        # Função para permitir que o jogador que ganhou o tabuleiro escolha o próximo
        escolha_popup = tk.Toplevel(self.root)
        escolha_popup.title("Escolha o Próximo Tabuleiro")
        escolha_popup.geometry("300x200")
        tk.Label(escolha_popup, text=f"{self.jogador_atual}, escolha o próximo tabuleiro menor para jogar:", font=("Helvetica", 12)).pack(pady=10)

        frame_botoes = tk.Frame(escolha_popup)
        frame_botoes.pack(fill="both", expand=True)

        for i in range(3):
            for j in range(3):
                if self.tabuleiro_maior[i][j] == ' ' and not tabuleiro_cheio(self.tabuleiros_menores[i][j]):
                    btn = tk.Button(frame_botoes, text=f"({i}, {j})", font=("Helvetica", 12),
                                    command=lambda x=i, y=j: self.definir_proximo_tabuleiro(escolha_popup, x, y))
                    btn.grid(row=i, column=j, padx=5, pady=5, sticky="nsew")

        # Configurar pesos para as linhas e colunas do frame_botoes
        for i in range(3):
            frame_botoes.grid_rowconfigure(i, weight=1)
            frame_botoes.grid_columnconfigure(i, weight=1)

    def definir_proximo_tabuleiro(self, popup, linha, coluna):
        # Define o próximo tabuleiro a ser jogado
        self.prox_linha_macro = linha
        self.prox_coluna_macro = coluna
        popup.destroy()
        self.atualizar_destacamento()

    def atualizar_destacamento(self):
        # Remove destaque de todos os frames
        for linha in range(3):
            for coluna in range(3):
                self.frames[linha][coluna].config(bg='black')

        # Atualiza o rótulo da jogada
        if self.prox_linha_macro == -1:
            self.label_jogada.config(text=f"Jogada de: {self.jogador_atual} (Escolha livre)")
            # Destaca todos os tabuleiros menores disponíveis
            for linha in range(3):
                for coluna in range(3):
                    if self.tabuleiro_maior[linha][coluna] == ' ' and not tabuleiro_cheio(self.tabuleiros_menores[linha][coluna]):
                        self.frames[linha][coluna].config(bg='lightgreen')
        else:
            self.label_jogada.config(text=f"Jogada de: {self.jogador_atual}")

            # Destaca o próximo tabuleiro menor se necessário
            if self.prox_linha_macro != -1 and self.prox_coluna_macro != -1:
                self.frames[self.prox_linha_macro][self.prox_coluna_macro].config(bg='lightgreen')


if __name__ == "__main__":
    root = tk.Tk()
    game = VelhaDasVelhas(root)
    root.mainloop()