from __future__ import annotations

from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Any, Mapping, Sequence


@dataclass(frozen=True)
class GoblinEvent:
    """Executable control signal for untrustworthy system state.

    Goblin is the front-door signal. It does not require root cause certainty.
    It only requires enough inconsistency to degrade trust and constrain action.
    """

    condition: str
    severity: int
    planes: Sequence[str] = field(default_factory=tuple)
    evidence: Mapping[str, Any] = field(default_factory=dict)
    detected_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    event_type: str = "GoblinEvent"

    @property
    def action(self) -> str:
        if self.severity >= 3:
            return "block"
        if self.severity >= 2:
            return "gate"
        if self.severity >= 1:
            return "warn"
        return "none"

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["type"] = payload.pop("event_type")
        payload["action"] = self.action
        return payload


def detect_goblin(
    inconsistency: bool,
    *,
    condition: str = "unspecified_inconsistency",
    severity: int = 2,
    planes: Sequence[str] | None = None,
    evidence: Mapping[str, Any] | None = None,
) -> dict[str, Any] | None:
    """Return a GoblinEvent payload when trust must be degraded.

    Severity semantics:
    - 0: clean
    - 1: warn
    - 2: gate decision / require verification
    - 3+: block irreversible action
    """

    if not inconsistency:
        return None

    normalized_severity = max(int(severity), 2)
    event = GoblinEvent(
        condition=condition,
        severity=normalized_severity,
        planes=tuple(planes or ()),
        evidence=dict(evidence or {}),
    )
    return event.to_dict()


def should_block(event: Mapping[str, Any] | None) -> bool:
    """True when an emitted GoblinEvent should block execution."""

    if not event:
        return False
    return int(event.get("severity", 0)) >= 3
