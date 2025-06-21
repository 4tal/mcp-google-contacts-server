"""MCP tools implementation for Google Contacts."""
import asyncio
from typing import Dict, List, Optional, Any, Union
from mcp.server.fastmcp import FastMCP
import traceback

from google_contacts_service import GoogleContactsService, GoogleContactsError
from formatters import format_contact, format_contacts_list, format_directory_people
from config import config

# Global service instance
contacts_service = None

def init_service() -> Optional[GoogleContactsService]:
    """Initialize and return a Google Contacts service instance.
    
    Returns:
        GoogleContactsService instance or None if initialization fails
    """
    global contacts_service
    
    if contacts_service:
        return contacts_service
    
    try:
        # First try environment variables
        try:
            contacts_service = GoogleContactsService.from_env()
            print("Successfully loaded credentials from environment variables.")
            return contacts_service
        except GoogleContactsError:
            pass
            
        # Then try default file locations
        for path in config.credentials_paths:
            if path.exists():
                try:
                    print(f"Found credentials file at {path}")
                    contacts_service = GoogleContactsService.from_file(path)
                    print("Successfully loaded credentials from file.")
                    return contacts_service
                except GoogleContactsError as e:
                    print(f"Error with credentials at {path}: {e}")
                    continue
                
        print("No valid credentials found. Please provide credentials to use Google Contacts.")
        return None
        
    except Exception as e:
        print(f"Error initializing Google Contacts service: {str(e)}")
        traceback.print_exc()
        return None

def register_tools(mcp: FastMCP) -> None:
    """Register all Google Contacts tools with the MCP server.
    
    Args:
        mcp: FastMCP server instance
    """
    
    @mcp.tool()
    async def list_contacts(name_filter: Optional[str] = None, max_results: int = 100, 
                           include_all_fields: bool = False) -> str:
        """List all contacts or filter by name with comprehensive field support.
        
        Args:
            name_filter: Optional filter to find contacts by name
            max_results: Maximum number of results to return (default: 100)
            include_all_fields: Whether to include all contact fields like addresses, birthdays, etc.
        """
        service = init_service()
        if not service:
            return "Error: Google Contacts service is not available. Please check your credentials."
        
        try:
            contacts = service.list_contacts(name_filter, max_results, include_all_fields)
            return format_contacts_list(contacts)
        except Exception as e:
            return f"Error: Failed to list contacts - {str(e)}"

    @mcp.tool()
    async def search_contacts(query: str, max_results: int = 50, 
                             search_fields: Optional[List[str]] = None) -> str:
        """Enhanced search contacts by name, email, phone, organization, or other fields.
        
        This uses server-side search when available and falls back to comprehensive client-side search.
        
        Args:
            query: Search term to find in contacts
            max_results: Maximum number of results to return (default: 50)
            search_fields: Specific fields to search in (e.g., ['emails', 'phones', 'organization'])
        """
        service = init_service()
        if not service:
            return "Error: Google Contacts service is not available. Please check your credentials."
        
        try:
            contacts = service.search_contacts(query, max_results, search_fields)
            
            if not contacts:
                return f"No contacts found matching '{query}'."
                
            return f"Search results for '{query}':\n\n{format_contacts_list(contacts)}"
        except Exception as e:
            return f"Error: Failed to search contacts - {str(e)}"

    @mcp.tool()
    async def get_contact(identifier: str, include_all_fields: bool = True) -> str:
        """Get a contact by resource name or email with comprehensive information.
        
        Args:
            identifier: Resource name (people/*) or email address of the contact
            include_all_fields: Whether to include all contact fields (default: True)
        """
        service = init_service()
        if not service:
            return "Error: Google Contacts service is not available. Please check your credentials."
        
        try:
            contact = service.get_contact(identifier, include_all_fields)
            return format_contact(contact)
        except Exception as e:
            return f"Error: Failed to get contact - {str(e)}"

    @mcp.tool()
    async def create_contact(given_name: str, family_name: Optional[str] = None, 
                           email: Optional[str] = None, phone: Optional[str] = None,
                           organization: Optional[str] = None, job_title: Optional[str] = None,
                           address: Optional[str] = None, birthday: Optional[str] = None,
                           website: Optional[str] = None, notes: Optional[str] = None,
                           nickname: Optional[str] = None) -> str:
        """Create a new contact with comprehensive field support.
        
        Args:
            given_name: First name of the contact
            family_name: Last name of the contact
            email: Email address of the contact
            phone: Phone number of the contact
            organization: Company/organization name
            job_title: Job title or position
            address: Physical address
            birthday: Birthday in YYYY-MM-DD format
            website: Website URL
            notes: Notes or biography
            nickname: Nickname
        """
        service = init_service()
        if not service:
            return "Error: Google Contacts service is not available. Please check your credentials."
        
        try:
            contact_data = {
                'given_name': given_name
            }
            
            # Add optional fields if provided
            if family_name:
                contact_data['family_name'] = family_name
            if email:
                contact_data['email'] = email
            if phone:
                contact_data['phone'] = phone
            if organization:
                contact_data['organization'] = organization
            if job_title:
                contact_data['job_title'] = job_title
            if address:
                contact_data['address'] = address
            if birthday:
                contact_data['birthday'] = birthday
            if website:
                contact_data['website'] = website
            if notes:
                contact_data['notes'] = notes
            if nickname:
                contact_data['nickname'] = nickname
            
            contact = service.create_contact(contact_data)
            return f"Contact created successfully!\n\n{format_contact(contact)}"
        except Exception as e:
            return f"Error: Failed to create contact - {str(e)}"

    @mcp.tool()
    async def create_contact_advanced(contact_data: Dict[str, Any]) -> str:
        """Create a new contact with full field support including multiple emails, phones, addresses, etc.
        
        Args:
            contact_data: Dictionary containing complete contact information with support for:
                - Multiple emails: {"emails": [{"value": "email@example.com", "type": "work"}]}
                - Multiple phones: {"phones": [{"value": "+1234567890", "type": "mobile"}]}
                - Multiple addresses: {"addresses": [{"formatted": "123 Main St", "type": "home"}]}
                - Relations: {"relations": [{"person": "John Doe", "type": "spouse"}]}
                - Events: {"events": [{"date": {"month": 12, "day": 25}, "type": "anniversary"}]}
                - Custom fields: {"custom_fields": [{"key": "Department", "value": "Engineering"}]}
        """
        service = init_service()
        if not service:
            return "Error: Google Contacts service is not available. Please check your credentials."
        
        try:
            contact = service.create_contact(contact_data)
            return f"Advanced contact created successfully!\n\n{format_contact(contact)}"
        except Exception as e:
            return f"Error: Failed to create advanced contact - {str(e)}"

    @mcp.tool()
    async def update_contact(resource_name: str, given_name: Optional[str] = None, 
                           family_name: Optional[str] = None, email: Optional[str] = None,
                           phone: Optional[str] = None, organization: Optional[str] = None,
                           job_title: Optional[str] = None, address: Optional[str] = None,
                           birthday: Optional[str] = None, website: Optional[str] = None,
                           notes: Optional[str] = None, nickname: Optional[str] = None) -> str:
        """Update an existing contact with comprehensive field support.
        
        Args:
            resource_name: Contact resource name (people/*)
            given_name: Updated first name
            family_name: Updated last name
            email: Updated email address
            phone: Updated phone number
            organization: Updated company/organization name
            job_title: Updated job title or position
            address: Updated physical address
            birthday: Updated birthday in YYYY-MM-DD format
            website: Updated website URL
            notes: Updated notes or biography
            nickname: Updated nickname
        """
        service = init_service()
        if not service:
            return "Error: Google Contacts service is not available. Please check your credentials."
        
        try:
            contact_data = {}
            
            # Add fields that are being updated
            if given_name is not None:
                contact_data['given_name'] = given_name
            if family_name is not None:
                contact_data['family_name'] = family_name
            if email is not None:
                contact_data['email'] = email
            if phone is not None:
                contact_data['phone'] = phone
            if organization is not None:
                contact_data['organization'] = organization
            if job_title is not None:
                contact_data['job_title'] = job_title
            if address is not None:
                contact_data['address'] = address
            if birthday is not None:
                contact_data['birthday'] = birthday
            if website is not None:
                contact_data['website'] = website
            if notes is not None:
                contact_data['notes'] = notes
            if nickname is not None:
                contact_data['nickname'] = nickname
            
            if not contact_data:
                return "Error: No fields provided for update."
            
            contact = service.update_contact(resource_name, contact_data)
            return f"Contact updated successfully!\n\n{format_contact(contact)}"
        except Exception as e:
            return f"Error: Failed to update contact - {str(e)}"

    @mcp.tool()
    async def update_contact_advanced(resource_name: str, contact_data: Dict[str, Any]) -> str:
        """Update an existing contact with full field support including multiple emails, phones, addresses, etc.
        
        Args:
            resource_name: Contact resource name (people/*)
            contact_data: Dictionary containing updated contact information with full field support
        """
        service = init_service()
        if not service:
            return "Error: Google Contacts service is not available. Please check your credentials."
        
        try:
            contact = service.update_contact(resource_name, contact_data)
            return f"Advanced contact updated successfully!\n\n{format_contact(contact)}"
        except Exception as e:
            return f"Error: Failed to update advanced contact - {str(e)}"

    @mcp.tool()
    async def delete_contact(resource_name: str) -> str:
        """Delete a contact by resource name.
        
        Args:
            resource_name: Contact resource name (people/*) to delete
        """
        service = init_service()
        if not service:
            return "Error: Google Contacts service is not available. Please check your credentials."
        
        try:
            result = service.delete_contact(resource_name)
            if result.get('success'):
                return f"Contact {resource_name} deleted successfully."
            else:
                return f"Failed to delete contact: {result.get('message', 'Unknown error')}"
        except Exception as e:
            return f"Error: Failed to delete contact - {str(e)}"

    @mcp.tool()
    async def list_workspace_users(query: Optional[str] = None, max_results: int = 50) -> str:
        """List Google Workspace users in your organization's directory.
        
        This tool allows you to search and list users in your Google Workspace directory,
        including their email addresses and other information.
        
        Args:
            query: Optional search term to find specific users (name, email, etc.)
            max_results: Maximum number of results to return (default: 50)
        """
        service = init_service()
        if not service:
            return "Error: Google Contacts service is not available. Please check your credentials."
        
        try:
            workspace_users = service.list_directory_people(query=query, max_results=max_results)
            return format_directory_people(workspace_users, query)
        except Exception as e:
            return f"Error: Failed to list Google Workspace users - {str(e)}"

    @mcp.tool()
    async def search_directory(query: str, max_results: int = 20) -> str:
        """Search for people specifically in the Google Workspace directory.
        
        This performs a more targeted search of your organization's directory.
        
        Args:
            query: Search term to find specific directory members
            max_results: Maximum number of results to return (default: 20)
        """
        service = init_service()
        if not service:
            return "Error: Google Contacts service is not available. Please check your credentials."
        
        try:
            results = service.search_directory(query, max_results)
            return format_directory_people(results, query)
        except Exception as e:
            return f"Error: Failed to search directory - {str(e)}"

    @mcp.tool()
    async def get_other_contacts(max_results: int = 50) -> str:
        """Retrieve contacts from the 'Other contacts' section.
        
        Other contacts are people you've interacted with but haven't added to your contacts list.
        These often include email correspondents that aren't in your main contacts.
        
        Args:
            max_results: Maximum number of results to return (default: 50)
        """
        service = init_service()
        if not service:
            return "Error: Google Contacts service is not available. Please check your credentials."
        
        try:
            other_contacts = service.get_other_contacts(max_results)
            
            if not other_contacts:
                return "No 'Other contacts' found in your Google account."
            
            # Count how many have email addresses
            with_email = sum(1 for c in other_contacts if c.get('email'))
            
            # Format and return the results
            formatted_list = format_contacts_list(other_contacts)
            return f"Other Contacts (people you've interacted with but haven't added):\n\n{formatted_list}\n\n{with_email} of these contacts have email addresses."
        except Exception as e:
            return f"Error: Failed to retrieve other contacts - {str(e)}"
