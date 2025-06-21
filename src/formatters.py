from typing import Any, Dict, List, Optional, Union


def format_contact(contact: Dict[str, Any]) -> str:
    """Format a contact dictionary into a readable string with comprehensive field support.

    Args:
        contact: Dictionary containing contact information

    Returns:
        Formatted string representation of the contact
    """
    if not contact:
        return "No contact data available"

    if "status" in contact and contact["status"] == "error":
        return f"Error: {contact.get('message', 'Unknown error')}"

    parts = []

    # Name information
    if "displayName" in contact and contact["displayName"]:
        parts.append(f"📝 Name: {contact['displayName']}")
    elif "givenName" in contact or "familyName" in contact:
        name_parts = []
        if contact.get("givenName"):
            name_parts.append(contact["givenName"])
        if contact.get("familyName"):
            name_parts.append(contact["familyName"])
        if name_parts:
            parts.append(f"📝 Name: {' '.join(name_parts)}")

    # Nickname
    if contact.get("nickname"):
        parts.append(f"🏷️  Nickname: {contact['nickname']}")

    # Contact information
    if contact.get("emails"):
        if isinstance(contact["emails"], list):
            email_parts = []
            for email in contact["emails"]:
                if isinstance(email, dict):
                    label = email.get("label", email.get("type", ""))
                    label_text = f" ({label})" if label else ""
                    email_parts.append(f"   • {email.get('value', '')}{label_text}")
                else:
                    email_parts.append(f"   • {email}")
            parts.append(f"📧 Email(s):\n" + "\n".join(email_parts))
    elif contact.get("email"):
        parts.append(f"📧 Email: {contact['email']}")

    if contact.get("phones"):
        if isinstance(contact["phones"], list):
            phone_parts = []
            for phone in contact["phones"]:
                if isinstance(phone, dict):
                    label = phone.get("label", phone.get("type", ""))
                    label_text = f" ({label})" if label else ""
                    phone_parts.append(f"   • {phone.get('value', '')}{label_text}")
                else:
                    phone_parts.append(f"   • {phone}")
            parts.append(f"📱 Phone(s):\n" + "\n".join(phone_parts))
    elif contact.get("phone"):
        parts.append(f"📱 Phone: {contact['phone']}")

    # Professional information
    if contact.get("organization") or contact.get("jobTitle") or contact.get("department"):
        org_parts = []
        if contact.get("organization"):
            org_parts.append(f"Company: {contact['organization']}")
        if contact.get("jobTitle"):
            org_parts.append(f"Title: {contact['jobTitle']}")
        if contact.get("department"):
            org_parts.append(f"Department: {contact['department']}")
        parts.append(f"🏢 Work:\n   • " + "\n   • ".join(org_parts))

    # Addresses
    if contact.get("addresses"):
        if isinstance(contact["addresses"], list):
            addr_parts = []
            for addr in contact["addresses"]:
                if isinstance(addr, dict):
                    formatted_addr = addr.get("formatted", "")
                    addr_type = addr.get("type", addr.get("label", ""))
                    type_text = f" ({addr_type})" if addr_type else ""
                    addr_parts.append(f"   • {formatted_addr}{type_text}")
                else:
                    addr_parts.append(f"   • {addr}")
            parts.append(f"🏠 Address(es):\n" + "\n".join(addr_parts))

    # Birthday
    if contact.get("birthday"):
        birthday = contact["birthday"]
        if isinstance(birthday, dict):
            year = birthday.get("year", "")
            month = birthday.get("month", "")
            day = birthday.get("day", "")
            if year and month and day:
                parts.append(f"🎂 Birthday: {year}-{month:02d}-{day:02d}")
            elif month and day:
                parts.append(f"🎂 Birthday: {month:02d}-{day:02d}")
        else:
            parts.append(f"🎂 Birthday: {birthday}")

    # Websites/URLs
    if contact.get("urls"):
        if isinstance(contact["urls"], list):
            url_parts = []
            for url in contact["urls"]:
                if isinstance(url, dict):
                    url_value = url.get("value", "")
                    url_type = url.get("type", url.get("label", ""))
                    type_text = f" ({url_type})" if url_type else ""
                    url_parts.append(f"   • {url_value}{type_text}")
                else:
                    url_parts.append(f"   • {url}")
            parts.append(f"🌐 Website(s):\n" + "\n".join(url_parts))

    # Notes/Biography
    if contact.get("notes"):
        notes = contact["notes"]
        # Truncate very long notes
        if len(notes) > 200:
            notes = notes[:200] + "..."
        parts.append(f"📝 Notes: {notes}")

    # Relations
    if contact.get("relations"):
        if isinstance(contact["relations"], list):
            rel_parts = []
            for relation in contact["relations"]:
                if isinstance(relation, dict):
                    person = relation.get("person", "")
                    rel_type = relation.get("type", relation.get("label", ""))
                    type_text = f" ({rel_type})" if rel_type else ""
                    rel_parts.append(f"   • {person}{type_text}")
                else:
                    rel_parts.append(f"   • {relation}")
            parts.append(f"👥 Relations:\n" + "\n".join(rel_parts))

    # Events
    if contact.get("events"):
        if isinstance(contact["events"], list):
            event_parts = []
            for event in contact["events"]:
                if isinstance(event, dict):
                    event_type = event.get("type", event.get("label", "Event"))
                    event_date = event.get("date", {})
                    if isinstance(event_date, dict):
                        month = event_date.get("month", "")
                        day = event_date.get("day", "")
                        year = event_date.get("year", "")
                        if month and day:
                            date_str = f"{month:02d}-{day:02d}"
                            if year:
                                date_str = f"{year}-{date_str}"
                            event_parts.append(f"   • {event_type}: {date_str}")
                    else:
                        event_parts.append(f"   • {event_type}: {event_date}")
                else:
                    event_parts.append(f"   • {event}")
            if event_parts:
                parts.append(f"📅 Events:\n" + "\n".join(event_parts))

    # Custom fields
    if contact.get("customFields"):
        if isinstance(contact["customFields"], list):
            custom_parts = []
            for field in contact["customFields"]:
                if isinstance(field, dict):
                    key = field.get("key", "")
                    value = field.get("value", "")
                    if key and value:
                        custom_parts.append(f"   • {key}: {value}")
            if custom_parts:
                parts.append(f"🔧 Custom Fields:\n" + "\n".join(custom_parts))

    # Contact groups
    if contact.get("groups"):
        group_count = len(contact["groups"])
        if group_count > 0:
            parts.append(f"📂 Groups: {group_count} group(s)")

    # Photo
    if contact.get("photoUrl"):
        parts.append(f"📷 Photo: Available")

    # Resource ID for reference
    if contact.get("resourceName"):
        parts.append(f"🔗 ID: {contact['resourceName']}")

    return "\n".join(parts) if parts else "Contact has no details"


def format_contacts_list(contacts: List[Dict[str, Any]]) -> str:
    """Format a list of contacts into a readable string with enhanced display.

    Args:
        contacts: List of contact dictionaries

    Returns:
        Formatted string representation of the contacts list
    """
    if not contacts:
        return "No contacts found."

    if isinstance(contacts, dict) and "status" in contacts and contacts["status"] == "error":
        return f"Error: {contacts.get('message', 'Unknown error')}"

    parts = []

    for i, contact in enumerate(contacts, 1):
        # Create a compact summary for lists
        contact_summary = _format_contact_summary(contact, i)
        parts.append(contact_summary)
        parts.append("")  # Add blank line between contacts

    summary = f"📊 Found {len(contacts)} contact(s)"

    # Add statistics
    stats = _calculate_contact_stats(contacts)
    if stats:
        summary += f"\n📈 Statistics: {stats}"

    parts.append("=" * 50)
    parts.append(summary)

    return "\n".join(parts)


def _format_contact_summary(contact: Dict[str, Any], index: int) -> str:
    """Format a single contact as a summary for list display."""
    summary_parts = [f"Contact {index}:"]

    # Name
    name = (
        contact.get("displayName")
        or f"{contact.get('givenName', '')} {contact.get('familyName', '')}".strip()
    )
    if name:
        summary_parts.append(f"  📝 {name}")

    # Primary email
    if contact.get("emails") and isinstance(contact["emails"], list):
        primary_email = contact["emails"][0]
        if isinstance(primary_email, dict):
            summary_parts.append(f"  📧 {primary_email.get('value', '')}")
    elif contact.get("email"):
        summary_parts.append(f"  📧 {contact['email']}")

    # Primary phone
    if contact.get("phones") and isinstance(contact["phones"], list):
        primary_phone = contact["phones"][0]
        if isinstance(primary_phone, dict):
            summary_parts.append(f"  📱 {primary_phone.get('value', '')}")
    elif contact.get("phone"):
        summary_parts.append(f"  📱 {contact['phone']}")

    # Organization
    if contact.get("organization"):
        job_title = contact.get("jobTitle", "")
        org_text = f"{contact['organization']}"
        if job_title:
            org_text += f" - {job_title}"
        summary_parts.append(f"  🏢 {org_text}")

    return "\n".join(summary_parts)


def _calculate_contact_stats(contacts: List[Dict[str, Any]]) -> str:
    """Calculate and return statistics about the contacts list."""
    if not contacts:
        return ""

    stats = []

    # Count contacts with emails
    with_email = sum(
        1 for c in contacts if c.get("email") or (c.get("emails") and len(c["emails"]) > 0)
    )
    if with_email > 0:
        stats.append(f"{with_email} with email")

    # Count contacts with phones
    with_phone = sum(
        1 for c in contacts if c.get("phone") or (c.get("phones") and len(c["phones"]) > 0)
    )
    if with_phone > 0:
        stats.append(f"{with_phone} with phone")

    # Count contacts with organizations
    with_org = sum(1 for c in contacts if c.get("organization"))
    if with_org > 0:
        stats.append(f"{with_org} with organization")

    # Count contacts with addresses
    with_addr = sum(1 for c in contacts if c.get("addresses") and len(c["addresses"]) > 0)
    if with_addr > 0:
        stats.append(f"{with_addr} with addresses")

    return ", ".join(stats)


def format_directory_people(people: List[Dict[str, Any]], query: Optional[str] = None) -> str:
    """Format a list of directory people into a readable string with enhanced display.

    Args:
        people: List of directory people dictionaries
        query: Optional search query used to find these people

    Returns:
        Formatted string representation of the directory people
    """
    if not people:
        if query:
            return f"No directory members found matching '{query}'."
        return "No directory members found."

    # Count how many users have emails
    users_with_email = sum(
        1
        for user in people
        if user.get("email") or (user.get("emails") and len(user["emails"]) > 0)
    )

    # Format the results
    formatted_users = []
    for i, user in enumerate(people, 1):
        user_parts = []
        user_parts.append(f"📁 Directory Member {i}:")

        # Name
        if user.get("displayName"):
            user_parts.append(f"  📝 Name: {user['displayName']}")

        # Email
        if user.get("emails") and isinstance(user["emails"], list):
            primary_email = user["emails"][0]
            if isinstance(primary_email, dict):
                user_parts.append(f"  📧 Email: {primary_email.get('value', '')}")
        elif user.get("email"):
            user_parts.append(f"  📧 Email: {user['email']}")

        # Organization info
        if user.get("organization"):
            user_parts.append(f"  🏢 Organization: {user['organization']}")
        if user.get("department"):
            user_parts.append(f"  🏛️  Department: {user['department']}")
        if user.get("jobTitle"):
            user_parts.append(f"  💼 Title: {user['jobTitle']}")

        # Phone
        if user.get("phones") and isinstance(user["phones"], list):
            primary_phone = user["phones"][0]
            if isinstance(primary_phone, dict):
                user_parts.append(f"  📱 Phone: {primary_phone.get('value', '')}")
        elif user.get("phone"):
            user_parts.append(f"  📱 Phone: {user['phone']}")

        # Resource ID
        if user.get("resourceName"):
            user_parts.append(f"  🔗 ID: {user['resourceName']}")

        formatted_users.append("\n".join(user_parts))

    query_part = f" matching '{query}'" if query else ""
    summary = f"📊 Found {len(people)} directory member(s){query_part}. {users_with_email} have email addresses."
    formatted_users.append("=" * 50)
    formatted_users.append(summary)

    return "\n\n".join(formatted_users)


def format_contact_group(group: Dict[str, Any]) -> str:
    """Format a contact group dictionary into a readable string.

    Args:
        group: Dictionary containing contact group information

    Returns:
        Formatted string representation of the contact group
    """
    if not group:
        return "No contact group data available"

    parts = []

    # Group name and type
    name = group.get("name", "Unnamed Group")
    group_type = group.get("groupType", "").replace("_", " ").title()
    if group_type:
        parts.append(f"📂 {name} ({group_type})")
    else:
        parts.append(f"📂 {name}")

    # Member count
    member_count = group.get("memberCount", 0)
    if member_count > 0:
        parts.append(f"👥 Members: {member_count}")
    else:
        parts.append(f"👥 Members: None")

    # Update time
    if group.get("updateTime"):
        parts.append(f"🕒 Last Updated: {group['updateTime']}")

    # Resource ID
    if group.get("resourceName"):
        parts.append(f"🔗 ID: {group['resourceName']}")

    # Client data
    if group.get("clientData"):
        client_data_parts = []
        for data in group["clientData"]:
            key = data.get("key", "")
            value = data.get("value", "")
            if key and value:
                client_data_parts.append(f"   • {key}: {value}")
        if client_data_parts:
            parts.append(f"🔧 Custom Data:\n" + "\n".join(client_data_parts))

    # Member resource names (if included)
    if group.get("memberResourceNames"):
        member_names = group["memberResourceNames"]
        if len(member_names) <= 5:
            parts.append(f"📋 Member IDs: {', '.join(member_names)}")
        else:
            parts.append(
                f"📋 Member IDs: {', '.join(member_names[:5])} ... (and {len(member_names) - 5} more)"
            )

    return "\n".join(parts)


def format_contact_groups_list(groups: List[Dict[str, Any]]) -> str:
    """Format a list of contact groups into a readable string.

    Args:
        groups: List of contact group dictionaries

    Returns:
        Formatted string representation of the contact groups list
    """
    if not groups:
        return "No contact groups found."

    parts = []

    # Separate user and system groups
    user_groups = [g for g in groups if g.get("groupType") == "USER_CONTACT_GROUP"]
    system_groups = [g for g in groups if g.get("groupType") == "SYSTEM_CONTACT_GROUP"]

    if user_groups:
        parts.append("👤 USER CONTACT GROUPS:")
        parts.append("")
        for i, group in enumerate(user_groups, 1):
            group_summary = _format_contact_group_summary(group, i)
            parts.append(group_summary)
            parts.append("")

    if system_groups:
        parts.append("🔧 SYSTEM CONTACT GROUPS:")
        parts.append("")
        for i, group in enumerate(system_groups, 1):
            group_summary = _format_contact_group_summary(group, i, is_system=True)
            parts.append(group_summary)
            parts.append("")

    # Summary statistics
    total_members = sum(group.get("memberCount", 0) for group in groups)
    parts.append("=" * 50)
    parts.append(
        f"📊 Summary: {len(groups)} total groups ({len(user_groups)} user, {len(system_groups)} system)"
    )
    parts.append(f"👥 Total contacts across all groups: {total_members}")

    return "\n".join(parts)


def _format_contact_group_summary(
    group: Dict[str, Any], index: int, is_system: bool = False
) -> str:
    """Format a single contact group as a summary for list display."""
    icon = "🔧" if is_system else "📂"
    summary_parts = [f"{icon} Group {index}: {group.get('name', 'Unnamed')}"]

    # Member count
    member_count = group.get("memberCount", 0)
    summary_parts.append(f"  👥 {member_count} member(s)")

    # Resource name
    if group.get("resourceName"):
        summary_parts.append(f"  🔗 {group['resourceName']}")

    return "\n".join(summary_parts)


def format_group_membership_result(result: Dict[str, Any], operation: str = "modify") -> str:
    """Format the result of adding/removing contacts from a group.

    Args:
        result: Result dictionary from group membership operation
        operation: Type of operation (add/remove)

    Returns:
        Formatted string representation of the operation result
    """
    if not result:
        return f"No result from group membership {operation} operation."

    parts = []

    if result.get("success"):
        parts.append(f"✅ Group membership {operation} operation completed successfully!")

        if "added_count" in result:
            parts.append(f"📥 Added {result['added_count']} contact(s) to group")
        elif "removed_count" in result:
            parts.append(f"📤 Removed {result['removed_count']} contact(s) from group")
    else:
        parts.append(f"❌ Group membership {operation} operation failed.")

    # Handle not found contacts
    if result.get("not_found"):
        not_found = result["not_found"]
        parts.append(f"⚠️  {len(not_found)} contact(s) not found:")
        for contact in not_found:
            parts.append(f"   • {contact}")

    # Handle contacts that couldn't be modified
    if result.get("could_not_add"):
        parts.append(f"⚠️  Could not add {len(result['could_not_add'])} contact(s)")
    elif result.get("could_not_remove"):
        could_not_remove = result["could_not_remove"]
        parts.append(f"⚠️  Could not remove {len(could_not_remove)} contact(s) (last group):")
        for contact in could_not_remove:
            parts.append(f"   • {contact}")

    return "\n".join(parts)
