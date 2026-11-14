def route(alert):
    backlog = alert["backlog"]
    if not isinstance(backlog, int) or isinstance(backlog, bool) or backlog < 0:
        raise ValueError("Backlog must be a nonnegative integer.")
    if not isinstance(alert["offline"], bool):
        raise ValueError("Offline must be true or false.")
    if alert["offline"]:
        return {"route": "connection", "reason": "offline rule takes priority"}
    if backlog >= 3:
        return {"route": "queue", "reason": "backlog is at least three"}
    return {"route": "monitor", "reason": "online with backlog below three"}


def solve_extension():
    return [route(alert) for alert in (
        {"offline": True, "backlog": 9},
        {"offline": False, "backlog": 9},
        {"offline": False, "backlog": 0},
    )]

if __name__ == "__main__":
    import json
    print(json.dumps(solve_extension(), sort_keys=True))
