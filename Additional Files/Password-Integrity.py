from werkzeug.security import generate_password_hash, check_password_hash
pwhash = generate_password_hash('P@ssw0rd')
print(pwhash)
check_password_hash(pwhash , 'P@ssw0rd')
