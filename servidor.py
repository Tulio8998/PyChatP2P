import socket
import threading
import json

HOST = "0.0.0.0"
PORTA = 9000

usuarios_conectados = {}


def tratar_cliente(conexao, endereco):
    global usuarios_conectados
    apelido_atual = None

    try:
        while True:
            dados = conexao.recv(2048)
            if not dados:
                break

            mensagem = json.loads(dados.decode())

            if mensagem["tipo"] == "registro":
                apelido_atual = mensagem["apelido"]
                porta_p2p = mensagem["porta"]

                if apelido_atual in usuarios_conectados:
                    resposta = {"status": "erro", "mensagem": "Apelido já está em uso."}
                    conexao.send(json.dumps(resposta).encode())
                else:
                    usuarios_conectados[apelido_atual] = {
                        "ip": endereco[0],
                        "porta": porta_p2p
                    }
                    conexao.send(json.dumps({"status": "ok"}).encode())
                    print(f"{apelido_atual} conectado de {endereco[0]}:{porta_p2p}")

            elif mensagem["tipo"] == "lista":
                conexao.send(json.dumps(usuarios_conectados).encode())

    finally:
        if apelido_atual and apelido_atual in usuarios_conectados:
            del usuarios_conectados[apelido_atual]
            print(f"{apelido_atual} desconectou")

        conexao.close()


def iniciar_servidor():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind((HOST, PORTA))
    servidor.listen()
    print(f"Servidor central rodando em {HOST}:{PORTA}")

    while True:
        conexao, endereco = servidor.accept()
        threading.Thread(
            target=tratar_cliente,
            args=(conexao, endereco),
            daemon=True
        ).start()


if __name__ == "__main__":
    iniciar_servidor()