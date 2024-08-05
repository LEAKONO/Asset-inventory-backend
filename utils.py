# utils.py
def determine_role_from_email(email):
    email = email.lower()  
    
    
    role_mappings = {
        "employee": "@gmail.com",
        "procurement_manager": "@manager.com",
        "admin": "@admin.com"
    }
    
    for role, domain in role_mappings.items():
        if domain in email:
            return role
    
    return "check your email and try again"
