from datetime import datetime, date

def to_date(date_str: str) -> date:
    return datetime.strptime(date_str, "%Y-%m-%d").date()

def today() -> date:
    return datetime.now().date()