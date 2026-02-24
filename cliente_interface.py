import tkinter as tk
from tkinter import messagebox, scrolledtext


class JanelaConversa:
    def __init__(self, janela_principal, rede, destinatario, dados_destino, interface):
        self.rede = rede
        self.destinatario = destinatario
        self.dados_destino = dados_destino
        self.interface = interface

        self.janela = tk.Toplevel(janela_principal)
        self.janela.title(f"Conversa com {destinatario}")
        self.janela.geometry("400x400")
        self.janela.protocol("WM_DELETE_WINDOW", self.ao_fechar)

        self.area = scrolledtext.ScrolledText(self.janela, state="disabled")
        self.area.pack(fill="both", expand=True)

        frame_envio = tk.Frame(self.janela)
        frame_envio.pack(fill="x")

        self.entrada = tk.Entry(frame_envio)
        self.entrada.pack(side="left", fill="x", expand=True)
        self.entrada.bind("<Return>", lambda e: self.enviar())

        tk.Button(frame_envio, text="Enviar", command=self.enviar).pack(side="right")

    def enviar(self):
        texto = self.entrada.get()
        if not texto:
            return

        try:
            self.rede.enviar_mensagem(
                self.dados_destino["ip"],
                self.dados_destino["porta"],
                texto
            )

            self.exibir_mensagem("Você", texto)

        except Exception as erro:
            messagebox.showerror("Erro", str(erro))

        self.entrada.delete(0, tk.END)

    def exibir_mensagem(self, remetente, texto):
        self.area.config(state="normal")
        self.area.insert(tk.END, f"[{remetente}]: {texto}\n")
        self.area.config(state="disabled")
        self.area.see(tk.END)

    def ao_fechar(self):
        if self.destinatario in self.interface.conversas_abertas:
            del self.interface.conversas_abertas[self.destinatario]
        self.janela.destroy()


class InterfaceChat:

    def __init__(self, janela, rede):
        self.janela = janela
        self.rede = rede
        self.usuarios = {}
        self.conversas_abertas = {}

        self.janela.title("Chat P2P")
        self.janela.geometry("400x400")

        self.criar_tela_login()

    def criar_tela_login(self):
        self.frame_login = tk.Frame(self.janela, pady=80)
        self.frame_login.pack()

        tk.Label(self.frame_login, text="Apelido").pack()
        self.entrada_apelido = tk.Entry(self.frame_login)
        self.entrada_apelido.pack()

        tk.Label(self.frame_login, text="Porta P2P").pack()
        self.entrada_porta = tk.Entry(self.frame_login)
        self.entrada_porta.pack()

        tk.Button(self.frame_login, text="Conectar", command=self.conectar).pack(pady=10)

    def conectar(self):
        apelido = self.entrada_apelido.get()
        porta = self.entrada_porta.get()

        try:
            resposta = self.rede.conectar(apelido, porta)

            if resposta["status"] == "ok":
                self.rede.iniciar_escuta(self.mensagem_recebida)
                self.criar_tela_principal()
            else:
                messagebox.showerror("Erro", resposta["mensagem"])

        except Exception as erro:
            messagebox.showerror("Erro", str(erro))

    def criar_tela_principal(self):
        self.frame_login.destroy()

        self.frame_principal = tk.Frame(self.janela)
        self.frame_principal.pack(fill="both", expand=True)

        tk.Button(self.frame_principal, text="Atualizar Lista", command=self.atualizar_lista).pack()

        self.lista = tk.Listbox(self.frame_principal)
        self.lista.pack(fill="both", expand=True)
        self.lista.bind("<Double-Button-1>", self.abrir_conversa)

        self.atualizar_lista()

    def atualizar_lista(self):
        self.usuarios = self.rede.obter_lista_usuarios()
        self.lista.delete(0, tk.END)

        for usuario in self.usuarios:
            if usuario != self.rede.apelido:
                self.lista.insert(tk.END, usuario)

    def abrir_conversa(self, evento):
        selecao = self.lista.curselection()
        if not selecao:
            return

        destinatario = self.lista.get(selecao[0])
        dados = self.usuarios[destinatario]

        if destinatario not in self.conversas_abertas:
            self.conversas_abertas[destinatario] = JanelaConversa(
            self.janela,
            self.rede,
            destinatario,
            dados,
            self
        )

    def mensagem_recebida(self, remetente, texto):
        self.janela.after(0, self._abrir_ou_exibir, remetente, texto)

    def _abrir_ou_exibir(self, remetente, texto):
        if remetente not in self.conversas_abertas:
            dados = self.usuarios.get(remetente)
            if dados:
                self.conversas_abertas[remetente] = JanelaConversa(
                    self.janela,
                    self.rede,
                    remetente,
                    dados,
                    self
                )

        if remetente in self.conversas_abertas:
            self.conversas_abertas[remetente].exibir_mensagem(remetente, texto)