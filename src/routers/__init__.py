import typing

from fastapi import APIRouter

from routers import home


class Router(typing.TypedDict):
    router: APIRouter
    prefix: str


url_path_list: list[Router] = [Router(router=home.router, prefix="")]
