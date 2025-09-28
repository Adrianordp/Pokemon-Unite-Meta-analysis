**Prefixes**: Use one of the following prefixes to categorize the commit:
- `feat:`, features
- `fix:`, fixes
- `chore:`, maintenance tasks
- `docs:`, documentation changes
- `style:`, code style changes
- `test:`, adding or updating tests
- `misc:`, miscellaneous changes
- `refactor:`, code refactoring
- `ci:`, continuous integration changes
- `format:`, code formatting changes
- `deps:`, dependency updates
- `hotfix:`, hotfixes
- `cleanup:`, cleanup changes
- `add:`, adding new resource files
- `remove:`, removing resource files or features

**Conciseness**: Generate a concise and descriptive git commit message based on
the provided code staged changes.

**Imperative Mood**: Use the imperative mood (e.g., 'Add feature', 'Fix bug').

**Length**: Keep the message under 50 characters if possible.

**Single File**: Include the relative file path of the file. Example:
`prefix[src/util/log.py]: message`.

**Multiple Files**: Include dots in the path instead. Example: `prefix[...]: message`.

**Staged Files**: Consider only files that are staged for commit.