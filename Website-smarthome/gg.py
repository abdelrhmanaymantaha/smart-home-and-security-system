from werkzeug.security import check_password_hash

stored_hashed_password = "scrypt:32768:8:1$Zs9uCe3hGVATA51W$dd9666455817f1832c88bfd03f82530bd72eea4611991a4b1c067e3a0de343fc2dcd652277812fff3043fe6091a21fddc9656a6f85ceb2f2d8cf05d4aabc6386"

password_input = "123456"  

if check_password_hash(stored_hashed_password, password_input):
    print("true")
else:
    print("false")