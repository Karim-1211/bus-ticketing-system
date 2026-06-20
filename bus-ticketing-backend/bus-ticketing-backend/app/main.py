from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.base import Base
from app.db.session import engine
from app.models import user, bus, route, schedule, seat, booking, ticket, payment, employee, notification
from app.api.routes import auth, buses, bus_routes, schedules, bookings, reports, notifications, employees

app = FastAPI(title="Bus Ticketing Management System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://silly-torte-0369fc.netlify.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(buses.router)
app.include_router(bus_routes.router)
app.include_router(schedules.router)
app.include_router(bookings.router)
app.include_router(reports.router)
app.include_router(notifications.router)
app.include_router(employees.router)

@app.get("/")
def root():
    return {"message": "Bus Ticketing API is running!"}