SERVIDOR=servidor
CLIENTE=cliente 
COMPOSE=docker compose

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
