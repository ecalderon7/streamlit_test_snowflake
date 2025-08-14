#!/bin/bash
set -e

echo "🔐 Logging into Snowflake Container Registry..."
echo "Wdtxm-13513926" | docker login beikxlh-multimedios.registry.snowflakecomputing.com -u US_ECALDERONG --password-stdin

echo "📤 Pushing Docker image to Snowflake..."
docker push beikxlh-multimedios.registry.snowflakecomputing.com/db_analytics_dev/sch_dir_tec/streamlit_app_repo/streamlit-radio-app:latest

echo "✅ Image pushed successfully!"
echo ""
echo "🎯 Now run the CREATE SERVICE command from snowflake_setup.sql"