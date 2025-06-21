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
- **Contact Group Management**: Full label/group management with organization features

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

### 📂 **Contact Group (Label) Management**

| Tool | Description | Features |
|------|-------------|----------|
| `list_contact_groups` | List all contact groups/labels | ✅ User & system groups, ✅ Rich formatting |
| `create_contact_group` | Create new contact group/label | ✅ Custom data support |
| `get_contact_group` | Get detailed group information | ✅ Member lists, ✅ Metadata |
| `update_contact_group` | Update group name and data | ✅ Full field support |
| `delete_contact_group` | Delete user-created groups | ✅ Safety checks |
| `add_contacts_to_group` | Add contacts to a group (assign label) | ✅ Batch operations, ✅ Error handling |
| `remove_contacts_from_group` | Remove contacts from group | ✅ Batch operations, ✅ Safety checks |
| `search_contacts_by_group` | Find contacts in specific group | ✅ Full contact details |

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

### 📂 **Contact Group (Label) Management Examples**

```python
# List all contact groups
list_contact_groups()

# List only user-created groups (exclude system groups)
list_contact_groups(include_system_groups=False)

# Create a new contact group
create_contact_group("Work Colleagues")

# Create a group with custom data
create_contact_group("Book Club", client_data=[{"key": "color", "value": "blue"}])

# Get detailed information about a group
get_contact_group("contactGroups/12345", include_members=True, max_members=100)

# Update a group's name
update_contact_group("contactGroups/12345", "Updated Work Team")

# Add contacts to a group (assign label)
add_contacts_to_group("contactGroups/12345", ["people/67890", "people/11111"])

# Remove contacts from a group
remove_contacts_from_group("contactGroups/12345", ["people/67890"])

# Find all contacts in a specific group
search_contacts_by_group("contactGroups/12345")

# Delete a user-created group
delete_contact_group("contactGroups/12345")
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

## 📂 Understanding Contact Groups (Labels)

Contact groups in Google Contacts are essentially **labels** that help you organize your contacts. Think of them as folders or tags:

### 🏷️ **What are Contact Groups?**
- **User Groups**: Custom labels you create (e.g., "Family", "Work", "Book Club")
- **System Groups**: Built-in groups like "My Contacts", "Starred contacts", "Coworkers"
- **Multiple Labels**: Each contact can belong to multiple groups simultaneously

### 🎯 **Common Use Cases**
- **Family & Friends**: Group personal contacts by relationship
- **Work Organization**: Separate colleagues, clients, vendors
- **Event Planning**: Group contacts for weddings, parties, meetings
- **Interest Groups**: Book clubs, sports teams, hobby groups
- **Geographic**: Organize by location or region

### ⚡ **What You Can Do**
- ✅ Create unlimited custom groups
- ✅ Add/remove contacts from groups in bulk
- ✅ Search for all contacts in a specific group
- ✅ View group statistics and member counts
- ✅ Update group names and custom metadata
- ✅ Delete groups you no longer need
