from app.models.user import Role

class Permissions:
    CREATE_USER = "create_user"
    DELETE_USER = "delete_user"
    UPDATE_USER = "update_user"
    VIEW_USER = "view_user"
    CREATE_CONTENT = "create_content"
    DELETE_CONTENT = "delete_content"
    UPDATE_CONTENT = "update_content"
    VIEW_CONTENT = "view_content"


from .permissions import Permissions

# Define roles and their associated permissions using constants
ROLES_PERMISSIONS = {
   Role.ADMIN : [
        Permissions.CREATE_USER, 
        Permissions.DELETE_USER, 
        Permissions.UPDATE_USER, 
        Permissions.VIEW_USER, 
        Permissions.CREATE_CONTENT, 
        Permissions.DELETE_CONTENT, 
        Permissions.UPDATE_CONTENT, 
        Permissions.VIEW_CONTENT
    ],
    Role.MODERATOR: [
        Permissions.UPDATE_USER, 
        Permissions.VIEW_USER, 
        Permissions.UPDATE_CONTENT, 
        Permissions.DELETE_CONTENT, 
        Permissions.VIEW_CONTENT
    ],
    Role.USER: [
        Permissions.CREATE_CONTENT, 
        Permissions.UPDATE_CONTENT, 
        Permissions.VIEW_CONTENT
    ]
}
