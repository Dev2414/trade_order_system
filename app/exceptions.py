from fastapi import HTTPException

def stock_not_found():
    raise HTTPException(
        status_code=404,
        detail="Stock not found"
    )

def not_enough_shares():
    raise HTTPException(
        status_code=400,
        detail="Not enough shares to sell"
    )

def email_exists():
    raise HTTPException(
        status_code=400,
        detail="Email already exists"
    )

def unauthorized():
    raise HTTPException(
        status_code=401,
        detail="Invalid or expired token"
    )

def admin_only():
    raise HTTPException(
        status_code=403,
        detail="Admin access only"
    )
