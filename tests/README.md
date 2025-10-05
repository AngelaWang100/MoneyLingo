# RealityCheck Test Suite

## 📁 Test Structure

```
tests/
├── __init__.py
├── conftest.py              # Test configuration and fixtures
├── run_all_tests.py         # Master test runner
├── README.md               # This file
├── unit/                   # Unit tests for individual components
│   ├── __init__.py
│   └── test_individual_agents.py
├── integration/            # Integration tests for agent interactions
│   ├── __init__.py
│   └── test_orchestrator.py
├── e2e/                    # End-to-end tests for complete workflows
│   ├── __init__.py
│   └── test_complete_workflows.py
└── fixtures/               # Test data and fixtures
    └── __init__.py
```

## 🧪 Test Categories

### **Unit Tests** (`tests/unit/`)
- **Purpose**: Test individual agents and components in isolation
- **Scope**: Single agent functionality
- **Examples**: Translation agent, Financial planning agent, Voice service

### **Integration Tests** (`tests/integration/`)
- **Purpose**: Test agent interactions and orchestration
- **Scope**: Multi-agent coordination, error handling
- **Examples**: Orchestrator coordination, Voice integration

### **End-to-End Tests** (`tests/e2e/`)
- **Purpose**: Test complete user workflows
- **Scope**: Full user journeys, real-world scenarios
- **Examples**: Retirement planning workflow, Multilingual workflow

## 🚀 Running Tests

### **Run All Tests**
```bash
# Run the complete test suite
python tests/run_all_tests.py
```

### **Run Specific Test Categories**
```bash
# Unit tests only
python tests/unit/test_individual_agents.py

# Integration tests only
python tests/integration/test_orchestrator.py

# E2E tests only
python tests/e2e/test_complete_workflows.py
```

### **Run with pytest** (if installed)
```bash
# Install pytest
pip install pytest pytest-asyncio

# Run all tests
pytest tests/

# Run specific category
pytest tests/unit/
pytest tests/integration/
pytest tests/e2e/
```

## 📊 Test Coverage

### **Unit Tests Coverage**
- ✅ Translation Agent
- ✅ Financial Planning Agent
- ✅ Remittance Agent
- ✅ Voice Services
- ✅ Auto Language Detection
- ✅ Voice Translation
- ✅ Tavily Research

### **Integration Tests Coverage**
- ✅ Orchestrator Coordination
- ✅ Agent Error Handling
- ✅ Voice Integration
- ✅ Multi-agent Workflows

### **E2E Tests Coverage**
- ✅ Retirement Planning Workflow
- ✅ Multilingual User Workflow
- ✅ Financial Research Workflow
- ✅ Voice Synthesis Workflow

## 🔧 Test Configuration

### **Environment Variables**
Tests use the same environment variables as the main application:
- `GOOGLE_API_KEY` - For AI agents
- `ELEVENLABS_API_KEY` - For voice synthesis
- `COMET_API_KEY` - For observability
- `ECHO_API_KEY` - For monetization

### **Test Data**
Common test data is provided in `conftest.py`:
- Financial planning scenarios
- Translation examples
- Remittance requests
- Voice synthesis tests
- Research queries

## 📈 Test Results

### **Expected Results**
- **Unit Tests**: 7/7 agents should pass
- **Integration Tests**: 3/3 coordination tests should pass
- **E2E Tests**: 4/4 workflows should pass

### **Success Criteria**
- All agents initialize correctly
- Orchestrator coordinates agents successfully
- Voice synthesis generates audio files
- Multi-language detection works
- Research agent provides insights
- Error handling is graceful

## 🐛 Troubleshooting

### **Common Issues**
1. **Missing API Keys**: Ensure `.env` file has all required keys
2. **Import Errors**: Check Python path includes project root
3. **Async Issues**: Use `pytest-asyncio` for async tests
4. **Voice Failures**: Check ElevenLabs API key and quota

### **Debug Mode**
```bash
# Run with verbose logging
python tests/run_all_tests.py --verbose

# Run specific test with debug
python tests/unit/test_individual_agents.py
```

## 🎯 Test Goals

The test suite ensures:
- ✅ **All agents work correctly**
- ✅ **Orchestrator coordinates properly**
- ✅ **Voice synthesis functions**
- ✅ **Multi-language support works**
- ✅ **Research capabilities function**
- ✅ **Error handling is robust**
- ✅ **Complete workflows succeed**

**Your RealityCheck platform is thoroughly tested and ready for hackathon success!** 🏆
