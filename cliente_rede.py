import socket
import threading
import json

class ClienteRede:

    def __init__(self, ip_servidor, porta_servidor):
        self.ip_servidor = ip_servidor
        self.porta_servidor = porta_servidor

        self.apelido = ""
        self.porta_local = 0
        self.socket_servidor = None
        self.callback_mensagem = None

    #CONEXAO COM SERVIDOR CENTRAL

    def conectar(self, apelido, porta_local):
        self.apelido = apelido
        self.porta_local = int(porta_local)

        self.socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_servidor.connect((self.ip_servidor, self.porta_servidor))

        mensagem = {
            "tipo": "registro",
            "apelido": self.apelido,
            "porta": self.porta_local
        }

        self.socket_servidor.send(json.dumps(mensagem).encode())
        resposta = json.loads(self.socket_servidor.recv(2048).decode())

        return resposta

    def obter_lista_usuarios(self):
        self.socket_servidor.send(json.dumps({"tipo": "lista"}).encode())
        return json.loads(self.socket_servidor.recv(2048).decode())

    #ENVIO P2P

    def enviar_mensagem(self, ip_destino, porta_destino, texto):
        socket_p2p = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_p2p.connect((ip_destino, porta_destino))

        mensagem = {
            "remetente": self.apelido,
            "texto": texto
        }

        socket_p2p.send(json.dumps(mensagem).encode())
        socket_p2p.close()

    #SERVIDOR P2P

    def iniciar_escuta(self, callback):
        self.callback_mensagem = callback
        thread = threading.Thread(target=self._servidor_p2p, daemon=True)
        thread.start()

    def _servidor_p2p(self):
        servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        servidor.bind(("0.0.0.0", self.porta_local))
        servidor.listen()

        while True:
            conexao, endereco = servidor.accept()
            dados = conexao.recv(2048)

            mensagem = json.loads(dados.decode())

            if self.callback_mensagem:
                self.callback_mensagem(
                    mensagem["remetente"],
                    mensagem["texto"]
                )

            conexao.close()