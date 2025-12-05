# Contributing to F1 Telemetry System

First off, thank you for considering contributing to the F1 Telemetry System! It's people like you that make this project better.

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the existing issues to avoid duplicates. When you create a bug report, include as many details as possible:

- **Use a clear and descriptive title**
- **Describe the exact steps to reproduce the problem**
- **Provide specific examples**
- **Describe the behavior you observed and what you expected**
- **Include logs, screenshots, or error messages**
- **Specify your environment** (OS, Docker version, etc.)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion:

- **Use a clear and descriptive title**
- **Provide a detailed description of the suggested enhancement**
- **Explain why this enhancement would be useful**
- **List any alternatives you've considered**

### Pull Requests

1. **Fork the repository** and create your branch from `main`
2. **Follow the coding standards** for each service
3. **Write clear commit messages**
4. **Add tests** if applicable
5. **Update documentation** as needed
6. **Ensure CI/CD passes** before requesting review

## Development Process

### Setting Up Development Environment

1. Clone your fork:
   ```bash
   git clone https://github.com/YOUR_USERNAME/F1-Telemetry.git
   cd F1-Telemetry
   ```

2. Create a branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. Start development environment:
   ```bash
   make dev-up
   ```

### Service-Specific Guidelines

#### C++ (Telemetry Ingest)

- Follow C++17 standards
- Use meaningful variable and function names
- Add comments for complex logic
- Run memory leak checks with valgrind
- Format code consistently

#### Python (Telemetry Processor)

- Follow PEP 8 style guide
- Use type hints where applicable
- Format with `black`
- Lint with `flake8`
- Type check with `mypy`
- Write docstrings for functions and classes

#### TypeScript/React (Telemetry Frontend)

- Follow TypeScript best practices
- Use functional components with hooks
- Format with Prettier
- Lint with ESLint
- Write meaningful component names
- Add PropTypes or TypeScript interfaces

### Testing Requirements

- **Unit tests** for new functionality
- **Integration tests** for service interactions
- **Maintain or improve** code coverage
- **All tests must pass** before merging

### Commit Message Guidelines

Use clear and meaningful commit messages:

```
<type>(<scope>): <subject>

<body>

<footer>
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

Example:
```
feat(ingest): add support for F1 24 telemetry format

- Parse new packet types introduced in F1 24
- Update data structures for new fields
- Maintain backward compatibility with F1 23

Closes #123
```

### Code Review Process

1. **Automated checks** run via GitHub Actions
2. **At least one maintainer** must approve
3. **All feedback** should be addressed
4. **Squash and merge** preferred for feature branches

## Project Structure

```
F1-Telemetry/
├── services/
│   ├── telemetry-ingest/       # C++ UDP ingest service
│   ├── telemetry-processor/    # Python middleware
│   └── telemetry-frontend/     # React frontend
├── monitoring/                  # Observability configs
├── .github/workflows/          # CI/CD pipelines
├── docker-compose.yml          # Production orchestration
├── docker-compose.dev.yml      # Development overrides
└── Makefile                    # Convenience commands
```

## Questions?

Feel free to:
- Open an issue for discussion
- Join GitHub Discussions
- Reach out to maintainers

Thank you for your contributions! 🏎️
