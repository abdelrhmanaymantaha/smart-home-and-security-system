from werkzeug.security import generate_password_hash

password = "12"  
hashed_password = generate_password_hash(password)

print(hashed_password)