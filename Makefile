# Makefile for Docker and Snowpark Container Services deployment

# Variables (will be set from environment or command line)
SNOWFLAKE_ACCOUNT ?= beikxlh-multimedios
SNOWFLAKE_DATABASE ?= db_analytics_dev
SNOWFLAKE_SCHEMA ?= sch_dir_tec
IMAGE_REPO ?= $(SNOWFLAKE_ACCOUNT).registry.snowflakecomputing.com/$(SNOWFLAKE_DATABASE)/$(SNOWFLAKE_SCHEMA)/streamlit_app_repo
IMAGE_TAG ?= latest
APP_NAME = streamlit-radio-app

# Local development
.PHONY: build-local
build-local:
	docker build -t $(APP_NAME):$(IMAGE_TAG) .

.PHONY: run-local
run-local: build-local
	docker run --rm -p 8501:8501 --env-file .env $(APP_NAME):$(IMAGE_TAG)

.PHONY: run-compose
run-compose:
	docker-compose up --build

.PHONY: stop-compose
stop-compose:
	docker-compose down

# Snowflake deployment
.PHONY: build-snowflake
build-snowflake:
	docker build -t $(IMAGE_REPO)/$(APP_NAME):$(IMAGE_TAG) .

.PHONY: push-snowflake
push-snowflake: build-snowflake
	docker push $(IMAGE_REPO)/$(APP_NAME):$(IMAGE_TAG)

.PHONY: login-snowflake
login-snowflake:
	docker login $(SNOWFLAKE_ACCOUNT).registry.snowflakecomputing.com -u $(SNOWFLAKE_USER)

# Utility commands
.PHONY: clean
clean:
	docker system prune -f
	docker image prune -f

.PHONY: logs
logs:
	docker-compose logs -f

.PHONY: shell
shell:
	docker run --rm -it --env-file .env $(APP_NAME):$(IMAGE_TAG) /bin/bash