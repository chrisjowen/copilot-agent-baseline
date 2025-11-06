# JavaScript/TypeScript Development Standards

## Language-Specific Guidelines

### Code Style and Formatting
- **Linting**: Use ESLint with strict configuration
- **Formatting**: Use Prettier for consistent code formatting
- **TypeScript**: Prefer TypeScript for type safety and better IDE support
- **ES6+**: Use modern JavaScript features and syntax

### Naming Conventions
```javascript
// Variables and functions: camelCase
const userName = 'john_doe';
function getUserData() { }

// Constants: UPPER_SNAKE_CASE
const API_BASE_URL = 'https://api.example.com';

// Classes: PascalCase
class UserManager { }

// Private properties: prefix with underscore
class User {
  constructor(name) {
    this._id = generateId();
    this.name = name;
  }
}
```

### File Organization
```
src/
├── components/     # React/Vue components
├── services/       # Business logic and API calls
├── utils/          # Utility functions
├── types/          # TypeScript type definitions
├── hooks/          # Custom React hooks
├── stores/         # State management (Redux, Zustand, etc.)
└── tests/          # Test files
    ├── unit/
    ├── integration/
    └── e2e/
```

## Testing Standards (JavaScript/TypeScript)

### Testing Framework Setup
```javascript
// Jest configuration example
module.exports = {
  testEnvironment: 'node',
  coverageDirectory: 'coverage',
  collectCoverageFrom: [
    'src/**/*.{js,ts}',
    '!src/**/*.d.ts',
    '!src/**/*.test.{js,ts}'
  ],
  testMatch: [
    '**/__tests__/**/*.{js,ts}',
    '**/*.{test,spec}.{js,ts}'
  ],
  setupFilesAfterEnv: ['<rootDir>/src/setupTests.js']
};
```

### Unit Test Examples

#### Basic Function Testing
```javascript
// Function under test
function calculateTotal(items, taxRate = 0) {
  if (!Array.isArray(items)) {
    throw new Error('Items must be an array');
  }
  
  const subtotal = items.reduce((sum, item) => sum + (item.price || 0), 0);
  return subtotal * (1 + taxRate);
}

// Test file: calculateTotal.test.js
describe('calculateTotal', () => {
  it('should calculate total for array of items without tax', () => {
    // Arrange
    const items = [
      { price: 10.00 },
      { price: 20.00 }
    ];
    
    // Act
    const result = calculateTotal(items);
    
    // Assert
    expect(result).toBe(30.00);
  });

  it('should calculate total including tax', () => {
    // Arrange
    const items = [{ price: 100.00 }];
    const taxRate = 0.08;
    
    // Act
    const result = calculateTotal(items, taxRate);
    
    // Assert
    expect(result).toBe(108.00);
  });

  it('should throw error for invalid input', () => {
    // Arrange & Act & Assert
    expect(() => calculateTotal('not an array')).toThrow('Items must be an array');
  });

  it('should handle items without price property', () => {
    // Arrange
    const items = [
      { price: 10.00 },
      { name: 'item without price' }
    ];
    
    // Act
    const result = calculateTotal(items);
    
    // Assert
    expect(result).toBe(10.00);
  });
});
```

#### Class Testing with Test Data Builder
```javascript
// Test data builder pattern
class UserBuilder {
  constructor() {
    this.user = {
      id: '123',
      name: 'Default Name',
      email: 'default@email.com',
      role: 'user'
    };
  }
  
  withId(id) {
    this.user.id = id;
    return this;
  }
  
  withName(name) {
    this.user.name = name;
    return this;
  }
  
  withEmail(email) {
    this.user.email = email;
    return this;
  }
  
  withRole(role) {
    this.user.role = role;
    return this;
  }
  
  build() {
    return { ...this.user };
  }
}

// Usage in tests
describe('UserValidator', () => {
  let validator;

  beforeEach(() => {
    validator = new UserValidator();
  });

  it('should return true for valid user', () => {
    // Arrange
    const user = new UserBuilder()
      .withEmail('valid@email.com')
      .withName('John Doe')
      .build();
    
    // Act
    const isValid = validator.validateUser(user);
    
    // Assert
    expect(isValid).toBe(true);
  });

  it('should return false for invalid email format', () => {
    // Arrange
    const user = new UserBuilder()
      .withEmail('invalid-email')
      .build();
    
    // Act
    const isValid = validator.validateUser(user);
    
    // Assert
    expect(isValid).toBe(false);
  });
});
```

### Async Testing
```javascript
describe('UserService', () => {
  let userService;
  let mockApiClient;

  beforeEach(() => {
    mockApiClient = {
      get: jest.fn(),
      post: jest.fn()
    };
    userService = new UserService(mockApiClient);
  });

  it('should fetch user data successfully', async () => {
    // Arrange
    const userId = '123';
    const expectedUser = { id: userId, name: 'John Doe' };
    mockApiClient.get.mockResolvedValue({ data: expectedUser });

    // Act
    const user = await userService.getUser(userId);

    // Assert
    expect(user).toEqual(expectedUser);
    expect(mockApiClient.get).toHaveBeenCalledWith(`/users/${userId}`);
  });

  it('should handle API errors gracefully', async () => {
    // Arrange
    const userId = '123';
    const error = new Error('Network error');
    mockApiClient.get.mockRejectedValue(error);

    // Act & Assert
    await expect(userService.getUser(userId)).rejects.toThrow('Network error');
  });
});
```

### React Component Testing
```javascript
import { render, screen, fireEvent } from '@testing-library/react';
import UserProfile from './UserProfile';

describe('UserProfile', () => {
  const defaultProps = {
    user: {
      id: '1',
      name: 'John Doe',
      email: 'john@example.com'
    },
    onEdit: jest.fn()
  };

  it('should display user information', () => {
    // Arrange & Act
    render(<UserProfile {...defaultProps} />);
    
    // Assert
    expect(screen.getByText('John Doe')).toBeInTheDocument();
    expect(screen.getByText('john@example.com')).toBeInTheDocument();
  });

  it('should call onEdit when edit button is clicked', () => {
    // Arrange
    render(<UserProfile {...defaultProps} />);
    
    // Act
    fireEvent.click(screen.getByRole('button', { name: /edit/i }));
    
    // Assert
    expect(defaultProps.onEdit).toHaveBeenCalledWith(defaultProps.user);
  });

  it('should show loading state', () => {
    // Arrange & Act
    render(<UserProfile {...defaultProps} isLoading={true} />);
    
    // Assert
    expect(screen.getByText('Loading...')).toBeInTheDocument();
  });
});
```

### API Integration Testing
```javascript
import request from 'supertest';
import app from '../app';

describe('User API Endpoints', () => {
  describe('GET /api/users/:id', () => {
    it('should return user data for valid ID', async () => {
      // Arrange
      const userId = '123';
      
      // Act
      const response = await request(app)
        .get(`/api/users/${userId}`)
        .expect(200);
      
      // Assert
      expect(response.body).toMatchObject({
        id: userId,
        name: expect.any(String),
        email: expect.stringMatching(/\S+@\S+\.\S+/)
      });
    });

    it('should return 404 for non-existent user', async () => {
      // Act & Assert
      await request(app)
        .get('/api/users/nonexistent')
        .expect(404)
        .expect(res => {
          expect(res.body.error).toBe('User not found');
        });
    });
  });

  describe('POST /api/users', () => {
    it('should create new user with valid data', async () => {
      // Arrange
      const newUser = {
        name: 'Jane Doe',
        email: 'jane@example.com'
      };
      
      // Act
      const response = await request(app)
        .post('/api/users')
        .send(newUser)
        .expect(201);
      
      // Assert
      expect(response.body).toMatchObject({
        id: expect.any(String),
        ...newUser
      });
    });

    it('should validate required fields', async () => {
      // Arrange
      const invalidUser = { name: 'No Email' };
      
      // Act & Assert
      await request(app)
        .post('/api/users')
        .send(invalidUser)
        .expect(400)
        .expect(res => {
          expect(res.body.errors).toContain('Email is required');
        });
    });
  });
});
```

### Mocking Best Practices
```javascript
// Mock external dependencies
jest.mock('../services/emailService', () => ({
  sendEmail: jest.fn()
}));

// Mock only specific methods
const mockDatabaseService = {
  findUser: jest.fn(),
  createUser: jest.fn(),
  updateUser: jest.fn()
};

jest.mock('../services/databaseService', () => mockDatabaseService);

describe('UserController', () => {
  beforeEach(() => {
    // Clear all mocks before each test
    jest.clearAllMocks();
  });

  it('should create user and send welcome email', async () => {
    // Arrange
    const userData = { name: 'John', email: 'john@example.com' };
    const createdUser = { id: '123', ...userData };
    
    mockDatabaseService.createUser.mockResolvedValue(createdUser);
    
    // Act
    const result = await userController.createUser(userData);
    
    // Assert
    expect(mockDatabaseService.createUser).toHaveBeenCalledWith(userData);
    expect(emailService.sendEmail).toHaveBeenCalledWith(
      userData.email,
      'Welcome!',
      expect.any(String)
    );
    expect(result).toEqual(createdUser);
  });
});
```

## Build and Development Tools

### Package.json Scripts
```json
{
  "scripts": {
    "dev": "nodemon src/index.js",
    "build": "tsc",
    "test": "jest",
    "test:watch": "jest --watch",
    "test:coverage": "jest --coverage",
    "lint": "eslint src/**/*.{js,ts}",
    "lint:fix": "eslint src/**/*.{js,ts} --fix",
    "format": "prettier --write src/**/*.{js,ts}",
    "type-check": "tsc --noEmit"
  }
}
```

### ESLint Configuration
```javascript
module.exports = {
  extends: [
    'eslint:recommended',
    '@typescript-eslint/recommended',
    'prettier'
  ],
  parser: '@typescript-eslint/parser',
  plugins: ['@typescript-eslint'],
  rules: {
    'no-console': 'warn',
    'no-unused-vars': 'error',
    '@typescript-eslint/no-explicit-any': 'error',
    '@typescript-eslint/explicit-function-return-type': 'warn'
  }
};
```

### Performance and Security

#### Performance Best Practices
```javascript
// Use async/await for better readability
async function processUsers(userIds) {
  const users = await Promise.all(
    userIds.map(id => userService.getUser(id))
  );
  return users.filter(user => user.isActive);
}

// Implement caching
const cache = new Map();

function getExpensiveData(key) {
  if (cache.has(key)) {
    return cache.get(key);
  }
  
  const data = performExpensiveOperation(key);
  cache.set(key, data);
  return data;
}
```

#### Security Best Practices
```javascript
// Input validation
const Joi = require('joi');

const userSchema = Joi.object({
  name: Joi.string().alphanum().min(3).max(30).required(),
  email: Joi.string().email().required(),
  age: Joi.number().integer().min(18).max(100)
});

function validateUser(userData) {
  return userSchema.validate(userData);
}

// Sanitize output
const validator = require('validator');

function sanitizeUserInput(input) {
  return {
    name: validator.escape(input.name),
    email: validator.normalizeEmail(input.email)
  };
}
```

---

**Note**: This document provides JavaScript/TypeScript-specific standards and examples. Follow these in conjunction with the general development and testing standards.
