from passlib.context import CryptContext
change_password=CryptContext(schemes= ["argon2", "bcrypt"],
        deprecated="auto"
    )
def hash_password(plan_password:str):
    return change_password.hash(plan_password)
def verfiy_password(orgin_password:str,plan_password:str):
    return change_password.verify(orgin_password,plan_password)
