from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
password = "passowrd123"
hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
check = bcrypt.check_password_hash(hashed_password, password)  # Should return True

print(hashed_password)