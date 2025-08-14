# Snowpark Container Services Deployment Guide

## Quick Start

### Prerequisites
- Docker Desktop installed and running
- Access to Snowflake account `BEIKXLH-MULTIMEDIOS`
- ACCOUNTADMIN role permissions

### Option 1: Automated Deployment (Recommended)
```bash
./deploy.sh
```

### Option 2: Manual Step-by-Step

#### 1. Local Testing
```bash
# Build and test locally
make run-local

# Or with docker-compose
make run-compose

# Access at http://localhost:8501
```

#### 2. Snowflake Setup
Run these SQL commands in Snowflake:
```sql
-- Execute all commands in snowflake_setup.sql
```

#### 3. Deploy to Snowpark
```bash
# Login to Snowflake registry
make login-snowflake

# Build and push image
make push-snowflake
```

#### 4. Create Service
Execute the service creation SQL from `snowflake_setup.sql`

## Configuration Details

### Environment Variables
- **Account**: `BEIKXLH-MULTIMEDIOS`
- **Database**: `DB_ANALYTICS_DEV`
- **Schema**: `SCH_DIR_TEC`
- **Warehouse**: `WH_DIR_SYS`
- **User**: `US_ECALDERONG`

### Docker Images
- **Local**: `streamlit-radio-app:latest`
- **Snowflake Registry**: `beikxlh-multimedios.registry.snowflakecomputing.com/db_analytics_dev/sch_dir_tec/streamlit_app_repo/streamlit-radio-app:latest`

### Service Configuration
- **Compute Pool**: `streamlit_compute_pool`
- **Service Name**: `streamlit_radio_service`
- **Resources**: 1GB RAM, 0.5 CPU
- **Port**: 8501 (public endpoint)

## Monitoring Commands

```sql
-- Check service status
SHOW SERVICES;

-- Get detailed service status
SELECT SYSTEM$GET_SERVICE_STATUS('streamlit_radio_service');

-- View service logs
SELECT SYSTEM$GET_SERVICE_LOGS('streamlit_radio_service', '0', 'streamlit-app');

-- Get public endpoint
SHOW ENDPOINTS IN SERVICE streamlit_radio_service;

-- Check compute pool
SHOW COMPUTE POOLS;
DESCRIBE COMPUTE POOL streamlit_compute_pool;
```

## Troubleshooting

### Local Issues
- **Docker not running**: Start Docker Desktop
- **Port 8501 in use**: Stop other Streamlit instances
- **Environment variables**: Check `.env` file exists and has correct values

### Snowflake Issues
- **Permission errors**: Ensure ACCOUNTADMIN role
- **Image push fails**: Check Docker login to Snowflake registry
- **Service won't start**: Check compute pool status and service logs
- **Can't access endpoint**: Verify service is running and endpoint is public

### Common Commands
```bash
# Clean up local Docker
make clean

# View logs
make logs

# Access container shell
make shell
```

## Architecture

The deployment creates:
1. **Image Repository**: Stores your Docker image in Snowflake
2. **Compute Pool**: Provides compute resources for containers
3. **Service**: Runs your Streamlit application
4. **Public Endpoint**: Allows external access to your app

Your radio transmission management application will be accessible through a Snowflake-provided public URL once deployed.