# TOOLS.md - Local Notes

Skills define *how* tools work. This file is for *your* specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:
- API keys and services you use
- SSH hosts and aliases  
- Project-specific configurations
- Environment-specific notes
- Anything unique to your setup

## Examples

```markdown
### API Services
- Weather API: OpenWeatherMap (key in env)
- Search: Serper (key in env)

### SSH
- home-server → 192.168.1.100, user: admin

### Projects
- Main project: ~/projects/my-app
- Documentation: ~/docs
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

## Authenticated Services

Skills that connect to external APIs or CLIs use credentials managed through the `credentials` tool.

### HTTP APIs (curl)
Use `{{credential:NAME}}` as a placeholder for credential values in curl commands:

    curl -s https://api.example.com/endpoint \
      -H "Authorization: Bearer {{credential:my-api}}" \
      -d '{"query": "hello"}'

The placeholder is securely resolved at execution time. Credentials are bound to their registered base URL — they can only be used in curl commands targeting that URL.

For complex API processing, use curl for the authenticated call and pipe to python for processing:

    curl -s https://api.example.com/data \
      -H "Authorization: Bearer {{credential:my-api}}" | \
      python3 -c "import json, sys; data = json.load(sys.stdin); print(data['result'])"

### CLI Tools
CLI credentials are injected automatically as environment variables. When you run a registered CLI command, the credential is available in the configured env var without any special syntax.

---

Add whatever helps you do your job. This is your cheat sheet.
