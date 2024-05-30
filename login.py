from src.auth import register_user, login_user
from database import check_database

# If no errors are thrown, the user registration, login, and database download should be successful.

def main():
    print("Starting user registration...")
    register_user()  
    
    print("Attempting user login...")
    login_user() 
    
    print("Downloading and decrypting database...")
    check_database()

if __name__ == "__main__":
    main()
    
