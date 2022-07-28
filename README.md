# Atividade de Sistemas Distribuidos (WhatsApp)

## Aluno
### RA: ```759027```
### Nome: ```Iago Elias de Faria Barbosa```

## Objetivos
Interface cli para criação de servidor e client de chat.
A aplicação é dividida em duas partes, acessíveis por uma mesma interface. As partes são:
- Aplicação Proxy/Middleware para a disponibilização de um servidor Pub/Sub.
- Aplicação Cliente que pode se inscrever em um tópico do servidor e enviar mensagens para algum tópico.

## Requisitos
A atividade possuia os seguintes requisitos:
- Utilização de Python
- Utilizar o ZeroMQ para a criação do proxy e do cliente.
- A comunicação deve se basear no padrão Pub/Sub
- A aplicação deve Permitir mais de 3 usuários em um mesmo tópico e máquinas diferentes.

## Instalação

O passo básico da instação é instalar o poetry, que é um assistente para o versionamento e gerenciamento de pacotes e serviços que envolvam módulos, é um wrapper do pip, as instruções podem ser vistas por [aqui](https://python-poetry.org/docs/#osx--linux--bashonwindows-install-instructions), porém o comando está colado abaixo:

### Linux
```bash
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
```

### Windows
```powershell
(Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py -UseBasicParsing).Content | python -
```

Exporte o caminho do executável do poetry para o PATH:
```bash
export PATH=$PATH:$HOME/.poetry/bin
```

Após a instação do poetry, basta executar:

```bash
poetry install
```

Que o pacote estará instalado. <br/>
Para entrar no ambiente virtual onde os pacotes estão instalador, basta executar:

```bash
poetry shell
```

## Uso

Para inicializar o shell, basta rodar o executável:
```sh
./zap
```

A série de comandos disponíveis segue abaixo:
- serve ```:input_port``` ```:output_port```: Serve na rede local o proxy, com a ```input_port``` sendo a porta de entrada para a publicação e ```:output_port``` a porta para inscrição. 
- connect ```:address``` ```:input_port``` ```:output_port```: Se connecta em um proxy, o ```adress``` deve estar no formato tcp://endereço e a porta de entra e saída seguem o mesmo padrão do servidor:
- set_user ```:user_name```: Configura um usuário para aparecer em chats remotos quando o usuário manda uma mensagem.
- enter_topic ```:topic_name```: Se inscreve em um chat.
- exit_topic ```:topic_name```: Se desinscreve em um chat.
- send: ```:topic_name``` ```:message```: Envia uma mensagem para um tópico, com ```mensage``` sendo o conteúdo.
  
Existe também a possibilidade de entrar na aplicação zap utilizando a linha de comando de entrada:

- Entrando com a flag ```-s``` ou ```--serve``` é indicado que se deseja entrar no modo servidor. (Obrigatória a passagem de endereço)
- Entrando com a flag ```-a``` ou ````--address``` é indicado que se deseja estabelecer uma conexão, o valor do endereço deve estar no formato: tcp://{endereço}:{porta de entrada}-{porta de saida}. (Essa opção é obrigatória no modo servidor)
- Entrando com a flag ```-u``` ou ```--user``` é indicado a identificação do usuário.
- Entrando com a flag ```-t``` ou ```--topic``` é indicado que se deseja entrar em um tópico.
  
Exemplo:

### Abrindo um servidor na porta 6001 (para receber de clientes) e 6000 (para enviar para clientes):
```bash
./zap -s -a tcp://locahost:6001-6000
```

### Se conectando em um servidor no localhost porta 6001 (para enviar) e 6000 (para se inscrever) com o usuário aluno e se inscrevendo no tópico aulas:
```bash
./zap -u aluno -t aulas -a tcp://localhost:6001-6000
```

## Forwarding de portas para a LAN:

Basta seguir este [tutorial](https://gist.github.com/stormwild/f464fae904212d4334b3905655a2218c), no caso do uso do WSL. Consultar métodos externos para usar em outros SO's.