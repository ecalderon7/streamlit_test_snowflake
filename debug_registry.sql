-- Run this in Snowflake to get the correct registry URL
SELECT SYSTEM$REGISTRY_LIST_IMAGES('streamlit_app_repo');

-- Also check the exact registry URL format
SHOW IMAGE REPOSITORIES;

-- Get registry login details
SELECT SYSTEM$GET_SNOWSIGHT_HOST() as snowflake_host;

-- Check account info
SELECT CURRENT_ACCOUNT() as account_name;