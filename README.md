# RaBisKos

> Sistema para confecção colaborativa de quadros interativos

A execução do sistema ocorre através do Makefile construído 

```sh 
up:
	xhost +local:docker
	$(COMPOSE) up
down:
	$(COMPOSE) down

upd:
	xhost +local:docker
	$(COMPOSE) up -d

mais_cliente:
	$(COMPOSE) run --rm $(CLIENTE)

mais_cliente_d:
	$(COMPOSE) run -d --rm $(CLIENTE)

menos_orfaos:
	$(COMPOSE) down --remove-orphans

down_total: down
	$(MAKE) menos_orfaos
```

## Como usar?
- `make up` -> inicia a aplicação (construção das imagens, execução dos containers, criação do banco, start no servidor e cliente)
    - Nessa etapa apenas uma instância de cliente é inicializada
- `make upd` -> faz o mesmo que o `make up`, mas sem o log do docker
- `make mais_cliente` -> executa mais instâncias de clientes na sessão do terminal 
- `make mais_cliente_d` -> mesmo funcionamento do make mais_cliente, porém 'detached'
- `make down` -> 'desliga' o que foi construído no `make up`
    - contudo, instâncias extras de clientes (criadas a partir de `make mais_cliente` ou `make mais_cliente_d`) ainda mantém alguns recursos ativos após a execuçãod este comando 
- `make menos_orfaos` -> libera os recursos restantes que não foram desligados pelo `make down`
- `make down_total` -> executa `make down` e `make down_total` em sequência

### Como rabiscar
Ao iniciar a aplicação temos a tela de login:
<img width="1911" height="916" alt="image" src="https://github.com/user-attachments/assets/b31c156e-da82-48c0-b57a-845eb0578242" />

Caso o usuário não tenha cadastro basta selecionar a opção __Criar nova conta__, isto o direcionará para a tela de registro:
<img width="1911" height="916" alt="image" src="https://github.com/user-attachments/assets/7290ebdc-6736-4bcb-a69e-4b4effa7c4c9" />

Consecutivamente, após entrar com suas credenciais poderá realizar seu login com estas.

![#f03c15](https://placehold.co/15x15/f03c15/f03c15.png)  `Note que a quantidade de entradas no registro é diferente da quantidade de entradas no login`

O login permite duas formas de acesso:
1. Usuário 'loga' e cria seu próprio quadro em branco
2. Uusário 'loga' em um quadro criado previamente ao inserir o código da sala no login

Dentro de um quadro, o usuário tem acesso ao que é apresentado abaixo:
<img width="1911" height="916" alt="image" src="https://github.com/user-attachments/assets/bf760a38-4203-46ba-81dd-a21c2095bd17" />

Assim, ele pode:
- Limpar o quadro (remove todos os elementos rabiscados sobre ele)
- Interagir com diferentes componentes
	- Inserir formas, setas, texto e desenhar (opção padrão)
 		- Ao definir qual componente será manipulado, pode-se selecionar entre diferentes cores usando as teclas:
   			- 0: ![black](https://placehold.co/15x15/black/black.png) preto (default)
      		- 1: ![red](https://placehold.co/15x15/red/red.png) vermelho
        	- 2: ![blue](https://placehold.co/15x15/blue/blue.png) azul
         	- 3: ![verde](https://placehold.co/15x15/green/green.png) verde
 	- Selecionar elementos no quadro
  		- Selecionando um elemento é possível: mudar sua cor (teclas 0,1,2 e 3), arrastá-lo pelo quadro ou excluí-lo (tecla backspace ou delete) 	   
- Informar a outros usuários o id da sala para que outros usuários possam desenhar no mesmo quadro

## Exemplo de quadro RaBisKado
<img width="1911" height="994" alt="image" src="https://github.com/user-attachments/assets/2090a4db-04fb-4160-966d-e8f601a1aeae" />
