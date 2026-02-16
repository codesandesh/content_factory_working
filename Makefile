.PHONY: help start stop logs status

help:
	@echo "🎬 Content Factory Commands"
	@echo "  make start   - Start containers"
	@echo "  make stop    - Stop containers"
	@echo "  make logs    - View n8n logs"
	@echo "  make status  - Check status"

start:
	docker compose up -d

stop:
	docker compose down

logs:
	docker compose logs -f n8n

status:
	docker compose ps
