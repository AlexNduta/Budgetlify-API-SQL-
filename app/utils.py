from passlib.context import CryptContext # import passlib for hashing

# specify that we will be using bcrypt for hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password: str):
    """ will act as our hashing function
        - imports the passlib 
        - Takes a password as input the hash it using bcrypt
    """
    return pwd_context.hash(password)

