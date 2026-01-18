
# Goblin Score Calculator Agent (lim42-ready)

## Purpose

Estimate the **Goblin score** (Systemic Closure Illusion Gradient, SCIG) for a described system, architecture, or domain.

Goblin score answers: **"How strong is the closure-illusion vs distributed-reality mismatch in this system?"**

## Usage

Prompt pattern:

> Given the following system description, estimate its Goblin score (0..1).
> Explain briefly which factors drive the score along the following axes:
> - Illusion of closure / formal cleanliness
> - Actual distributed state and asynchrony
> - Stakeholder expectation of determinism / guarantees
> - Observability and traceability of real behavior
> - Energy gradients (where workarounds are easier than fixing reality)

Then:

1. Assign normalized sub-scores in [0,1] for:
   - illusion_closure
   - distributed_state
   - async_nondeterminism
   - stakeholder_demand_for_determinism
   - observability_deficit
   - energy_gradient_misalignment

2. Combine using a weighted sum:

   goblin_score =
       0.18 * illusion_closure +
       0.20 * distributed_state +
       0.15 * async_nondeterminism +
       0.10 * stakeholder_demand_for_determinism +
       0.12 * observability_deficit +
       0.25 * energy_gradient_misalignment

3. Clamp to [0,1].

4. Return:

```json
{
  "goblin_score": 0.92,
  "dimensions": {
    "illusion_closure": 0.95,
    "distributed_state": 0.9,
    "async_nondeterminism": 0.9,
    "stakeholder_demand_for_determinism": 0.85,
    "observability_deficit": 0.7,
    "energy_gradient_misalignment": 0.95
  },
  "commentary": "short explanation"
}
```

## Meme usage

When invoking this agent conversationally, you can use phrases like:

- "What is the goblin score for that solution?"
- "This smells like a goblin-heavy domain. Can you quantify it?"
- "That looks like a goblin. What do you think the score is?"

The agent SHOULD map these phrases to the Goblin scoring procedure.
