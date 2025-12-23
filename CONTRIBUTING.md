# Contributing to SPIFFE/SPIRE for AI Agents Code Examples

Thank you for your interest in contributing! This repository contains code examples from the book "SPIFFE/SPIRE for AI Agents."

## How to Contribute

### Reporting Bugs

Found a bug in the code examples? Please open an issue with:

- **Description:** Clear description of the bug
- **Steps to reproduce:** How to replicate the issue
- **Expected behavior:** What should happen
- **Actual behavior:** What actually happens
- **Environment:**
  - OS (e.g., Ubuntu 22.04)
  - SPIRE version (e.g., 1.8.0)
  - Kubernetes version (e.g., 1.27)
  - Python version (if applicable)

### Suggesting Enhancements

Have an idea for improvement?

1. Open an issue with the "enhancement" label
2. Describe the enhancement clearly
3. Explain why it would be useful
4. Provide examples if possible

### Pull Requests

#### Process

1. Fork the repository
2. Create a branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Test thoroughly
5. Commit with clear messages (`git commit -m 'Add amazing feature'`)
6. Push to your branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

#### Guidelines

**Python Code:**
- Follow PEP 8 style guide
- Use Black for formatting (`black .`)
- Add docstrings to functions
- Include type hints where appropriate
- Add comments for complex logic

**YAML/Kubernetes:**
- 2 spaces for indentation
- Comments for non-obvious configurations
- Follow Kubernetes best practices
- Test on actual cluster when possible

**Shell Scripts:**
- Use `#!/bin/bash` shebang
- Add comments explaining each section
- Use `set -e` to fail on errors
- Make scripts executable (`chmod +x`)

**Documentation:**
- Update relevant README files
- Use clear, concise language
- Provide examples
- Test all commands before committing

### Testing Requirements

All code examples must be tested before submission:

1. **Include test instructions** in the chapter README
2. **Provide expected output**
3. **Document prerequisites** (versions, credentials, etc.)
4. **Test on clean environment** if possible

### Code Style

#### Python Example

```python
from spiffe import SpiffeClient
from typing import Optional

def fetch_svid(socket_path: Optional[str] = None) -> str:
    """
    Fetch SVID from SPIRE agent.
    
    Args:
        socket_path: Optional path to SPIRE agent socket
        
    Returns:
        SPIFFE ID as string
        
    Raises:
        RuntimeError: If SVID fetch fails
    """
    client = SpiffeClient(socket_path=socket_path)
    svid = client.fetch_x509_svid()
    return str(svid.spiffe_id)
```

#### Kubernetes YAML Example

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: spire-server
  namespace: spire
data:
  server.conf: |
    # SPIRE server configuration
    server {
      bind_address = "0.0.0.0"
      bind_port = "8081"
      trust_domain = "example.org"
    }
```

### Commit Messages

Use clear, descriptive commit messages:

**Good:**
```
Add JWT-SVID example for Lambda functions
Fix authentication error in LangChain integration
Update Kubernetes manifests to SPIRE 1.8
```

**Bad:**
```
update stuff
fix bug
changes
```

### Documentation Updates

When adding features or examples:

1. Update the chapter README
2. Add configuration examples
3. Include troubleshooting tips
4. Link to relevant book chapters
5. Update main README if needed

### What to Contribute

#### Welcome Contributions:

- Bug fixes in existing code
- Performance improvements
- Additional examples (with documentation)
- Better error handling
- Updated dependencies
- Improved documentation
- Troubleshooting tips

#### Not Accepted:

- Breaking changes without discussion
- Code without tests/documentation
- Proprietary or licensed code
- Examples not related to SPIRE + AI agents

## Code of Conduct

### Our Standards

- Be respectful and professional
- Welcome newcomers
- Accept constructive criticism
- Focus on what's best for the community
- Show empathy towards others

### Unacceptable Behavior

- Harassment or discriminatory language
- Trolling or insulting comments
- Personal or political attacks
- Publishing others' private information
- Unprofessional conduct

## Getting Help

### Questions?

- Open an issue with the "question" label
- Check existing issues for answers
- Review the book for context
- Join [SPIFFE Slack](https://slack.spiffe.io)

### Need Book Context?

Many examples are easier to understand with the full book context:
- [Get the book on Amazon](https://amazon.com/dp/YOUR_ASIN_HERE)
- [Visit RuntimeFence](https://runtimefence.com)

## License

By contributing, you agree that your contributions will be licensed under the Apache License 2.0.

## Recognition

Contributors will be acknowledged in:
- Repository contributors list
- Future book editions (with permission)
- Release notes

## Review Process

1. **Submission:** You submit a PR
2. **Initial Review:** Maintainer reviews within 1 week
3. **Feedback:** Maintainer provides feedback if needed
4. **Revision:** You address feedback
5. **Approval:** Maintainer approves and merges
6. **Release:** Changes included in next release

## Priority for Review

PRs are reviewed in this order:

1. **Critical bugs** (security, data loss)
2. **Bug fixes** (functionality broken)
3. **Documentation** improvements
4. **Enhancements** (new features)
5. **Refactoring** (code improvements)

## Contact

**Repository Maintainer:** David (CCIE #14019)  
**Organization:** RuntimeFence  
**Book:** SPIFFE/SPIRE for AI Agents

---

Thank you for contributing to the SPIRE + AI agents community! 🎉
