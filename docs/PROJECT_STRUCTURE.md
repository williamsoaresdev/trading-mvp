# 📁 Project Structure Guide

## 🏗️ **Enterprise-Level Organization**

This project follows enterprise-level organizational standards for professional development.

### 📂 **Root Directory Structure**

```
trading-mvp/
├── 📚 docs/                    # Documentation & Guides
├── 🔧 scripts/                 # Build & Setup Scripts  
├── 🧪 tests/                   # Test Suite
├── 🛠️ tools/                   # Development Tools
├── ⚙️ config/                  # Configuration Files
├── 🧠 trading-intelligence/    # AI/ML Backend
├── 🤖 trading-executor/        # .NET Executor
├── 🖥️ trading-dashboard/       # Angular Frontend
├── 📖 README.md               # Main documentation
├── ⚖️ LICENSE                 # License file
├── 🚫 .gitignore              # Git ignore rules
└── 📦 trading-mvp.sln         # Visual Studio Solution
```

## 📚 **docs/** - Documentation Hub

**Purpose**: Centralized documentation management
**Contents**:
- `SETUP_GUIDE.md` - Complete setup instructions
- `REFACTORING_LOG.md` - Architecture evolution history
- `REQUIREMENTS.md` - System requirements
- `PROJECT_STRUCTURE.md` - This file

**Why separate**: Keeps root clean while maintaining comprehensive docs

## 🔧 **scripts/** - Build & Automation

**Purpose**: All build, setup, and execution scripts
**Contents**:
- `setup.py` - Cross-platform setup script
- `setup.sh` - Unix/Linux setup automation
- `setup.bat` - Windows setup automation
- `run_server.py` - Start API server
- `run_realtime.py` - Start real-time service
- `start_api.py` - Legacy API starter
- `start_clean_api.py` - Clean Architecture API starter

**Why separate**: Organized DevOps and eliminates root clutter

## 🧪 **tests/** - Quality Assurance

**Purpose**: Complete test suite organization
**Contents**:
- `test_clean_architecture.py` - Clean Architecture validation
- `test_complete_system.py` - End-to-end integration tests
- `test_results_summary.py` - Test results and metrics

**Why separate**: Professional testing organization and CI/CD ready

## 🛠️ **tools/** - Development Utilities

**Purpose**: Development tools and code analysis
**Contents**:
- `code_analysis.py` - Comprehensive code quality analyzer
- `quality_report.py` - Quality metrics and reports
- `final_structure.py` - Structure documentation generator
- `verify_structure.py` - Structure validation tool

**Why separate**: Developer productivity tools in dedicated space

## 🏗️ **Core Architecture**

### 🧠 **trading-intelligence/** - Python AI/ML
Clean Architecture implementation with Domain-Driven Design

### 🤖 **trading-executor/** - .NET Real-time
High-performance order execution with Clean Architecture

### 🖥️ **trading-dashboard/** - Angular Frontend
Modern reactive UI with real-time WebSocket updates

### ⚙️ **config/** - Configuration
Centralized configuration management

## 🎯 **Benefits of This Organization**

### ✅ **Professional Standards**
- Enterprise-level folder structure
- Industry best practices compliance
- Scalable organization patterns

### ✅ **Developer Experience**
- Clear separation of concerns
- Easy navigation and onboarding
- Predictable file locations

### ✅ **DevOps Ready**
- CI/CD friendly structure
- Automated tooling support
- Clean deployment patterns

### ✅ **Maintenance Friendly**
- Logical grouping reduces cognitive load
- Easy to find and update files
- Consistent patterns across project

## 🚀 **Usage Patterns**

### Development Workflow
```bash
# Run analysis tools
python tools/code_analysis.py

# Execute tests
python tests/test_clean_architecture.py

# Setup project
python scripts/setup.py

# Start services
python scripts/run_realtime.py
```

### Documentation Workflow
```bash
# Read setup guide
docs/SETUP_GUIDE.md

# Check requirements
docs/REQUIREMENTS.md

# Review architecture evolution
docs/REFACTORING_LOG.md
```

---

**🎯 Result**: Professional, scalable, and maintainable project organization that follows enterprise standards while supporting rapid development and deployment.