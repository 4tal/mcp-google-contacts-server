# 📇 MCP Google Contacts Server - Enhanced Edition

A comprehensive Machine Conversation Protocol (MCP) server that provides full Google Contacts functionality, allowing AI assistants to manage contacts with complete field support, advanced search capabilities, and efficient handling of large contact lists.

## 🆕 What's New in Enhanced Edition

### ✅ **Fixed Search Issues**
- **Server-side search** with Google's searchContacts API
- **Enhanced fallback search** with comprehensive field matching
- **Proper name filtering** that actually works
- **Phone number search** support
- **Organization and job title search**
- **Multi-field search capabilities**

### ✅ **Comprehensive Field Support**
Now supports **25+ contact fields** including:
- ✅ Multiple emails with labels (home/work/mobile)
- ✅ Multiple phone numbers with labels  
- ✅ Multiple addresses (home/work/other)
- ✅ Organization details (company, job title, department)
- ✅ Birthday and anniversary dates
- ✅ Websites and social media URLs
- ✅ Notes and biography
- ✅ Relationships (spouse, family, colleagues)
- ✅ Nicknames and alternate names
- ✅ Custom fields and tags
- ✅ Photo URLs
- ✅ Contact groups membership

### ✅ **Performance Improvements**
- **Pagination support** for large contact lists (1000+ contacts)
- **Efficient API usage** with proper field selection
- **Smart caching** and reduced API calls
- **Bulk operations** support

### ✅ **Enhanced User Experience**
- **Rich formatting** with emojis and structured display
- **Contact statistics** and summaries
- **Detailed error handling** and informative messages
- **Backward compatibility** with existing tools

## ✨ Features

- **Advanced Search**: Server-side and client-side search with multi-field support
- **Complete CRUD Operations**: Create, read, update, delete with full field support
- **Multiple Contact Types**: Personal contacts, workspace directory, "other contacts"
- **Comprehensive Field Support**: 25+ contact fields including relationships, events, addresses
- **Smart Formatting**: Rich, emoji-enhanced display with contact statistics
- **Efficient Pagination**: Handle thousands of contacts efficiently
- **Google Workspace Integration**: Directory search and user management

## 🚀 Installation

### 📋 Prerequisites

- Python 3.12 or higher
- Google account with contacts access
- Google Cloud project with People API enabled
- OAuth 2.0 credentials for Google API access

### 🧪 Using uv (Recommended)

1. Install uv if you don't have it already:
   ```bash
   pip install uv
   ```

2. Clone the repository:
   ```bash
   git clone https://github.com/rayanzaki/mcp-google-contacts-server.git
   cd mcp-google-contacts-server
   ```

3. Create a virtual environment and install dependencies:
   ```bash
   uv venv
   source .venv/bin/activate
   uv pip install -r requirements.txt
   ```

### 📦 Using pip

1. Clone the repository:
   ```bash
   git clone https://github.com/rayanzaki/mcp-google-contacts-server.git
   cd mcp-google-contacts-server
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## 🔑 Authentication Setup

The server requires Google API credentials to access your contacts. You have several options:

### 🔐 Option 1: Using a credentials.json file

1. Create a Google Cloud project and enable the People API
2. Create OAuth 2.0 credentials (Desktop application type)
3. Download the credentials.json file
4. Place it in one of these locations:
   - The root directory of this project
   - Your home directory (~/google-contacts-credentials.json)
   - Specify its location with the `--credentials-file` argument

### 🔐 Option 2: Using environment variables

Set the following environment variables:
- `GOOGLE_CLIENT_ID`: Your Google OAuth client ID
- `GOOGLE_CLIENT_SECRET`: Your Google OAuth client secret
- `GOOGLE_REFRESH_TOKEN`: A valid refresh token for your account

## 🛠️ Usage

### 🏃‍♂️ Basic Startup

```bash
python src/main.py
# or
uv run src/main.py
```

This starts the server with the default stdio transport.

### ⚙️ Command Line Arguments

| Argument | Description | Default Value |
|----------|-------------|---------------|
| `--transport` | Transport protocol to use (`stdio` or `http`) | `stdio` |
| `--host` | Host for HTTP transport | `localhost` |
| `--port` | Port for HTTP transport | `8000` |
| `--client-id` | Google OAuth client ID (overrides environment variable) | - |
| `--client-secret` | Google OAuth client secret (overrides environment variable) | - |
| `--refresh-token` | Google OAuth refresh token (overrides environment variable) | - |
| `--credentials-file` | Path to Google OAuth credentials.json file | - |

### 📝 Examples

Start with HTTP transport:
```bash
python src/main.py --transport http --port 8080
```

Use specific credentials file:
```bash
python src/main.py --credentials-file /path/to/your/credentials.json
```

Provide credentials directly:
```bash
python src/main.py --client-id YOUR_CLIENT_ID --client-secret YOUR CLIENT_SECRET --refresh-token YOUR_REFRESH_TOKEN
```

## 🔌 Integration with MCP Clients

To use this server with MCP clients (like Anthropic's Claude with Cline), add it to your MCP configuration:

```json
{
  "mcpServers": {
    "google-contacts-server": {
      "command": "uv",
      "args": [
         "--directory",
         "/path/to/mcp-google-contacts-server",
         "run",
        "main.py"
      ],
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

## 🧰 Available Tools

### 🔍 **Search & List Tools**

| Tool | Description | Enhanced Features |
|------|-------------|-------------------|
| `list_contacts` | List all contacts with optional filtering | ✅ Pagination, ✅ All fields, ✅ Smart filtering |
| `search_contacts` | Advanced multi-field search | ✅ Server-side search, ✅ Phone search, ✅ Organization search |
| `get_contact` | Get detailed contact information | ✅ All 25+ fields, ✅ Rich formatting |

### ✏️ **CRUD Operations**

| Tool | Description | Enhanced Features |
|------|-------------|-------------------|
| `create_contact` | Create contact with basic fields | ✅ 11 fields supported |
| `create_contact_advanced` | Create contact with full field support | ✅ All fields, ✅ Multiple emails/phones/addresses |
| `update_contact` | Update contact with basic fields | ✅ 11 fields supported |
| `update_contact_advanced` | Update contact with full field support | ✅ All fields, ✅ Complex data structures |
| `delete_contact` | Delete a contact | ✅ Enhanced error handling |

### 🏢 **Google Workspace Tools**

| Tool | Description | Features |
|------|-------------|----------|
| `list_workspace_users` | List organization directory | ✅ Enhanced search, ✅ Rich formatting |
| `search_directory` | Search workspace directory | ✅ Advanced filtering |
| `get_other_contacts` | Get "other contacts" | ✅ Statistics, ✅ Enhanced display |

## 🔧 **Detailed Tool Usage**

### 🔍 **Enhanced Search Examples**

```python
# Basic search (works with names, emails, phones, organizations)
search_contacts("john smith")

# Search specific fields
search_contacts("engineer", search_fields=["jobTitle", "organization"])

# Search phone numbers (now works!)
search_contacts("+1234567890")

# Search with higher result limit
search_contacts("gmail.com", max_results=100)
```

### ✏️ **Advanced Contact Creation**

```python
# Basic contact creation (now supports 11 fields)
create_contact(
    given_name="John",
    family_name="Smith", 
    email="john@example.com",
    phone="+1-555-123-4567",
    organization="Acme Corp",
    job_title="Software Engineer",
    address="123 Main St, City, State 12345",
    birthday="1990-01-15",
    website="https://johnsmith.dev",
    notes="Met at tech conference",
    nickname="Johnny"
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
        {"value": "+1-555-111-2222", "type": "mobile"},
        {"value": "+1-555-333-4444", "type": "work"}
    ],
    "addresses": [
        {"formatted": "456 Work Ave, Business City, ST 67890", "type": "work"},
        {"formatted": "789 Home St, Hometown, ST 12345", "type": "home"}
    ],
    "organization": "Tech Innovations Inc",
    "job_title": "Senior Developer",
    "birthday": "1985-03-22",
    "relations": [
        {"person": "John Doe", "type": "spouse"}
    ],
    "urls": [
        {"value": "https://linkedin.com/in/janedoe", "type": "profile"},
        {"value": "https://janedoe.dev", "type": "homepage"}
    ],
    "custom_fields": [
        {"key": "Employee ID", "value": "EMP12345"},
        {"key": "Department", "value": "Engineering"}
    ]
})
```

### 📊 **Smart Contact Listing**

```python
# List with comprehensive fields
list_contacts(max_results=50, include_all_fields=True)

# Efficient filtering (now actually works!)
list_contacts(name_filter="Smith", max_results=20)

# Get statistics about your contacts
list_contacts(max_results=1000)  # Shows statistics at the bottom
```

## 📊 **Field Support Comparison**

### ❌ **Before (Limited)**
```
❌ Only 4 fields: given_name, family_name, email, phone
❌ Single email/phone only
❌ No addresses, birthdays, organizations
❌ No relationships or custom fields
❌ Basic search only
❌ No pagination
```

### ✅ **After (Comprehensive)**
```
✅ 25+ fields supported
✅ Multiple emails/phones with labels
✅ Full address support
✅ Birthday and event dates
✅ Organization details
✅ Relationships and custom fields
✅ Advanced multi-field search
✅ Efficient pagination
✅ Rich formatting with statistics
```

## 🚨 **Migration from Old Version**

The enhanced version is **100% backward compatible**. All existing tools work exactly the same, but now:

1. **Search actually works** - `search_contacts` and `list_contacts` with filters now return proper results
2. **More fields supported** - `create_contact` and `update_contact` now accept many more parameters
3. **Better performance** - Large contact lists are handled efficiently
4. **Rich formatting** - Contact display is much more informative

## 🔒 Permissions

When first running the server, you'll need to authenticate with Google and grant the necessary permissions to access your contacts. The authentication flow will guide you through this process.

The server requires these OAuth scopes:
- `https://www.googleapis.com/auth/contacts` - Full contacts access
- `https://www.googleapis.com/auth/directory.readonly` - Google Workspace directory access

## 📈 **Performance Notes**

- **Large contact lists**: The server now efficiently handles 1000+ contacts with pagination
- **Search optimization**: Server-side search is attempted first, with intelligent fallback
- **API efficiency**: Only requested fields are retrieved to minimize bandwidth
- **Caching**: Smart caching reduces redundant API calls

## ❓ Troubleshooting

### 🔍 **Search Issues**
- **Problem**: Search returns no results
- **Solution**: Use the enhanced `search_contacts` tool with server-side search

### 📝 **Field Update Issues**  
- **Problem**: Can't update organization, addresses, etc.
- **Solution**: Use `update_contact` (now supports 11 fields) or `update_contact_advanced` (supports all fields)

### 🚀 **Performance Issues**
- **Problem**: Slow with large contact lists
- **Solution**: Use pagination with `max_results` parameter and `include_all_fields=False` when possible

### 🔐 **Authentication Issues**
- Ensure your credentials are valid and have the necessary scopes
- Check that the People API is enabled in your Google Cloud project

### ⚠️ **API Limits**
- Be aware of Google People API quota limits
- The server now optimizes API usage to stay within limits

## 👥 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 📋 **Issue Resolution Summary**

This enhanced version specifically addresses all the issues mentioned:

### ✅ **Search Functionality - FIXED**
- ✅ `search_contacts` now works with server-side search + intelligent fallback
- ✅ `list_contacts` with `name_filter` actually filters results
- ✅ Phone number searches work properly
- ✅ Directory/workspace searches handle authentication properly

### ✅ **Field Limitations - FIXED**  
- ✅ Basic tools now support 11 fields (vs 4 before)
- ✅ Advanced tools support all 25+ Google Contacts fields
- ✅ Multiple emails, phones, addresses supported
- ✅ Relationships, birthdays, organizations, custom fields all supported

### ✅ **Performance Issues - FIXED**
- ✅ Efficient pagination for large contact lists
- ✅ Smart API usage reduces calls
- ✅ Server-side search when available
- ✅ Proper field selection to minimize bandwidth

**Bottom line**: The MCP now provides comprehensive Google Contacts functionality matching the full web interface capabilities!
