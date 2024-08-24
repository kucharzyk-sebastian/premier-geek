class BaseError(Exception):
    """Base app error"""


class UnrelatedQueryError(BaseError):
    """The query asked was unrelated to Premier League squads"""
