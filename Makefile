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
	$(COMPOSE) logs -f $(CLIENTE)

mais_cliente:
	docker compose run --rm cliente
