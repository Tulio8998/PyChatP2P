# PyChat – Chat P2P com Servidor Central

## 📋 Requisitos
- Python 3.6 ou superior (bibliotecas padrão: `socket`, `threading`, `json`, `tkinter`)

## 🚀 Como executar

### 1. Configurar o IP do servidor
No arquivo `main.py`, altere a variável `IP_SERVIDOR` para o endereço IP da máquina onde o servidor será executado.  
Exemplo:
```python
IP_SERVIDOR = "192.168.1.100"
PORTA_SERVIDOR = 9000
```

### 2. Iniciar o servidor central
O servidor deve estar rodando antes dos clientes.

```bash
python servidor.py
```

Por padrão, ele escuta em `0.0.0.0:9000`.

### 3. Iniciar um cliente
```bash
python main.py
```
Uma janela será aberta. Informe:
- **Apelido** (nome único)
- **Porta P2P** (porta onde este cliente receberá mensagens de outros usuários; ex.: 5000, 5001...)

Clique em **Conectar**.

### 4. Usar o chat
- Após conectar, a lista de usuários online será exibida.
- Clique em **Atualizar Lista** para recarregar.
- Dê um duplo clique em um nome para abrir uma conversa.
- Digite a mensagem e pressione Enter ou clique em **Enviar**.
- Mensagens recebidas abrem automaticamente uma nova janela de conversa.

## ⚙️ Observações
- O servidor gerencia apenas o registro e a lista de usuários. As mensagens são trocadas diretamente entre os clientes (P2P).
- Cada mensagem P2P abre e fecha uma nova conexão TCP.
- Para testar em uma única máquina, use portas diferentes para cada cliente (ex.: 5000, 5001). O IP será `127.0.0.1`.

## 🛑 Encerrando
- Feche as janelas dos clientes para desconectar.
- O servidor pode ser interrompido com `Ctrl+C` no terminal.

