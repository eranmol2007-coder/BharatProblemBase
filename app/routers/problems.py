from fastapi import APIRouter, Depends, HTTPException, Query, BackgroundTasks
from sqlalchemy.orm import Session
from sqlalchemy import or_, case
from typing import Optional

from app.database import get_db
from app.models.problem_statement import ProblemStatement
from app.schemas.problem_statement import (
    ProblemStatementCreate,
    ProblemStatementUpdate,
    ProblemStatementResponse,
    PaginatedResponse,
)
from app.scrapers.orchestrator import ScraperOrchestrator

router = APIRouter(prefix="/api/problems", tags=["problems"])


@router.get("/suggest", response_model=list[dict])
def suggest_problems(
    q: str = Query("", min_length=0),
    db: Session = Depends(get_db),
):
    if not q:
        return []
    search_term = f"%{q}%"
    results = (
        db.query(ProblemStatement.id, ProblemStatement.title, ProblemStatement.domain)
        .filter(ProblemStatement.title.ilike(search_term))
        .limit(6)
        .all()
    )
    return [{"id": r.id, "title": r.title, "domain": r.domain or ""} for r in results]


@router.get("/all-titles", response_model=list[dict])
def get_all_titles(db: Session = Depends(get_db)):
    results = (
        db.query(ProblemStatement.id, ProblemStatement.title, ProblemStatement.domain)
        .all()
    )
    return [{"id": r.id, "title": r.title, "domain": r.domain or ""} for r in results]


@router.get("", response_model=PaginatedResponse)
def list_problems(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=10000),
    search: Optional[str] = None,
    domain: Optional[str] = None,
    platform: Optional[str] = None,
    difficulty: Optional[str] = None,
    organization: Optional[str] = None,
    category: Optional[str] = None,
    is_open: Optional[bool] = None,
    source_year: Optional[int] = None,
    sort_by: Optional[str] = Query("created_at", pattern="^(created_at|title|source_year)$"),
    sort_order: Optional[str] = Query("desc", pattern="^(asc|desc)$"),
    db: Session = Depends(get_db),
):
    query = db.query(ProblemStatement)

    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                ProblemStatement.title.ilike(search_term),
                ProblemStatement.description.ilike(search_term),
                ProblemStatement.organization.ilike(search_term),
                ProblemStatement.domain.ilike(search_term),
            )
        )

    if domain:
        query = query.filter(ProblemStatement.domain.ilike(f"%{domain}%"))
    if platform:
        query = query.filter(ProblemStatement.source_platform.ilike(f"%{platform}%"))
    if difficulty:
        query = query.filter(ProblemStatement.difficulty.ilike(f"%{difficulty}%"))
    if organization:
        query = query.filter(ProblemStatement.organization.ilike(f"%{organization}%"))
    if category:
        query = query.filter(ProblemStatement.category.ilike(f"%{category}%"))
    if is_open is not None:
        query = query.filter(ProblemStatement.is_open == is_open)
    if source_year:
        query = query.filter(ProblemStatement.source_year == source_year)

    total = query.count()

    if search:
        title_match = case(
            (ProblemStatement.title.ilike(f"%{search}%"), 0),
            else_=1,
        )
        desc_match = case(
            (ProblemStatement.description.ilike(f"%{search}%"), 0),
            else_=1,
        )
        query = query.order_by(title_match, desc_match, ProblemStatement.created_at.desc())
    else:
        sort_col = getattr(ProblemStatement, sort_by, ProblemStatement.created_at)
        if sort_order == "desc":
            query = query.order_by(sort_col.desc())
        else:
            query = query.order_by(sort_col.asc())

    items = query.offset((page - 1) * page_size).limit(page_size).all()

    return PaginatedResponse(
        items=[ProblemStatementResponse.model_validate(p) for p in items],
        total=total,
        page=page,
        page_size=page_size,
        total_pages=max(1, (total + page_size - 1) // page_size),
    )


@router.get("/platforms", response_model=list[dict])
def list_platforms(db: Session = Depends(get_db)):
    from sqlalchemy import func
    results = (
        db.query(
            ProblemStatement.source_platform,
            func.count(ProblemStatement.id).label("count"),
            func.count(ProblemStatement.id).filter(ProblemStatement.is_open == True).label("open_count"),
        )
        .group_by(ProblemStatement.source_platform)
        .all()
    )
    return [
        {
            "name": r.source_platform or "General",
            "total": r.count,
            "open": r.open_count,
        }
        for r in results
    ]


@router.get("/domains", response_model=list[dict])
def list_domains(db: Session = Depends(get_db)):
    from sqlalchemy import func
    results = (
        db.query(
            ProblemStatement.domain,
            func.count(ProblemStatement.id).label("count"),
        )
        .group_by(ProblemStatement.domain)
        .all()
    )
    return [{"name": r.domain or "General", "count": r.count} for r in results]


@router.get("/stats", response_model=dict)
def get_stats(db: Session = Depends(get_db)):
    total = db.query(ProblemStatement).count()
    open_count = db.query(ProblemStatement).filter(ProblemStatement.is_open == True).count()
    platform_count = (
        db.query(ProblemStatement.source_platform)
        .distinct()
        .count()
    )
    domain_count = (
        db.query(ProblemStatement.domain)
        .distinct()
        .count()
    )
    return {
        "total_problems": total,
        "open_problems": open_count,
        "platforms": platform_count,
        "domains": domain_count,
    }


@router.get("/{problem_id}", response_model=ProblemStatementResponse)
def get_problem(problem_id: int, db: Session = Depends(get_db)):
    problem = db.query(ProblemStatement).filter(ProblemStatement.id == problem_id).first()
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")
    return problem


@router.post("", response_model=ProblemStatementResponse, status_code=201)
def create_problem(problem: ProblemStatementCreate, db: Session = Depends(get_db)):
    existing = db.query(ProblemStatement).filter(
        ProblemStatement.title == problem.title
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Problem with this title already exists")

    db_problem = ProblemStatement(**problem.model_dump())
    db.add(db_problem)
    db.commit()
    db.refresh(db_problem)
    return db_problem


@router.put("/{problem_id}", response_model=ProblemStatementResponse)
def update_problem(problem_id: int, problem: ProblemStatementUpdate, db: Session = Depends(get_db)):
    db_problem = db.query(ProblemStatement).filter(ProblemStatement.id == problem_id).first()
    if not db_problem:
        raise HTTPException(status_code=404, detail="Problem not found")

    update_data = problem.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_problem, key, value)

    db.commit()
    db.refresh(db_problem)
    return db_problem


@router.delete("/{problem_id}", status_code=204)
def delete_problem(problem_id: int, db: Session = Depends(get_db)):
    db_problem = db.query(ProblemStatement).filter(ProblemStatement.id == problem_id).first()
    if not db_problem:
        raise HTTPException(status_code=404, detail="Problem not found")
    db.delete(db_problem)
    db.commit()


@router.post("/scrape", response_model=dict)
def trigger_scrape(background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    def _run_scrape():
        orchestrator = ScraperOrchestrator()
        orchestrator.scrape_all(db=db)

    background_tasks.add_task(_run_scrape)
    return {"status": "scrape_started", "message": "Scraping is running in the background"}
