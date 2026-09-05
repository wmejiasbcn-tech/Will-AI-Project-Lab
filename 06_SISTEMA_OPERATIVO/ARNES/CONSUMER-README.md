# Feedforward runtime consumer

The runtime consumer is intentionally minimal: it reads the materialized `harness-feedforward.json`, validates its required fields and SHA-256, and produces `harness-runtime-context.json` for preparation of an execution context.

It does not execute the Guide, grant authority, or replace SCI transport or epistemic verification.
