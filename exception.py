class MessageNotFoundException(Exception):
    detail = 'Message not found'

class TokenNotCorrect(Exception):
    detail = 'Token is not correct'


class UserNotFound(Exception):
    detail = 'User not found'


class UserDataNotAvailable(Exception):
    detail = 'User data is not available'


class MessageNotSent(Exception):
    detail = 'Message not sent'
