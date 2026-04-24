def detect_goblin(inconsistency: bool, severity: int = 2):
    if not inconsistency:
        return None

    return {
        "type": "GoblinEvent",
        "severity": max(severity, 2),
        "action": "block" if severity >= 3 else "gate"
    }
