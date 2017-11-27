

def tryint(value):
    """
    Try to convert value to int
    :param value: value that we want to try to convert to int
    :return: False if fails, int value if ok.
    """
    try:
        return int(value)
    except:
        return False


def is_user_valid(username, password):
    """
    Mock to validate user and password for authentication
    :param username: user used to authenticate
    :param password: password used to authenticate
    :return:
    """
    if username == "admin" and password == "admin":
        return True
    else:
        return False
