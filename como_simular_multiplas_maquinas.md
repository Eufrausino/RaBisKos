# Como Simular o RaBisKos em Múltiplas Máquinas (ou WSL + Windows)

Este guia orienta como configurar e executar o sistema distribuído **RaBisKos** em computadores diferentes (ou simulando com o Windows Host e a máquina virtual do WSL) para que as telas de desenho se sincronizem em tempo real usando o middleware Pyro5.

---

## Cenário e Arquitetura

* **Máquina A (Servidora + Cliente 1):** Onde rodarão o **Name Server (Pyro5)**, o **Servidor** principal e opcionalmente uma instância de **Cliente**. Pode ser o seu terminal Linux/WSL ou uma máquina física A.
* **Máquina B (Cliente 2):** Uma segunda máquina (física ou o Windows Host) que rodará apenas o **Cliente** e se conectará à Máquina A.

---

## 📌 Passo 1: Preparação na Máquina A (Servidor e Name Server)

A Máquina A precisa executar o Name Server e o Servidor de forma que eles fiquem visíveis na rede para outras máquinas.

### 1.1. Obter o IP de Rede da Máquina A
Você precisará do IP local da Máquina A para que a Máquina B consiga se conectar.
* **No Linux / WSL:**
  ```bash
  ip addr show eth0 | grep inet
  ```
  *(Identifique o IP, por exemplo: `172.25.214.2` ou `192.168.1.100`)*
* **No Windows:**
  ```cmd
  ipconfig
  ```
*(Vamos nos referir a este IP como `<IP_DA_MAQUINA_A>`)*

### 1.2. Iniciar o Name Server (Pyro5)
Abra um terminal na Máquina A e inicie o Name Server escutando em todas as interfaces de rede (`0.0.0.0`):
```bash
pyro5-ns -n 0.0.0.0
```
> **Nota:** O terminal deve exibir `NS running on 0.0.0.0:9090`.

### 1.3. Iniciar o Servidor do RaBisKos
Abra um **segundo terminal** na Máquina A, defina a variável `SERVIDOR_HOST` com o IP real da Máquina A e inicie o servidor:
* **No Linux / WSL:**
  ```bash
  export PYTHONPATH=$(pwd)
  export NS_HOST=127.0.0.1
  export NS_PORT=9090
  export SERVIDOR_HOST=<IP_DA_MAQUINA_A>
  python3 servidor/main_servidor.py
  ```
* **No Windows:**
  ```powershell
  $env:PYTHONPATH="."
  $env:NS_HOST="127.0.0.1"
  $env:NS_PORT="9090"
  $env:SERVIDOR_HOST="<IP_DA_MAQUINA_A>"
  python servidor/main_servidor.py
  ```

---

## 📌 Passo 2: Executar o Cliente 1 na Máquina A

Para ter a primeira tela de teste ativa:
Abra um **terceiro terminal** na Máquina A e execute:
* **No Linux / WSL:**
  ```bash
  export NS_HOST=localhost
  export NS_PORT=9090
  python3 cliente/main_cliente.py
  ```
* **No Windows:**
  ```powershell
  $env:NS_HOST="localhost"
  $env:NS_PORT="9090"
  python cliente/main_cliente.py
  ```

---

## 📌 Passo 3: Executar o Cliente 2 na Máquina B (Outra Máquina ou Windows Host)

Agora, na outra máquina física (ou no terminal do seu Windows Host se estiver simulando com WSL):

### 3.1. Instalar as dependências
Certifique-se de que a Máquina B tem o Python instalado e execute no terminal:
```bash
pip install PyQt6 Pyro5
```

### 3.2. Iniciar o Cliente apontando para a Máquina A
Inicie o cliente informando o IP da Máquina A nas variáveis de ambiente:
* **No Windows (PowerShell):**
  ```powershell
  $env:NS_HOST="<IP_DA_MAQUINA_A>"
  $env:NS_PORT="9090"
  python cliente/main_cliente.py
  ```
* **No Linux / macOS:**
  ```bash
  export NS_HOST="<IP_DA_MAQUINA_A>"
  export NS_PORT="9090"
  python3 cliente/main_cliente.py
  ```

---

## 📌 Passo 4: Sincronização dos Quadros

Com as duas telas abertas (uma na Máquina A e outra na Máquina B):

1. **Na Tela do Cliente 1 (Máquina A):**
   * Vá em **Criar nova conta** e crie um usuário (ex: `user_a`).
   * Faça login. O sistema gerará um quadro interativo em branco.
   * Copie o código da **Sala** que aparece no topo da janela.

2. **Na Tela do Cliente 2 (Máquina B):**
   * Vá em **Criar nova conta** e crie outro usuário (ex: `user_b`).
   * Faça login inserindo o nome de usuário, senha e o **código da Sala** copiado no passo anterior.

3. **Interação:**
   * Qualquer desenho, forma ou alteração feita na tela de uma das máquinas será sincronizada instantaneamente na outra!

---

## ⚠️ Solução de Problemas: `ConnectionClosedError` no Windows

Se ao fazer login ou entrar em uma sala o cliente crashar com o erro:
```
Pyro5.errors.ConnectionClosedError: receiving: not enough data
```

### Causa
O cliente Pyro5 registra um Daemon local para receber callbacks do servidor. O IP desse Daemon é obtido via `socket.gethostbyname(socket.gethostname())`. Em máquinas Windows com **WSL, Hyper-V ou Docker Desktop** instalados, esse comando retorna o IP do **adaptador de rede virtual** (ex: `172.25.208.1`) em vez do IP real da rede local (ex: `192.168.0.106`).

O servidor tenta enviar o callback para o IP virtual, que não é acessível pela rede, e a conexão é encerrada.

### Diagnóstico
Verifique qual IP o Python está resolvendo:
```powershell
python -c "import socket; print(socket.gethostbyname(socket.gethostname()))"
```
Se o resultado **não** for o IP da sua rede local (ex: `192.168.x.x`), aplique a solução abaixo.

### Alterar a métrica do adaptador de rede (Recomendada)
Dê prioridade ao adaptador Wi-Fi/Ethernet real para que o Windows resolva o hostname para o IP correto. Execute como **Administrador**:
```powershell
# Descubra o ifIndex do seu adaptador real (Wi-Fi ou Ethernet)
Get-NetAdapter | Where-Object { $_.Status -eq 'Up' } | Select-Object Name, ifIndex

# Defina a métrica mais baixa (maior prioridade) para o adaptador real
Set-NetIPInterface -InterfaceIndex <ifIndex_do_Wi-Fi_ou_Ethernet> -InterfaceMetric 10
```

### Verificação
Após aplicar a solução, confirme que o IP está correto:
```powershell
python -c "import socket; print(socket.gethostbyname(socket.gethostname()))"
# Deve retornar o IP da sua rede local (ex: 192.168.0.106)
```
