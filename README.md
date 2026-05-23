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
---
- `make up` -> inicia a aplicação (construção das imagens, execução dos containers, criação do banco, start no servidor e cliente)
    - Nessa etapa apenas uma instância de cliente é inicializada
- `make upd` -> faz o mesmo que o `make up`, mas sem o log do docker
- `make mais_cliente` -> executa mais instâncias de clientes na sessão do terminal 
- `make mais_cliente_d` -> mesmo funcionamento do make mais_cliente, porém 'detached'
- `make down` -> 'desliga' o que foi construído no `make up`
    - contudo, instâncias extras de clientes (criadas a partir de `make mais_cliente` ou `make mais_cliente_d`) ainda mantém alguns recursos ativos após a execuçãod este comando 
- `make menos_orfaos` -> libera os recursos restantes que não foram desligados pelo `make down`
- `make down_total` -> executa `make down` e `make down_total` em sequência
