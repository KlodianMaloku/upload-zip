SERVICE_NAME=backend-api

up-deps:
	docker-compose up -d postgres sonarqube qdrant
# up:
#     docker-compose down
# 	docker-compose up -d ${SERVICE_NAME}