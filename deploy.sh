#!/bin/bash

# Snowpark Container Services Deployment Script
# This script automates the deployment process

set -e  # Exit on any error

echo "🚀 Starting Snowpark Container Services Deployment..."

# Load environment variables
if [ -f .env ]; then
    export $(cat .env | xargs)
    echo "✅ Environment variables loaded"
else
    echo "❌ .env file not found. Please create it from .env.template"
    exit 1
fi

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker Desktop."
    exit 1
fi

# Step 1: Build Docker image for local testing
echo "🔨 Building Docker image for local testing..."
docker build -t streamlit-radio-app:latest .

# Step 2: Test locally (optional - will run in background for 10 seconds)
echo "🧪 Testing application locally..."
docker run -d --name streamlit-test -p 8501:8501 --env-file .env streamlit-radio-app:latest

echo "⏳ Waiting 10 seconds for app to start..."
sleep 10

# Check if app is responding
if curl -f http://localhost:8501/_stcore/health > /dev/null 2>&1; then
    echo "✅ Local test successful! App is running at http://localhost:8501"
else
    echo "⚠️  Local health check failed, but continuing with deployment..."
fi

# Stop test container
docker stop streamlit-test > /dev/null 2>&1
docker rm streamlit-test > /dev/null 2>&1

# Step 3: Build image for Snowflake registry
echo "🔨 Building Docker image for Snowflake registry..."
SNOWFLAKE_IMAGE="${SNOWFLAKE_ACCOUNT,,}.registry.snowflakecomputing.com/${SNOWFLAKE_DATABASE,,}/${SNOWFLAKE_SCHEMA,,}/streamlit_app_repo/streamlit-radio-app:latest"
docker build -t "$SNOWFLAKE_IMAGE" .

# Step 4: Login to Snowflake registry
echo "🔐 Logging into Snowflake Container Registry..."
echo "You will be prompted for your Snowflake password..."
docker login "${SNOWFLAKE_ACCOUNT,,}.registry.snowflakecomputing.com" -u "$SNOWFLAKE_USER"

# Step 5: Push image to Snowflake
echo "📤 Pushing image to Snowflake registry..."
docker push "$SNOWFLAKE_IMAGE"

echo "✅ Docker image pushed successfully!"
echo ""
echo "🎯 Next Steps:"
echo "1. Run the SQL commands in snowflake_setup.sql in your Snowflake account"
echo "2. The service will be created and available at a public endpoint"
echo "3. Use these commands to monitor the service:"
echo "   - SHOW SERVICES;"
echo "   - SELECT SYSTEM\$GET_SERVICE_STATUS('streamlit_radio_service');"
echo "   - SHOW ENDPOINTS IN SERVICE streamlit_radio_service;"
echo ""
echo "🌐 Your Streamlit app will be available at the public endpoint once the service is running!"