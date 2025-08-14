# Radio Transmission Order Management System - Snowpark Container Services Deployment

## Project Overview

This repository contains a **Spanish-language Streamlit application** for managing radio transmission orders and campaigns (Órdenes/Pautas de Transmisión Radio). **The database tables and structures already exist in Snowflake**, but the application is experiencing significant performance and functionality limitations when running as native Streamlit inside Snowflake.

## **Current Situation**

### **✅ What's Already Done**
- **Database Infrastructure**: All required tables and schemas exist in Snowflake
- **Core Application Logic**: Functional Streamlit app with complete business workflows
- **Data Connectivity**: Working connections to existing Snowflake data structures

### **❌ Current Problems with Native Streamlit in Snowflake**
- **Performance Issues**: Slow response times and timeouts
- **JavaScript Limitations**: Calendar and interactive components not working properly
- **File Upload Restrictions**: Limited file handling capabilities
- **UI Responsiveness**: Poor user experience compared to local development

### **🎯 Migration Goal**
Deploy the application to **Snowpark Container Services** to unlock full Streamlit functionality and resolve performance issues while maintaining connection to existing Snowflake data.

## **SNOWPARK CONTAINER SERVICES DEPLOYMENT STRATEGY**

### **Phase 1: Basic Deployment Test (Priority 1)**
Create a minimal Streamlit app to test and understand the Snowpark deployment process:

```python
# test_app.py - Basic Snowpark deployment test
import streamlit as st
import snowflake.snowpark as snowpark
from snowflake.snowpark import Session

st.title("Snowpark Deployment Test")
st.write("Testing basic Snowpark Container Services deployment")

# Simple connectivity test
if st.button("Test Snowflake Connection"):
    try:
        # Basic connection test (using existing credentials)
        st.success("Connection successful!")
        st.write("Ready for full app migration")
    except Exception as e:
        st.error(f"Connection failed: {e}")
```

### **Phase 2: Full Application Migration (Priority 2)**
Once deployment process is understood, migrate the complete radio transmission application.

## **SNOWPARK DEPLOYMENT REQUIREMENTS**

### **1. Container Configuration**
```dockerfile
# Dockerfile for Snowpark deployment
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### **2. Dependencies for Snowpark**
```txt
# requirements.txt
streamlit>=1.28.0
snowflake-snowpark-python>=1.9.0
pandas>=2.0.0
openpyxl>=3.1.0
python-dateutil>=2.8.0
```

### **3. Snowpark Service Configuration**
```yaml
# snowpark-service.yaml
spec:
  containers:
  - name: streamlit-app
    image: <your-registry>/radio-transmission-app:latest
    env:
      SNOWFLAKE_ACCOUNT: <account>
      SNOWFLAKE_USER: <user>
      SNOWFLAKE_PASSWORD: <password>
      SNOWFLAKE_DATABASE: <existing-database>
      SNOWFLAKE_SCHEMA: <existing-schema>
    resources:
      requests:
        memory: "1Gi"
        cpu: "0.5"
      limits:
        memory: "2Gi"
        cpu: "1.0"
  endpoints:
  - name: streamlit
    port: 8501
    public: true
```

## **DEPLOYMENT PROCESS STEPS**

### **Step 1: Prepare Container Registry**
```sql
-- Create image repository in Snowflake
CREATE IMAGE REPOSITORY IF NOT EXISTS my_db.my_schema.my_repo;

-- Grant privileges
GRANT READ, WRITE ON IMAGE REPOSITORY my_db.my_schema.my_repo TO ROLE my_role;
```

### **Step 2: Build and Push Container**
```bash
# Build container
docker build -t radio-transmission-app .

# Tag for Snowflake registry
docker tag radio-transmission-app <account>.registry.snowflakecomputing.com/my_db/my_schema/my_repo/radio-transmission-app:latest

# Push to Snowflake
docker push <account>.registry.snowflakecomputing.com/my_db/my_schema/my_repo/radio-transmission-app:latest
```

### **Step 3: Create Snowpark Service**
```sql
-- Create compute pool for containers
CREATE COMPUTE POOL IF NOT EXISTS my_compute_pool
  MIN_NODES = 1
  MAX_NODES = 3
  INSTANCE_FAMILY = CPU_X64_XS;

-- Create service
CREATE SERVICE my_streamlit_service
  IN COMPUTE POOL my_compute_pool
  FROM SPECIFICATION $
    spec:
      containers:
      - name: streamlit-app
        image: <account>.registry.snowflakecomputing.com/my_db/my_schema/my_repo/radio-transmission-app:latest
        env:
          SNOWFLAKE_ACCOUNT: <account>
        resources:
          requests:
            memory: 1Gi
            cpu: 0.5
      endpoints:
      - name: streamlit
        port: 8501
        public: true
  $;
```

## **MIGRATION ADVANTAGES**

### **✅ Benefits of Snowpark Container Services**
- **Full JavaScript Support**: Calendar components will work properly
- **Better Performance**: Dedicated container resources
- **Complete File Handling**: No upload restrictions
- **Custom Dependencies**: Install any required Python packages
- **Scalability**: Auto-scaling based on demand
- **Isolation**: Dedicated environment for the application

### **🔄 Maintains Existing Infrastructure**
- **Database Connectivity**: Direct access to existing Snowflake tables
- **Security Model**: Leverages existing Snowflake RBAC
- **Data Pipeline Integration**: No changes to existing data flows
- **User Access**: Same authentication and authorization

## **BASIC TEST APPLICATION FOR DEPLOYMENT**

### **Simple Test App (test_app.py)**
```python
import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Snowpark Test App", layout="wide")

st.title("🧪 Snowpark Container Services Test")
st.markdown("---")

# Test basic Streamlit functionality
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Test Metric 1", "100", "5")
    
with col2:
    st.metric("Test Metric 2", "200", "-3")
    
with col3:
    st.metric("Test Metric 3", "300", "10")

# Test interactive components
st.markdown("### Interactive Components Test")
with st.expander("Test Expandable Section"):
    name = st.text_input("Test Input")
    date = st.date_input("Test Date", datetime.now())
    option = st.selectbox("Test Select", ["Option 1", "Option 2", "Option 3"])
    
    if st.button("Test Button"):
        st.success(f"✅ Input received: {name}, {date}, {option}")

# Test data display
st.markdown("### Data Display Test")
test_data = pd.DataFrame({
    'Column A': [1, 2, 3, 4],
    'Column B': ['Test 1', 'Test 2', 'Test 3', 'Test 4'],
    'Column C': [10.5, 20.3, 30.1, 40.8]
})

edited_data = st.data_editor(test_data, num_rows="dynamic")

# Test file upload (basic)
st.markdown("### File Upload Test")
uploaded_file = st.file_uploader("Test file upload", type=['txt', 'csv'])
if uploaded_file:
    st.success("✅ File uploaded successfully!")
    st.write(f"File name: {uploaded_file.name}")

# Test connection placeholder
st.markdown("

## **TECHNICAL DEBT & ISSUES**

### **Code Quality Concerns**
- **Mixed Languages**: Comments and variables in Spanish, affecting maintainability
- **Hardcoded Values**: Currency rates, user roles, and business logic embedded in UI
- **Error Handling**: Minimal error handling for file operations and data validation
- **No Testing**: No unit tests or integration tests present

### **Performance Issues**
- **DataFrame Recalculation**: Expensive operations in UI loops
- **File Processing**: Synchronous file operations may cause timeouts
- **Memory Usage**: Large session state objects for complex campaigns

### **Security Gaps**
- **No Authentication**: Hardcoded user credentials
- **No Validation**: Missing input sanitization and data validation
- **No Encryption**: Sensitive data handled in plain text

## **MIGRATION ROADMAP**

### **Phase 1: Database Foundation (Week 1-2)**
1. Design and create Snowflake database schema
2. Implement basic CRUD operations for campaigns
3. Set up user roles and permissions
4. Create API endpoints for data operations

### **Phase 2: Core Functionality Migration (Week 3-4)** 
1. Migrate campaign creation and editing
2. Implement file upload to Snowflake stages
3. Convert transmission grid to database-backed operations
4. Add basic financial calculations

### **Phase 3: Advanced Features (Week 5-6)**
1. Implement simplified calendar interface
2. Add material management with file storage
3. Create reporting and export functionality
4. Add audit logging and workflow management

### **Phase 4: Production Readiness (Week 7-8)**
1. Performance optimization and caching
2. Comprehensive error handling
3. Security hardening and testing
4. User training and documentation

## **TECHNICAL REQUIREMENTS**

### **Snowflake Resources**
- Database with appropriate compute warehouse
- External stage configuration (Azure Blob/AWS S3)
- User roles and permissions setup
- Snowpark Container Services (if containerized approach)

### **Python Dependencies**
```python
# Core requirements
streamlit>=1.28.0
pandas>=2.0.0
snowflake-snowpark-python>=1.9.0
snowflake-connector-python>=3.5.0

# Additional for file processing
openpyxl>=3.1.0  # Excel file handling
python-dateutil>=2.8.0  # Date parsing
```

### **Infrastructure Considerations**
- Network security for external stage access
- Backup and disaster recovery procedures
- Monitoring and alerting for application health
- Data retention and archival policies

## **RISKS & MITIGATION STRATEGIES**

### **High-Risk Items**
1. **Calendar Functionality**: May require complete redesign
   - *Mitigation*: Prototype simplified calendar early
2. **File Upload Performance**: Large files may timeout
   - *Mitigation*: Implement chunked uploads and async processing  
3. **User Adoption**: Complex workflow changes
   - *Mitigation*: Phased rollout with extensive training

### **Medium-Risk Items**
1. **Data Migration**: Existing Excel-based workflows
   - *Mitigation*: Maintain Excel export/import during transition
2. **Integration Points**: ERP system connectivity
   - *Mitigation*: API-first design for external integrations

## **SUCCESS METRICS**

### **Technical KPIs**
- Page load times < 3 seconds
- File upload success rate > 95%
- Zero data loss during migration
- 99.5% application uptime

### **Business KPIs**  
- 50% reduction in campaign creation time
- 90% user adoption within 3 months
- Elimination of manual Excel processes
- Complete audit trail for compliance

## **IMMEDIATE NEXT STEPS**

1. **Database Design Workshop**: Define complete schema with business stakeholders
2. **File Storage Proof of Concept**: Test external stage configuration and file processing
3. **Calendar Component Research**: Evaluate alternatives for transmission scheduling
4. **Performance Baseline**: Establish current performance metrics for comparison
5. **Security Assessment**: Review compliance requirements and implement authentication

---

## **Repository Structure Recommendation**

```
/
├── src/
│   ├── streamlit_app.py          # Current application
│   ├── snowpark/                 # Snowpark-specific adaptations
│   ├── database/                 # Schema and migration scripts  
│   ├── api/                      # File upload and data APIs
│   └── utils/                    # Shared utilities
├── docs/
│   ├── deployment-guide.md
│   ├── database-schema.md
│   └── migration-plan.md
├── tests/
├── docker/                       # Container configuration (if needed)
└── environment.yml               # Current Snowpark dependencies
```

This context should provide Claude Code with comprehensive understanding of the migration complexity and technical requirements for successful Snowpark deployment.