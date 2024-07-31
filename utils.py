# utils.py

def determine_role_from_email(email):
    if "@gmail.com" in email:
        return "employee"
    elif "@manager.gmail.com" in email:
        return "procurement_manager"
    elif "@admin.gmail.com" in email:
        return "admin"
    else:
        return "check your email and try again"  
