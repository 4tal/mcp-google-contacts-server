# 📇 MCP Google Contacts Server

A Machine Conversation Protocol (MCP) server that provides comprehensive Google Contacts functionality for AI assistants.

## ✨ Features

- **Complete Contact Management**: Create, read, update, and delete contacts with 25+ fields
- **Advanced Search**: Multi-field search across names, emails, phones, and organizations
- **Contact Groups**: Full label/group management and organization
- **Google Workspace Integration**: Directory search and user management
- **Efficient Performance**: Pagination support for large contact lists (1000+ contacts)
- **Rich Field Support**: Multiple emails/phones, addresses, birthdays, relationships, custom fields

## 🚀 Installation

### Prerequisites

- Python 3.12 or higher
- Google account with contacts access
- Google Cloud project with People API enabled
- OAuth 2.0 credentials

### Setup

1. **Clone and install:**

   ```bash
   git clone https://github.com/rayanzaki/mcp-google-contacts-server.git
   cd mcp-google-contacts-server
   
   # Using uv (recommended)
   uv venv && source .venv/bin/activate
   uv pip install -r requirements.txt
   
   # Or using pip
   pip install -r requirements.txt
   ```

2. **Set up Google API credentials** (choose one):

   **Option A: Credentials file**
   - Download `credentials.json` from Google Cloud Console
   - Place in project root or specify with `--credentials-file`

   **Option B: Environment variables**

   ```bash
   export GOOGLE_CLIENT_ID="your_client_id"
   export GOOGLE_CLIENT_SECRET="your_client_secret"
   export GOOGLE_REFRESH_TOKEN="your_refresh_token"
   ```

## 🛠️ Usage

### Basic Startup

```bash
python src/main.py
# or
uv run src/main.py
```

### Command Line Options

- `--transport`: Protocol (`stdio` or `http`, default: `stdio`)
- `--host`: HTTP host (default: `localhost`)
- `--port`: HTTP port (default: `8000`)
- `--credentials-file`: Path to credentials.json
- `--client-id`, `--client-secret`, `--refresh-token`: OAuth credentials

### Examples

```bash
# HTTP transport
python src/main.py --transport http --port 8080

# Specific credentials file
python src/main.py --credentials-file /path/to/credentials.json
```

## 🔌 MCP Client Integration

Add to your MCP configuration:

```json
{
  "mcpServers": {
    "google-contacts-server": {
      "command": "uv",
      "args": [
        "--directory", "/path/to/mcp-google-contacts-server",
        "run", "main.py"
      ]
    }
  }
}
```

## 🧰 Available Tools

### Contact Management

- **`list_contacts`** - List all contacts with filtering and pagination
- **`search_contacts`** - Advanced multi-field search
- **`get_contact`** - Get detailed contact information
- **`create_contact`** - Create contact with basic fields (11 fields)
- **`create_contact_advanced`** - Create contact with all fields (25+ fields)
- **`update_contact`** - Update contact with basic fields
- **`update_contact_advanced`** - Update contact with all fields
- **`delete_contact`** - Delete a contact

### Contact Groups (Labels)

- **`list_contact_groups`** - List all contact groups/labels
- **`create_contact_group`** - Create new contact group
- **`get_contact_group`** - Get group details and members
- **`update_contact_group`** - Update group name
- **`delete_contact_group`** - Delete user-created groups
- **`add_contacts_to_group`** - Add contacts to a group
- **`remove_contacts_from_group`** - Remove contacts from group
- **`search_contacts_by_group`** - Find contacts in specific group

### Google Workspace

- **`list_workspace_users`** - List organization directory
- **`search_directory`** - Search workspace directory
- **`get_other_contacts`** - Get "other contacts"

## 📝 Quick Examples

### Search Contacts

```python
# Basic search
search_contacts("john smith")

# Search specific fields
search_contacts("engineer", search_fields=["jobTitle", "organization"])

# Search phone numbers
search_contacts("+1234567890")
```

### Create Contact

```python
# Basic contact
create_contact(
    given_name="John",
    family_name="Smith",
    email="john@example.com",
    phone="+1-555-123-4567",
    organization="Acme Corp",
    job_title="Software Engineer"
)

# Advanced contact with multiple fields
create_contact_advanced({
    "given_name": "Jane",
    "family_name": "Doe",
    "emails": [
        {"value": "jane@work.com", "type": "work"},
        {"value": "jane@personal.com", "type": "home"}
    ],
    "phones": [
        {"value": "+1-555-111-2222", "type": "mobile"}
    ],
    "organization": "Tech Corp",
    "birthday": "1985-03-22"
})
```

### Manage Contact Groups

```python
# Create group
create_contact_group("Work Team")

# Add contacts to group
add_contacts_to_group("contactGroups/12345", ["people/67890", "people/11111"])

# Find contacts in group
search_contacts_by_group("contactGroups/12345")
```

## ❓ Troubleshooting

### Authentication Issues

- Ensure People API is enabled in Google Cloud Console
- Check OAuth credentials are valid and have proper scopes
- Required scopes: `contacts` and `directory.readonly`

### Search Not Working

- Use server-side search with `search_contacts`
- Try different search terms or fields

### Performance Issues

- Use pagination with `max_results` parameter
- Set `include_all_fields=False` for faster queries

## 🔧 Development

```bash
# Development setup
uv sync --dev

# Format code
./scripts/format.sh

# Run linting
./scripts/lint.sh

# Test
uv run python test_contact_groups.py
```

## 📄 License

MIT License - see LICENSE file for details.

---

**Note**: This server provides comprehensive Google Contacts functionality with support for all contact fields, advanced search, contact groups, and efficient handling of large contact lists.
