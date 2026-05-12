# Code Style & Quality Rules

## General
- Write clean, readable code over clever/tricky code
- Follow the existing code style in the project
- Use meaningful variable and function names
- Keep functions small and focused (single responsibility)
- Add comments only when the "why" is not obvious

## Error Handling
- Always handle errors gracefully; never swallow exceptions silently
- Use specific error types over generic ones
- Log errors with sufficient context for debugging

## Testing
- Write tests alongside implementation code
- Test behavior, not implementation details
- Cover edge cases and error paths, not just happy paths
- Keep tests fast and deterministic

## Security
- Never hardcode secrets, tokens, or passwords
- Validate all user inputs
- Follow least-privilege principle for permissions
- Sanitize data before logging or displaying

## Performance
- Prefer simple algorithms over premature optimization
- Avoid N+1 queries in database access
- Use lazy loading and pagination for large datasets
- Profile before optimizing

## Git
- Write clear commit messages: `type(scope): description`
- Types: feat, fix, refactor, test, docs, chore, style
- Keep commits focused on a single logical change
