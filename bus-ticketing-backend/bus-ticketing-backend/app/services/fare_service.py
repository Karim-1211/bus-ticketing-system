"""Fare calculation helpers."""
from app.models.route import Route

def calculate_fare(route: Route, discount: float = 0.0) -> float:
    return round(max(route.base_fare * (1 - discount), 0), 2)
