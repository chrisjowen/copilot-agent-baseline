# Testing Standards

## Testing Philosophy

### Test-Driven Development (TDD)
- **Red-Green-Refactor**: Follow the complete TDD cycle for all code changes
- **One Test at a Time**: Write one failing test, make it pass, then refactor
- **Minimal Implementation**: Write the least code necessary to make tests pass
- **Test First**: No production code without a failing test

### Testing Principles
- **Fast**: Tests should run quickly to encourage frequent execution
- **Independent**: Tests should not depend on each other or external state
- **Repeatable**: Tests should produce consistent results in any environment
- **Self-Validating**: Tests should have clear pass/fail results
- **Timely**: Tests should be written just before the production code

## Test Types and Strategy

### Unit Tests
**Purpose**: Test individual components in isolation

**Characteristics**:
- Test single functions, methods, or classes
- No external dependencies (use mocks/stubs)
- Fast execution (milliseconds per test)
- High coverage of business logic

**What to Test**:
- Happy path scenarios
- Edge cases and boundary conditions
- Error conditions and exception handling
- Input validation
- Business logic and calculations

### Integration Tests
**Purpose**: Test component interactions and integrations

**Characteristics**:
- Test multiple components working together
- May include database, file system, or network calls
- Slower than unit tests but faster than end-to-end tests
- Focus on data flow and interface contracts

**What to Test**:
- Database operations and queries
- API endpoint behavior
- Service layer interactions
- External service integrations
- Configuration and environment setup

### End-to-End (E2E) Tests
**Purpose**: Test complete user workflows and system behavior

**Characteristics**:
- Test from user perspective through UI or API
- Include all system components
- Slowest tests but highest confidence
- Fewer tests than unit/integration tests

**What to Test**:
- Critical user journeys
- Business process flows
- Cross-browser compatibility (if applicable)
- Performance under realistic conditions
- Security and authentication flows

### Contract Tests
**Purpose**: Test API contracts between services

**Characteristics**:
- Test API request/response formats
- Verify backward compatibility
- Ensure service agreements are met
- Catch breaking changes early

**What to Test**:
- API schema validation
- Response format consistency
- Error response formats
- Version compatibility

## Test Organization and Structure

### Test File Organization
- **Colocation**: Keep tests close to the code they test
- **Naming Conventions**: Clear, descriptive test file names
- **Directory Structure**: Mirror production code structure
- **Grouping**: Group related tests using describe/context blocks

### Test Naming
- **Descriptive Names**: Test names should describe the expected behavior
- **Format**: "should [expected behavior] when [conditions]"
- **Avoid Technical Details**: Focus on behavior, not implementation

**Good Examples**:
```
should return user data when valid ID is provided
should throw validation error when email format is invalid
should calculate total price including tax for premium users
```

**Poor Examples**:
```
test user function
check validation
test case 1
```

### Test Structure (Arrange-Act-Assert)
```
// Arrange: Set up test data and conditions
const input = createTestInput();
const expectedResult = calculateExpectedResult();

// Act: Execute the function being tested
const result = functionUnderTest(input);

// Assert: Verify the expected outcome
expect(result).toEqual(expectedResult);
```

## Test Quality Standards

### Code Coverage Goals
- **Statement Coverage**: 90%+ for critical code paths
- **Branch Coverage**: 85%+ for conditional logic
- **Function Coverage**: 100% for public APIs
- **Line Coverage**: Focus on quality over quantity

### Coverage Guidelines
- **Critical Code**: 100% coverage for business-critical logic
- **Error Paths**: Test all error conditions and exception paths
- **Edge Cases**: Cover boundary conditions and edge cases
- **Public APIs**: Test all public interfaces thoroughly

### Test Quality Criteria
- **Reliability**: Tests should not be flaky or intermittent
- **Maintainability**: Tests should be easy to understand and modify
- **Isolation**: Tests should not affect or depend on other tests
- **Clarity**: Test intent should be obvious from the code

## Test Data Management

### Test Data Strategies
- **Builders**: Use builder pattern for complex test objects
- **Factories**: Create factory functions for common test data
- **Fixtures**: Use fixture files for static test data
- **Generated Data**: Generate random data for property-based testing

### Test Data Principles
- **Minimal Data**: Use only the data necessary for the test
- **Realistic Data**: Use data that resembles production data
- **Data Isolation**: Each test should use independent data
- **Cleanup**: Clean up test data to avoid test pollution

## Mocking and Stubbing

### When to Mock
- **External Dependencies**: APIs, databases, file systems
- **Slow Operations**: Network calls, complex calculations
- **Non-Deterministic Code**: Random generators, current time
- **Side Effects**: Email sending, logging, notifications

### Mocking Best Practices
- **Mock Behaviors, Not Data**: Mock what the dependency does
- **Verify Interactions**: Assert that mocks are called correctly
- **Reset Mocks**: Clean up mocks between tests
- **Minimal Mocking**: Only mock what's necessary for the test

### Test Doubles Types
- **Stub**: Returns predefined responses
- **Mock**: Verifies interactions and method calls
- **Spy**: Wraps real objects to track interactions
- **Fake**: Simplified working implementations

## Performance Testing

### Performance Test Types
- **Load Testing**: Normal expected load
- **Stress Testing**: Beyond normal capacity
- **Volume Testing**: Large amounts of data
- **Endurance Testing**: Extended periods
- **Spike Testing**: Sudden load increases

### Performance Standards
- **Response Times**: Define acceptable response time limits
- **Throughput**: Measure requests per second capacity
- **Resource Usage**: Monitor CPU, memory, and I/O usage
- **Scalability**: Test horizontal and vertical scaling

## Security Testing

### Security Test Areas
- **Authentication**: Login, logout, session management
- **Authorization**: Access control and permissions
- **Input Validation**: SQL injection, XSS prevention
- **Data Protection**: Encryption, sensitive data handling
- **API Security**: Rate limiting, input sanitization

### Security Testing Practices
- **Automated Scanning**: Use security scanning tools
- **Penetration Testing**: Regular manual security testing
- **Dependency Scanning**: Check for vulnerable dependencies
- **Configuration Testing**: Verify secure configuration settings

## Test Automation and CI/CD

### Automation Standards
- **All Tests Automated**: No manual testing in CI/CD pipeline
- **Fast Feedback**: Tests should run quickly and provide rapid feedback
- **Parallel Execution**: Run tests in parallel when possible
- **Test Environment**: Consistent test environments across all stages

### CI/CD Integration
- **Pre-commit Hooks**: Run basic tests before commits
- **Build Pipeline**: Full test suite runs on every build
- **Deployment Gates**: Tests must pass before deployment
- **Post-deployment**: Smoke tests after deployment

### Test Reporting
- **Test Results**: Clear pass/fail reporting
- **Coverage Reports**: Track coverage trends over time
- **Performance Metrics**: Monitor test execution time
- **Failure Analysis**: Detailed information for failing tests

## Maintenance and Refactoring

### Test Maintenance
- **Keep Tests Current**: Update tests when requirements change
- **Refactor Tests**: Apply same quality standards as production code
- **Remove Obsolete Tests**: Delete tests for removed functionality
- **Performance**: Optimize slow-running tests

### Test Debt Management
- **Regular Reviews**: Periodically review and improve test suite
- **Test Smells**: Identify and fix problematic test patterns
- **Documentation**: Keep testing documentation up to date
- **Training**: Ensure team knowledge of testing best practices

---

**Note**: This document provides technology-agnostic testing standards. For technology-specific testing frameworks, syntax, and examples, refer to the appropriate technology-specific standards documents (e.g., `javascript-testing.md`, `python-testing.md`).
