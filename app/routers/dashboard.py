from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from jinja2 import Environment, FileSystemLoader
from app.config import DOMAIN

router = APIRouter(include_in_schema=False)
env = Environment(loader=FileSystemLoader("app/templates"))


def render(template: str, **kwargs) -> str:
    return env.get_template(template).render(**kwargs, domain=DOMAIN)


@router.get("/", response_class=HTMLResponse)
def landing():
    return render("landing.html")


@router.get("/pricing", response_class=HTMLResponse)
def pricing():
    return render("pricing.html")


@router.get("/docs-page", response_class=HTMLResponse)
def docs_page():
    return render("docs.html")
