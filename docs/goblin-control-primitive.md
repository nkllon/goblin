# Goblin as Control Primitive

This document operationalizes **Goblin** as a control primitive for agents and systems.

## Definition

Goblin = system state is not trustworthy for decision-making.

## Required Behavior

When Goblin is detected:

- Do not trust current state
- Gate irreversible actions
- Capture cross-plane state
- Surface explicitly

## Trigger Conditions

- Cross-plane inconsistency
- Presented vs actual divergence
- Orphaned authority
- Unresolvable truth source

## Agent Rule

```
IF inconsistency_detected:
  emit GoblinEvent
  set severity >= 2
  block irreversible actions
```

## Notes

Goblin is the front-door signal. Root cause (model gap, drift, SCIG) is secondary.
