import tkinter as tk
from cliente_rede import ClienteRede
from cliente_interface import InterfaceChat

IP_SERVIDOR = "10.144.169.139"
PORTA_SERVIDOR = 9000

if __name__ == "__main__":
    janela = tk.Tk()

    rede = ClienteRede(IP_SERVIDOR, PORTA_SERVIDOR)
    app = InterfaceChat(janela, rede)

    janela.mainloop()