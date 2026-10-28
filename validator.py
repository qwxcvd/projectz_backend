from re import *


def validate_email(email: str):
    rg = r"^[\w\.-]+@kpfu.ru"
    if fullmatch(rg, email):
        return True
    return False
