from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="src/static/html")

templates.env.globals["static"] = lambda path: f"/static{path}"
