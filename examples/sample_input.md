# Sample system description

Context: multi-service web app with async jobs, third-party APIs, and manual backoffice workflows.

Key points:
- Frontend models assume immediate consistency; actual system is eventually consistent.
- External payment API introduces retries and delayed webhooks.
- Backoffice users can override orders out-of-band.

Requested: compute the Goblin score and per-dimension notes using the lim42 agent profile.
