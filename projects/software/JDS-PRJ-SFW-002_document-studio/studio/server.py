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

from . import config, creator, doctor, editor, engine, placement, registry, templates

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


class SaveRequest(BaseModel):
    path: str
    content: str


class ReviseRequest(BaseModel):
    path: str
    author: str
    description: str
    new_status: str | None = None


class ClassifyRequest(BaseModel):
    ps: float
    volume: float
    medium: str = "compressed air"


class SupervisionRequest(BaseModel):
    step: str                       # inventory | program | round | review
    source: str
    output: str
    client: str | None = None
    site: str | None = None
    author: str | None = None
    round_type: str | None = None


# --- metadata routes --------------------------------------------------------

@app.get("/api/health")
def health():
    """Dependency preflight — lets the UI warn before a feature fails."""
    report = doctor.check()
    return {"dependencies": report, "ready": not doctor.missing(report)}


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
    """Preview the next number AND a suggested target folder for this category."""
    try:
        return {
            "doc_no": creator.preview_number(category, domain, template_type),
            "target_dir": placement.suggest_target_dir(category, domain, template_type),
        }
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


@app.get("/api/document")
def get_document(path: str):
    try:
        return editor.read_document(path)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"Not found: {path}")
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@app.post("/api/document/save")
def save_document(body: SaveRequest):
    try:
        return editor.save_document(body.path, body.content)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"Not found: {body.path}")
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@app.post("/api/revise")
def revise_document(body: ReviseRequest):
    try:
        return editor.revise_document(body.path, body.author, body.description,
                                      body.new_status or None)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"Not found: {body.path}")
    except ValueError as exc:
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


@app.post("/api/classify")
def classify(body: ClassifyRequest):
    """Quick AFS 2017:3 vessel classification — result text returned."""
    return engine.classify_quick(body.ps, body.volume, body.medium)


@app.post("/api/supervision")
def supervision(body: SupervisionRequest):
    """Run one AFS 2017:3 supervision-pipeline step (writes a markdown file)."""
    try:
        result = engine.supervision(
            body.step, body.source, body.output, client=body.client,
            site=body.site, author=body.author, round_type=body.round_type)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    if not result["ok"]:
        return JSONResponse(status_code=400, content=result)
    return result


@app.post("/api/office")
def make_office(kind: str):
    """Generate an Excel workbook (timesheet | expense | mileage | all)."""
    if kind not in ("timesheet", "expense", "mileage", "all"):
        raise HTTPException(status_code=400, detail=f"Unknown office doc '{kind}'")
    result = engine.generate_office(kind)
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
    print(doctor.format_report())
    print(f"\nJDS Document Studio → http://{config.HOST}:{config.PORT}")
    uvicorn.run(app, host=config.HOST, port=config.PORT)


if __name__ == "__main__":
    main()
