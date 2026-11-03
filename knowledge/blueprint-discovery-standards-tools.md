# Blueprint Standards

> Auto-maintained by the ai_session_skills background writer. One `###` entry
> per distinct action. `sig` comments are dedupe keys — never delete them.

## File editing

### Edit a standards file in place
<!-- sig: 536d888424b9 -->

```bash
'BLUEPRINT_DISCOVERY_STANDARDS_FILENAME'
1)
```

- **What it does:** This command uses a specific script to edit a standards file in place, allowing for validation against local models.
- **Why:** It provides a controlled way to modify standards files while ensuring that comments and validation logic are preserved during the edit.
- **Example:** The command is executed when running the script to edit standards.py or standards.yaml.
- **Notes:** The script interacts with a local model specified by BLUEPRINT_OLLAMA_MODEL to validate rules against the repository profile.
