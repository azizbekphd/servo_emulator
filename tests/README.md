# Test Suite Documentation

This directory contains comprehensive unit tests for the servo_emulator project.

## Test Organization

Tests are organized by module with each test file corresponding to a source module:

- **test_conversion.py**: Tests for hex/bytes conversion utilities
- **test_program_mode.py**: Tests for program mode enums and models
- **test_transmission.py**: Tests for transmission data model
- **test_config.py**: Tests for application configuration
- **test_request_response_pair.py**: Tests for request/response pair model
- **test_serial_port.py**: Tests for serial port model
- **test_serial_signal.py**: Tests for serial signal model
- **test_ports_list.py**: Tests for port list utilities
- **test_serials_list.py**: Tests for serial list utilities
- **test_responses_controller.py**: Tests for response controller

## Running Tests

### Run all tests:
```bash
pytest
```

### Run specific test file:
```bash
pytest tests/test_conversion.py
```

### Run specific test class:
```bash
pytest tests/test_conversion.py::TestConversion
```

### Run specific test:
```bash
pytest tests/test_conversion.py::TestConversion::test_bytes_to_hex_string_list_single_byte
```

### Run with verbose output:
```bash
pytest -v
```

### Run with coverage report:
```bash
pytest --cov=src --cov-report=html
```

## Test Coverage

The test suite covers:

1. **Utility Functions** (conversion, ports_list, serials_list)
   - Hex/bytes conversion in both directions
   - Port/serial finding and listing
   - Edge cases like empty lists and not-found scenarios

2. **Data Models** (transmission, program_mode, request_response_pair, serial_port, serial_signal)
   - Object creation with various parameters
   - Default values
   - Attribute access and modification
   - Model-specific behavior

3. **Configuration** (config.py)
   - Constant values
   - Configuration structure
   - Required keys and values

4. **Controllers** (responses.py)
   - State management
   - Data persistence (with mocked file I/O)
   - Request/response pair management

## Test Design Principles

- **Isolation**: Each test is independent and doesn't rely on other tests
- **Clarity**: Test names clearly describe what is being tested
- **Completeness**: Tests cover happy paths, edge cases, and error conditions
- **Mocking**: External dependencies (file I/O, serial ports) are mocked
- **Maintainability**: Tests use descriptive docstrings and comments

## Notes on GUI Testing

The `main.py` and `ui/` modules are primarily GUI-focused and difficult to unit test due to their dependency on Kivy. These components are better tested through:
- Manual testing
- UI/integration tests with a testing framework like pytest-qt
- System tests

The `ports.py` controller contains threading and serial communication logic that is partially tested through mocking. More comprehensive testing would require:
- Mock serial port objects
- Threading coordination tests
- Integration tests with virtual serial ports

## Future Enhancements

- Add integration tests for controller components
- Add UI tests using pytest-qt
- Add tests with coverage reporting
- Add performance benchmarks for conversion functions
- Add tests for thread safety in port controller
