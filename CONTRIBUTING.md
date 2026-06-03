# Contributing to Production RAG System

Thank you for your interest in contributing to the Production RAG System! This document provides guidelines and instructions for contributing.

## Code of Conduct

Be respectful, inclusive, and professional in all interactions.

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:

   ```bash
   git clone https://github.com/your-username/production-rag-system.git
   cd production-rag-system
   ```

3. **Create a virtual environment**:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

5. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Guidelines

### Code Style

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) conventions
- Use meaningful variable names
- Add type hints where possible
- Write docstrings for all public functions

### Example:

```python
def process_document(file_path: str, collection_name: str) -> dict:
    """
    Process a PDF document and add it to the vector database.

    Args:
        file_path: Path to the PDF file
        collection_name: Name of the Qdrant collection

    Returns:
        Dictionary with processing results
    """
    pass
```

### Testing

- Write tests for new features
- Ensure existing tests still pass
- Run evaluation script: `python run_evaluator.py`

### Documentation

- Update README.md if adding new features
- Add docstrings to new functions
- Comment complex logic

## Submitting Changes

1. **Push to your fork**:

   ```bash
   git push origin feature/your-feature-name
   ```

2. **Create a Pull Request**:
   - Provide a clear description of changes
   - Reference any related issues
   - Include relevant screenshots/results

3. **PR Guidelines**:
   - Keep PRs focused on a single feature/fix
   - Write clear commit messages
   - Update documentation as needed

## Areas for Contribution

### High Priority

- [ ] Multi-language support
- [ ] Advanced caching mechanisms
- [ ] Performance optimizations
- [ ] Better error handling

### Medium Priority

- [ ] Additional LLM provider integrations
- [ ] Custom embedding model support
- [ ] Advanced chunking strategies
- [ ] UI/UX improvements

### Low Priority

- [ ] Documentation improvements
- [ ] Code examples
- [ ] Demo notebooks

## Reporting Issues

When reporting bugs, please include:

- Clear description of the issue
- Steps to reproduce
- Expected vs actual behavior
- Python version and environment details
- Error messages/logs

## Questions?

Feel free to:

- Open an issue for discussion
- Start a discussion thread
- Contact the maintainers

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to Production RAG System! 🚀
