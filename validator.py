from re import *


def validate_email(email: str):
    rg = r"^[\w\.-]+@gmail.com"
    if fullmatch(rg, email):
        return True
    return False
