#!/usr/bin/env python3
"""
Test script for Contact Groups functionality in MCP Google Contacts Server
This script demonstrates the new label/group management features.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from google_contacts_service import GoogleContactsService
from formatters import format_contact_groups_list, format_contact_group, format_group_membership_result

def test_contact_groups():
    """Test contact groups functionality."""
    print("🧪 Testing Contact Groups Functionality\n")
    
    try:
        # Initialize service
        print("🔑 Initializing Google Contacts service...")
        service = GoogleContactsService.from_env()
        print("✅ Service initialized successfully!\n")
        
        # Test 1: List existing contact groups
        print("📂 Test 1: Listing existing contact groups...")
        groups = service.list_contact_groups()
        print(format_contact_groups_list(groups))
        print("\n" + "="*50 + "\n")
        
        # Test 2: Create a new contact group
        print("🆕 Test 2: Creating a new contact group...")
        new_group = service.create_contact_group(
            "MCP Test Group", 
            client_data=[{"key": "created_by", "value": "mcp_test_script"}]
        )
        print("✅ Created new group!")
        print(format_contact_group(new_group))
        print("\n" + "="*50 + "\n")
        
        # Test 3: Get the created group details
        print("📋 Test 3: Getting group details...")
        group_details = service.get_contact_group(new_group['resourceName'], max_members=10)
        print(format_contact_group(group_details))
        print("\n" + "="*50 + "\n")
        
        # Test 4: Update the group name
        print("✏️ Test 4: Updating group name...")
        updated_group = service.update_contact_group(
            new_group['resourceName'],
            "MCP Test Group (Updated)",
            client_data=[{"key": "updated_by", "value": "mcp_test_script"}]
        )
        print("✅ Updated group!")
        print(format_contact_group(updated_group))
        print("\n" + "="*50 + "\n")
        
        # Test 5: Clean up - delete the test group
        print("🗑️ Test 5: Cleaning up - deleting test group...")
        result = service.delete_contact_group(new_group['resourceName'])
        if result.get('success'):
            print("✅ Test group deleted successfully!")
        else:
            print("❌ Failed to delete test group")
        print("\n" + "="*50 + "\n")
        
        print("🎉 All contact group tests completed successfully!")
        
    except Exception as e:
        print(f"❌ Error during testing: {str(e)}")
        import traceback
        traceback.print_exc()

def demo_usage_examples():
    """Demonstrate common usage patterns."""
    print("\n📚 Contact Groups Usage Examples:\n")
    
    examples = [
        "# List all contact groups",
        "list_contact_groups()",
        "",
        "# Create a new group for work colleagues",
        "create_contact_group('Work Team')",
        "",
        "# Get group details with member list",
        "get_contact_group('contactGroups/12345', include_members=True)",
        "",
        "# Add contacts to a group",
        "add_contacts_to_group('contactGroups/12345', ['people/67890', 'people/11111'])",
        "",
        "# Find all contacts in a specific group",
        "search_contacts_by_group('contactGroups/12345')",
        "",
        "# Remove contacts from a group",
        "remove_contacts_from_group('contactGroups/12345', ['people/67890'])",
    ]
    
    for example in examples:
        if example.startswith("#"):
            print(f"💡 {example}")
        elif example == "":
            print()
        else:
            print(f"   {example}")

if __name__ == "__main__":
    # Show usage examples first
    demo_usage_examples()
    
    # Ask user if they want to run live tests
    print("\n" + "="*60)
    response = input("\n🤔 Do you want to run live tests with your Google account? (y/N): ")
    
    if response.lower() in ['y', 'yes']:
        test_contact_groups()
    else:
        print("👍 Skipping live tests. The examples above show how to use the new features!") 