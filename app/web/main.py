from pathlib import Path

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import select

from app.config import PRODUCTS, settings
from app.database import Order, OrderStatus, SessionLocal, Ticket, User, init_db
from app.services.analytics import calculate_profit, top_users_by_stars
from app.services.payments import get_providers

BASE_DIR = Path(__file__).resolve().parent

templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
app = FastAPI(title="Radio Bot Admin")
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")


@app.on_event("startup")
def startup() -> None:
    init_db()


@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request):
    with SessionLocal() as session:
        users = session.query(User).all()
        orders = session.query(Order).order_by(Order.id.desc()).all()
        tickets = session.query(Ticket).order_by(Ticket.id.desc()).all()
        leaders = top_users_by_stars(session)
    return templates.TemplateResponse(
        "admin_dashboard.html",
        {
            "request": request,
            "users": users,
            "orders": orders,
            "tickets": tickets,
            "leaders": leaders,
            "providers": get_providers(),
        },
    )


@app.post("/users/{user_id}/toggle")
def toggle_user(user_id: int):
    with SessionLocal() as session:
        user = session.get(User, user_id)
        if user:
            user.is_blocked = not user.is_blocked
            session.commit()
    return RedirectResponse("/", status_code=303)


@app.post("/orders/{order_id}/status")
def update_order_status(order_id: int, status: str = Form(...)):
    with SessionLocal() as session:
        order = session.get(Order, order_id)
        if order and status in {"pending", "paid", "cancelled"}:
            order.status = OrderStatus(status)
            session.commit()
    return RedirectResponse("/", status_code=303)




@app.post("/providers/{provider}/toggle")
def toggle_provider(provider: str):
    attr = f"{provider}_enabled"
    if hasattr(settings, attr):
        current = getattr(settings, attr)
        setattr(settings, attr, not current)
    return RedirectResponse("/", status_code=303)


@app.get("/webapp", response_class=HTMLResponse)
def webapp_catalog(request: Request):
    with SessionLocal() as session:
        leaders = top_users_by_stars(session)
    return templates.TemplateResponse(
        "webapp.html",
        {"request": request, "products": PRODUCTS, "providers": get_providers(), "leaders": leaders},
    )


@app.get("/profit", response_class=HTMLResponse)
def profit_page(request: Request, revenue: float = 0, commission: float = 0, cost: float = 0):
    profit = calculate_profit(revenue, commission, cost)
    return templates.TemplateResponse(
        "profit.html",
        {
            "request": request,
            "profit": profit,
            "revenue": revenue,
            "commission": commission,
            "cost": cost,
        },
    )


@app.post("/tickets")
def create_ticket(user_tg_id: int = Form(...), subject: str = Form(...), message: str = Form(...)):
    with SessionLocal() as session:
        user = session.scalar(select(User).where(User.tg_id == user_tg_id))
        if user is None:
            user = User(tg_id=user_tg_id)
            session.add(user)
            session.flush()
        ticket = Ticket(user_id=user.id, subject=subject, message=message)
        session.add(ticket)
        session.commit()
    return RedirectResponse("/", status_code=303)
