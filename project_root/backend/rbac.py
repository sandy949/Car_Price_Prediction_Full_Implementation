# backend/rbac.py

def is_authorized(role, action):
    """
    Check if a given role is authorized to perform a specific action.

    Args:
        role (str): The role of the user (e.g., 'admin', 'manager', 'user').
        action (str): The action to check permission for (e.g., 'create', 'update', 'delete', 'view').

    Returns:
        bool: True if the role is authorized for the action, False otherwise.
    
    Permissions:
        - admin: ['create', 'update', 'delete', 'view']
        - manager: ['create', 'update', 'view']
        - user: ['view']
    """
    permissions = {
        'admin': ['create', 'update', 'delete', 'view'],
        'manager': ['create', 'update', 'view'],
        'user': ['view']
    }
    return action in permissions.get(role, [])
