def allowed_requests(plan="free", used=0):
    limits = {"free": 5}
    return used < limits.get(plan, 0)
