# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Spanish-language Streamlit application for managing radio transmission orders and campaigns (Órdenes/Pautas de Transmisión Radio). The application handles campaign creation, material management, transmission scheduling, and financial calculations for radio advertising.

## Development Commands

### Environment Setup
```bash
# Create conda environment from environment.yml
conda env create -f environment.yml
conda activate app_environment
```

### Running the Application
```bash
# Run Streamlit application locally
streamlit run streamlit_app.py
```

### Dependencies
The application uses conda environment management with core dependencies:
- Python 3.11
- snowflake-snowpark-python 
- streamlit
- pandas, openpyxl for data processing

## Architecture Overview

### Core Application Structure
- **Single-file application**: `streamlit_app.py` contains the entire application logic
- **Session state management**: Uses Streamlit session state for UI state and data persistence
- **Multi-page navigation**: Sidebar menu system with three main sections:
  - "Pautas de Transmisión" (Transmission Orders listing)
  - "Convenios" (Contracts)
  - "➕ Nueva Pauta" (New Order creation)

### Key Components

#### Campaign Management (`➕ Nueva Pauta` section)
- Client and campaign information capture
- Dynamic transmission calendar with 45-day date range
- Financial calculations (subtotal, IVA, totals)
- Material upload and management system
- Excel file import for campaign data pre-population

#### Data Grid System
- Interactive data editor for transmission scheduling
- Real-time calculation of impacts and investment totals
- Calendar-based transmission planning (columns for each day)
- Support for multiple plazas, media types, and programs

#### Material Management
- File upload system for audio/video materials (mp3, wav, mp4, pdf)
- Duration calculation and metadata tracking
- Session state-based material list management

### Database Context
- **Migration Project**: Application is being migrated from native Snowflake Streamlit to Snowpark Container Services
- **Existing Infrastructure**: Database tables and schemas already exist in Snowflake
- **Performance Issues**: Current native implementation has limitations with JavaScript components, file uploads, and response times

### Key Business Logic
- **Campaign Periods**: Default 28-day campaigns with customizable date ranges  
- **Financial Calculations**: Automatic IVA calculation (16%, 8%, 0%, Exento) with multiple currency support
- **Transmission Scheduling**: Daily impact tracking across multiple radio stations and time slots
- **Approval Workflow**: Multi-status campaign management (BORRADOR, VENTAS, CONTACTO COMERCIAL, CAPTURA, PROCESADO F1)

## File Processing
- Excel import functionality reads campaign data from structured xlsx files
- File uploads stored in session state during user session
- Material files processed for duration and metadata extraction

## UI/UX Patterns
- **Responsive Design**: Uses Streamlit columns and containers for multi-column layouts
- **Spanish Language**: All UI text, labels, and user messages in Spanish
- **Custom Styling**: Extensive use of HTML/CSS markdown for custom styling and layout control
- **Expandable Sections**: Heavy use of st.expander for organizing form sections
- **Tab Navigation**: Complex editing interface uses st.tabs for section organization

## Common Development Tasks

When working on this codebase:
1. Test file upload functionality thoroughly - it's a core feature with known limitations
2. Be mindful of session state management - complex data structures are stored in st.session_state
3. Calendar functionality is currently simplified - avoid complex date manipulation
4. Financial calculations are embedded in UI logic - consider extracting for better testability
5. The application handles Spanish language input/output - maintain language consistency

## Migration Considerations
The application is planned for migration to Snowpark Container Services to resolve:
- JavaScript component limitations
- File upload performance issues  
- UI responsiveness problems
- Scalability constraints

Maintain compatibility with existing Snowflake database structures during any modifications.