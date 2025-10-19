import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from pathlib import Path
from funcoes_requisicao import transcrever_imagem, processar_texto
from clonar_pasta_modelo import executar_clonagem_completa
from modificar_laudo import gerar_laudo_markdown
import os
import re
import shutil
import json
import subprocess

class AutomacaoLaudosGUI:

    def __init__(self, root):

        self.root = root

        self.root.title("Automação de Laudos v3")

        self.root.geometry("700x600")



        # Variáveis para armazenar os caminhos e informações

        self.caminho_imagem = ""

        self.caminho_pasta = ""

        self.caminho_pasta_destino = ""  # Variável para armazenar o caminho da pasta de destino

        self.caminho_caso_atual = None # Guarda o caminho da pasta do caso atual

        self.informacoes_requisicao = {}

        self.modelo_dispositivo = ""

        

        # --- Widgets para campos editáveis ---

        self.info_frame = None

        self.info_entries = {}

        # -----------------------------------------



        # Carregar última pasta utilizada (se existir)

        self.carregar_ultima_pasta()



        # --- Estrutura principal com Canvas e Scrollbar ---
        canvas = tk.Canvas(root)
        scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")


        # --- 1. Frame de Seleção e Processamento da Imagem ---

        image_frame = tk.LabelFrame(scrollable_frame, text="Passo 1: Processar Requisição")

        image_frame.pack(pady=10, padx=10, fill=tk.X)



        # Botão para selecionar imagem

        self.btn_mudar_imagem = tk.Button(image_frame, text="Selecionar Imagem da Requisição", command=self.mudar_imagem)

        self.btn_mudar_imagem.pack(side=tk.LEFT, padx=5, pady=5)



        # Botão para processar imagem

        self.btn_processar_imagem = tk.Button(image_frame, text="Processar Imagem", command=self.processar_arquivo)

        self.btn_processar_imagem.pack(side=tk.LEFT, padx=5, pady=5)

        

        # Label para mostrar caminho da imagem

        self.caminho_imagem_label = tk.Label(image_frame, text="Nenhuma imagem selecionada", wraplength=680)

        self.caminho_imagem_label.pack(pady=5, padx=10)



        # --- 2. Frame de Resultados do OCR e Edição ---

        self.ocr_results_frame = tk.LabelFrame(scrollable_frame, text="Passo 2: Verificar e Corrigir Informações")

        self.ocr_results_frame.pack(pady=10, padx=10, fill=tk.X)

        tk.Label(self.ocr_results_frame, text="Aguardando processamento da imagem...").pack(pady=20)



        # --- 3. Frame de Clonagem de Pasta ---

        clone_frame = tk.LabelFrame(scrollable_frame, text="Passo 3: Criar Pasta do Laudo")

        clone_frame.pack(pady=10, padx=10, fill=tk.X)



        # Botão para selecionar a pasta de origem

        self.btn_selecionar_pasta = tk.Button(clone_frame, text="Selecionar Pasta de Origem", command=self.selecionar_pasta)

        self.btn_selecionar_pasta.pack(side=tk.LEFT, padx=5, pady=5)



        # Botão para clonar pasta

        self.btn_clonar_pasta = tk.Button(clone_frame, text="Clonar Pasta", command=self.clonar_pasta)

        self.btn_clonar_pasta.pack(side=tk.LEFT, padx=5, pady=5)



        # --- 4. Frame de Ações Finais ---

        laudo_frame = tk.LabelFrame(scrollable_frame, text="Passo 4: Ações Finais")
        laudo_frame.pack(pady=10, padx=10, fill=tk.X)

        # Frame para os botões de ação
        action_button_frame = tk.Frame(laudo_frame)
        action_button_frame.pack(pady=5)

        # Botão para Gerar o Laudo
        self.btn_gerar_laudo = tk.Button(action_button_frame, text="Gerar Laudo", command=self.abrir_janela_laudo, state=tk.DISABLED)
        self.btn_gerar_laudo.pack(side=tk.LEFT, padx=10)

        # Botão para Abrir o Terminal Gemini
        self.btn_abrir_terminal = tk.Button(action_button_frame, text="Abrir Terminal Gemini", command=self.abrir_terminal_gemini, state=tk.DISABLED)
        self.btn_abrir_terminal.pack(side=tk.LEFT, padx=10)



    def mudar_imagem(self):

        try:

            novo_caminho_imagem = filedialog.askopenfilename(filetypes=[("Imagem", "*.jpg;*.jpeg;*.png")])

            if novo_caminho_imagem:

                self.caminho_imagem = novo_caminho_imagem

                self.caminho_imagem_label.config(text=self.caminho_imagem)

                messagebox.showinfo("Imagem Selecionada", "A imagem foi selecionada com sucesso.")

            else:

                messagebox.showwarning("Aviso", "Nenhuma imagem foi selecionada.")

        except Exception as e:

            messagebox.showerror("Erro", f"Erro ao selecionar a imagem: {e}")



    def processar_arquivo(self):

        if not self.caminho_imagem:

            messagebox.showerror("Erro", "Nenhuma imagem foi selecionada.")

            return

        

        try:

            # 1. Carrega os dados padrão do JSON

            with open('dados_padrao.json', 'r', encoding='utf-8') as f:

                dados_base = json.load(f)



            # 2. Transcreve e processa a imagem

            texto_transcrito = transcrever_imagem(self.caminho_imagem)

            info_ocr = processar_texto(texto_transcrito)



            # 3. Atualiza os dados padrão com os dados do OCR

            # Apenas os valores que o OCR encontrou (diferente de "Não encontrado") irão sobrescrever

            for chave, valor in info_ocr.items():

                if valor and valor != "Não encontrado":

                    dados_base[chave] = valor

            

            self.informacoes_requisicao = dados_base



            # 4. Exibe o resultado combinado para edição

            self.display_editable_info()



        except Exception as e:

            messagebox.showerror("Erro", f"Erro ao processar a imagem: {e}")



    def display_editable_info(self):
        # Destruir o frame antigo se ele existir
        if self.info_frame:
            self.info_frame.destroy()

        # --- Frame principal para a área de resultados ---
        self.info_frame = tk.Frame(self.ocr_results_frame)
        self.info_frame.pack(pady=5, padx=5, fill=tk.BOTH, expand=True)

        # Adiciona um título
        title_label = tk.Label(self.info_frame, text="Informações Extraídas (edite se necessário)", font=("Helvetica", 10, "bold"))
        title_label.pack(pady=5)

        # --- Canvas com Scrollbar para os campos de entrada ---
        canvas = tk.Canvas(self.info_frame)
        scrollbar = tk.Scrollbar(self.info_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        # -----------------------------------------------------

        self.info_entries = {}
        # Cria um label e um entry para cada item dentro do frame rolável
        for i, (chave, valor) in enumerate(self.informacoes_requisicao.items()):
            label = tk.Label(scrollable_frame, text=f"{chave}:", anchor="w")
            label.grid(row=i, column=0, sticky="w", padx=5, pady=2)
            
            entry = tk.Entry(scrollable_frame, width=80) # Aumentar a largura para aproveitar o espaço
            entry.grid(row=i, column=1, sticky="ew", padx=5, pady=2)
            entry.insert(0, valor if valor else "")
            
            self.info_entries[chave] = entry

        # Configura a coluna do grid para expandir com a janela
        scrollable_frame.grid_columnconfigure(1, weight=1)

        # --- Botão de Salvar fora da área de rolagem ---
        save_button = tk.Button(self.ocr_results_frame, text="Salvar Correções", command=self.save_corrections)
        save_button.pack(pady=10)



    def save_corrections(self):

        if not self.info_entries:

            messagebox.showwarning("Aviso", "Nenhuma informação para salvar. Processe uma imagem primeiro.")

            return



        try:

            # Atualiza o dicionário com os valores dos campos de entrada

            for chave, entry_widget in self.info_entries.items():

                self.informacoes_requisicao[chave] = entry_widget.get()

            

            messagebox.showinfo("Sucesso", "Informações corrigidas foram salvas com sucesso!\nAgora você pode prosseguir para clonar a pasta.")

        except Exception as e:

            messagebox.showerror("Erro", f"Erro ao salvar as informações: {e}")



    def selecionar_pasta(self):

        try:

            # Permitir ao usuário selecionar uma nova pasta de origem

            self.caminho_pasta = filedialog.askdirectory(initialdir=self.caminho_pasta_destino or os.getcwd())

            if self.caminho_pasta:

                self.salvar_ultima_pasta(self.caminho_pasta)

                messagebox.showinfo("Pasta Selecionada", f"Pasta de origem selecionada: {self.caminho_pasta}")

            else:

                messagebox.showwarning("Aviso", "Nenhuma pasta foi selecionada.")

        except Exception as e:

            messagebox.showerror("Erro", f"Erro ao selecionar a pasta: {e}")



    def clonar_pasta(self):

        if not self.caminho_pasta:

            messagebox.showerror("Erro", "Nenhuma pasta de origem foi selecionada.")

            return



        if not self.informacoes_requisicao or not self.informacoes_requisicao.get('modelo_dispositivo', '').strip():

            messagebox.showerror("Erro", "O modelo do dispositivo não foi preenchido. Processe uma imagem e preencha o campo antes de clonar.")

            return



        caminho_pasta_destino = filedialog.askdirectory(title="Selecione o diretório de DESTINO para a nova pasta do laudo")

        if not caminho_pasta_destino:

            messagebox.showwarning("Aviso", "Nenhum diretório de destino foi selecionado.")

            return



        try:

            # A variável `modelo_dispositivo` agora vem do dicionário principal

            modelo_dispositivo = self.informacoes_requisicao.get('modelo_dispositivo', '')



            # Chama a função centralizada que faz todo o trabalho

            caminho_final = executar_clonagem_completa(

                caminho_origem=self.caminho_pasta,

                caminho_destino_base=caminho_pasta_destino,

                info_requisicao=self.informacoes_requisicao,

                modelo_dispositivo=modelo_dispositivo

            )

            # Guarda o caminho do caso atual e ativa os botões de ação

            self.caminho_caso_atual = caminho_final

            self.btn_gerar_laudo.config(state=tk.NORMAL)
            self.btn_abrir_terminal.config(state=tk.NORMAL)



            messagebox.showinfo("Sucesso", f"Processo concluído com sucesso!\n\nNova pasta criada em:\n{caminho_final}")

        except (FileNotFoundError, ValueError, FileExistsError) as e:

            messagebox.showerror("Erro de Validação", str(e))

        except Exception as e:

            messagebox.showerror("Erro Inesperado", f"Ocorreu um erro durante o processo:\n\n{e}")



    def abrir_terminal_gemini(self):
        """Abre o terminal Gemini na pasta do caso atual."""
        if not self.caminho_caso_atual:
            messagebox.showwarning("Aviso", "Nenhuma pasta de caso ativa. Clone uma pasta primeiro.")
            return
        
        try:
            # Constrói o caminho para o script que abre o terminal
            # __file__ se refere a este script (interface.py)
            script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'abrir_terminal_gemini.py')
            
            if not os.path.exists(script_path):
                messagebox.showerror("Erro", f"O script 'abrir_terminal_gemini.py' não foi encontrado no diretório do programa.")
                return

            # Usa Popen para não bloquear a GUI. Passa o caminho do caso como argumento.
            subprocess.Popen(['python', script_path, self.caminho_caso_atual])
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao abrir o terminal Gemini: {e}")



    def abrir_janela_laudo(self):

        json_path = 'dados_padrao.json' # Caminho para o arquivo de dados padrão

        if not os.path.exists(json_path):

            messagebox.showerror("Erro", f"Arquivo de dados padrão '{json_path}' não encontrado.")

            return



        # Carrega os dados do arquivo JSON padrão

        with open(json_path, 'r', encoding='utf-8') as f:

            dados_salvos = json.load(f)



        laudo_window = tk.Toplevel(self.root)

        laudo_window.title("Preencher e Gerar Laudo")

        laudo_window.geometry("800x700")



        canvas = tk.Canvas(laudo_window)

        scrollbar = tk.Scrollbar(laudo_window, orient="vertical", command=canvas.yview)

        scrollable_frame = tk.Frame(canvas)



        scrollable_frame.bind(

            "<Configure>",

            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))

        )



        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set)



        canvas.pack(side="left", fill="both", expand=True)

        scrollbar.pack(side="right", fill="y")



        import configparser

        config = configparser.ConfigParser()

        config.read('config.ini')

        placeholders = config['Placeholders']



        laudo_entries = {}

        # Atualiza os dados padrão com o que veio do OCR, se houver

        dados_para_exibir = dados_salvos.copy()

        dados_para_exibir.update(self.informacoes_requisicao)



        for i, (chave, placeholder_texto) in enumerate(placeholders.items()):

            label = tk.Label(scrollable_frame, text=f"{chave.replace('_', ' ').title()}:")

            label.grid(row=i, column=0, sticky="w", padx=10, pady=5)



            entry = tk.Entry(scrollable_frame, width=100)

            entry.grid(row=i, column=1, sticky="ew", padx=10, pady=5)

            

            entry.insert(0, dados_para_exibir.get(chave, ''))

            

            laudo_entries[chave] = entry



        def salvar_e_gerar():
            # 1. Coleta os dados finais da janela
            dados_finais = {chave: entry.get() for chave, entry in laudo_entries.items()}
            
            # 2. Sobrescreve o arquivo de dados padrão com as novas informações
            try:
                with open(json_path, 'w', encoding='utf-8') as f:
                    json.dump(dados_finais, f, ensure_ascii=False, indent=4)
                print(f"Arquivo de dados padrão '{json_path}' foi atualizado.")
            except Exception as e:
                messagebox.showerror("Erro ao Salvar", f"Não foi possível salvar os dados padrão em '{json_path}':\n{e}", parent=laudo_window)
                return

            # 3. Define o nome sugerido para o arquivo de laudo a partir dos dados da janela
            protocolo = dados_finais.get('protocolo', 'PROTOCOLO')
            dispositivo = dados_finais.get('modelo_dispositivo', 'DISPOSITIVO')
            nome_sugerido = f"Laudo {protocolo} - {dispositivo}.md"

            # 4. Pergunta ao usuário onde salvar o laudo
            caminho_salvar_laudo = filedialog.asksaveasfilename(
                title="Salvar Laudo Markdown Como...",
                initialdir=self.caminho_caso_atual or os.getcwd(), # Sugere a pasta do caso atual
                initialfile=nome_sugerido,
                defaultextension=".md",
                filetypes=[("Markdown files", "*.md"), ("All files", "*.* ")]
            )

            if not caminho_salvar_laudo:
                messagebox.showwarning("Operação Cancelada", "A geração do laudo foi cancelada.", parent=laudo_window)
                return

            # 5. Gera o arquivo de laudo final
            try:
                caminho_template_md = Path('modelo_laudo.md')
                gerar_laudo_markdown(dados_finais, Path(caminho_salvar_laudo), caminho_template_md)
                messagebox.showinfo("Sucesso", f"Laudo gerado e salvo com sucesso em:\n{caminho_salvar_laudo}", parent=laudo_window)
                laudo_window.destroy()
            except Exception as e:
                messagebox.showerror("Erro ao Gerar Laudo", f"Não foi possível gerar o arquivo de laudo:\n{e}", parent=laudo_window)



        btn_salvar_gerar = tk.Button(scrollable_frame, text="Salvar Padrão e Gerar Laudo", command=salvar_e_gerar)

        btn_salvar_gerar.grid(row=len(placeholders), column=0, columnspan=2, pady=20)



    def salvar_ultima_pasta(self, caminho):

        try:

            with open("ultima_pasta.txt", "w") as file:

                file.write(caminho)

        except Exception as e:

            messagebox.showerror("Erro", f"Erro ao salvar a última pasta: {e}")



    def carregar_ultima_pasta(self):

        try:

            if os.path.exists("ultima_pasta.txt"):

                with open("ultima_pasta.txt", "r") as file:

                    self.caminho_pasta_destino = file.read()

        except Exception as e:

            messagebox.showerror("Erro", f"Erro ao carregar a última pasta: {e}")



