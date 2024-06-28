from .comments import comments_router
from .discussions import discussion_router
from .questions import questions_router
from .votes import votes_router


list_of_routes = [
    comments_router,
    questions_router,
    discussion_router,
    votes_router,
]


__all__ = [
    "list_of_routes",
]