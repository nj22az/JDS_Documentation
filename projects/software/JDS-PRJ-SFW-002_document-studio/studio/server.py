"""FastAPI server — the thin HTTP layer over the Studio core.

Every route delegates to the core (creator/registry/templates) or the engine
(validator/PDF). No JDS logic lives here; this file only translates HTTP to
function calls and back, so it stays small and the testable logic stays in the
core modules.

Run:  python3 -m studio.server      (or use ../run.command)
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from . import config, creator, engine, registry, templates

app = FastAPI(title="JDS Document Studio", version="A")


# --- request models ---------------------------------------------------------

class NewDocument(BaseModel):
    template_rel_path: str
    target_dir: str
    title: str
    category: str
    author: str
    domain: str | None = None
    template_type: str | None = None
    status: str = "DRAFT"
    rev: str = "A"


class PdfRequest(BaseModel):
    path: str


# --- metadata routes --------------------------------------------------------

@app.get("/api/taxonomy")
def taxonomy():
    """Dropdown data for the UI: categories, domains, statuses."""
    return {
        "categories": list(config.CATEGORY_SECTIONS.keys()),
        "domains": list(config.DOMAIN_CODES),
        "statuses": list(config.VALID_STATUSES),
    }


@app.get("/api/templates")
def get_templates():
    return templates.list_templates()


@app.get("/api/next-number")
def next_number(category: str, domain: str | None = None,
                template_type: str | None = None):
    try:
        return {"doc_no": creator.preview_number(category, domain, template_type)}
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=400, detail=str(exc))


@app.get("/api/registry")
def get_registry():
    return registry.parse_entries(registry.read_text())


# --- action routes ----------------------------------------------------------

@app.post("/api/documents")
def create_document(body: NewDocument):
    try:
        return creator.create_document(
            template_rel_path=body.template_rel_path,
            target_dir=body.target_dir,
            title=body.title,
            category=body.category,
            author=body.author,
            domain=body.domain or None,
            template_type=body.template_type or None,
            status=body.status,
            rev=body.rev,
        )
    except (ValueError, KeyError, FileExistsError) as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@app.post("/api/validate")
def validate(quick: bool = False):
    return engine.run_validator(quick=quick)


@app.post("/api/pdf")
def make_pdf(body: PdfRequest):
    result = engine.generate_pdf(body.path)
    if not result["ok"]:
        return JSONResponse(status_code=400, content=result)
    return result


# --- static front-end -------------------------------------------------------

@app.get("/")
def index():
    return FileResponse(config.WEB_DIR / "index.html")


app.mount("/", StaticFiles(directory=str(config.WEB_DIR)), name="web")


def main():
    import uvicorn
    print(f"JDS Document Studio → http://{config.HOST}:{config.PORT}")
    uvicorn.run(app, host=config.HOST, port=config.PORT)


if __name__ == "__main__":
    main()
