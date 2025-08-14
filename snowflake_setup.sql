-- Snowpark Container Services Setup Script
-- Run these commands in Snowflake to prepare for container deployment

-- 1. Use your existing database and schema
USE DATABASE DB_ANALYTICS_DEV;
USE SCHEMA SCH_DIR_TEC;

-- 2. Create image repository
CREATE IMAGE REPOSITORY IF NOT EXISTS streamlit_app_repo;

-- 3. Grant privileges on image repository
GRANT READ, WRITE ON IMAGE REPOSITORY streamlit_app_repo TO ROLE ACCOUNTADMIN;

-- 4. Create compute pool for container services
CREATE COMPUTE POOL IF NOT EXISTS streamlit_compute_pool
  MIN_NODES = 1
  MAX_NODES = 2
  INSTANCE_FAMILY = CPU_X64_XS
  AUTO_SUSPEND_SECS = 3600;

-- 5. Grant usage on compute pool
GRANT USAGE, MONITOR ON COMPUTE POOL streamlit_compute_pool TO ROLE ACCOUNTADMIN;

-- 6. Check compute pool status
SHOW COMPUTE POOLS;

-- 7. Check image repository
SHOW IMAGE REPOSITORIES;

-- 8. Create service specification (run after pushing Docker image)
CREATE SERVICE streamlit_radio_service
  IN COMPUTE POOL streamlit_compute_pool
  FROM SPECIFICATION $$
    spec:
      containers:
      - name: streamlit-app
        image: beikxlh-multimedios.registry.snowflakecomputing.com/db_analytics_dev/sch_dir_tec/streamlit_app_repo/streamlit-radio-app:latest
        env:
          SNOWFLAKE_ACCOUNT: BEIKXLH-MULTIMEDIOS
          SNOWFLAKE_USER: US_ECALDERONG
          SNOWFLAKE_PASSWORD: Wdtxm-13513926
          SNOWFLAKE_WAREHOUSE: WH_DIR_SYS
          SNOWFLAKE_DATABASE: DB_ANALYTICS_DEV
          SNOWFLAKE_SCHEMA: SCH_DIR_TEC
          SNOWFLAKE_ROLE: ACCOUNTADMIN
        resources:
          requests:
            memory: 1Gi
            cpu: 0.5
          limits:
            memory: 2Gi
            cpu: 1.0
      endpoints:
      - name: streamlit
        port: 8501
        public: true
  $$;

-- 9. Monitor service (after creation)
-- SHOW SERVICES;
-- SELECT SYSTEM$GET_SERVICE_STATUS('streamlit_radio_service');
-- SHOW ENDPOINTS IN SERVICE streamlit_radio_service;