# Model Routing

Read this file before assigning an explicit model or reasoning effort to a subagent or relay successor. Treat role capabilities as stable and exact model names as a replaceable catalog layer; first verify which models and effort levels the current host exposes.

## Fixed Two-Profile Mapping

Use exactly one profile for every router-selected subagent or relay successor:

| Profile | Responsibility | Model | Effort |
| --- | --- | --- | --- |
| **Terra bounded-work agent** (`Terra 有界工作智能体`) | A stable contract, explicit non-overlapping boundary, concrete deliverable, and bounded validation | `gpt-5.6-terra` | `max` |
| **Sol judgment/integration agent** (`Sol 判断/集成智能体`) | Architecture, unresolved root cause or scope, shared contracts, cross-module judgment, safety or data integrity, integration, and final acceptance | `gpt-5.6-sol` | `xhigh` |

These are fixed router defaults. Every router-selected Terra assignment uses `max`; every
router-selected Sol assignment uses `xhigh`. Do not lower, promote, or swap either setting
based on perceived simplicity or difficulty.

## Assignment Rules

1. Classify the assigned responsibility, not the subject, whether code will be written, or whether
   the agent is primary or child.
2. Use the Terra bounded-work profile only after the controlling contract, exact boundary,
   expected output, and validation are stable. It covers bounded implementation, tests, UI
   details, routine read-only checks, documentation, data organization, and repetitive work.
3. Use the Sol judgment/integration profile for architecture, decomposition, unresolved or
   cross-module diagnosis, Scope Amendment decisions, ambiguous public contracts, safety or
   data-integrity judgment, integration, and final acceptance.
4. Split mixed work sequentially when safe: Sol establishes or repairs the contract; Terra
   executes the resulting bounded work. Do not label an unstable or high-risk action Terra
   merely because it is called implementation.
5. A Terra agent stops at the current safe boundary and escalates when it finds an unresolved
   root cause, an unapproved shared-interface change, conflicting ownership, material scope
   expansion, a safety or data-integrity decision, or a final cross-module tradeoff. It reports
   evidence and a proposed Scope Amendment; it does not decide the Sol-owned question.
6. A Sol agent used as a child returns its judgment to the primary. It does not acquire Git,
   approval, integration, or final-acceptance authority that the primary retained.
7. Set model and effort explicitly when the selected host and tool permit those fields. When
   overrides require fresh context, use `fork_turns: none` or the smallest sufficient history
   and provide a self-contained capsule. When host policy owns runtime selection, follow
   **Host-Owned Runtime Selection** below.
8. Preserve domain-skill isolation requirements for blind validation.
9. Do not create a user-visible task solely to change the current primary's model.

## Availability And Overrides

A later explicit user model or effort choice overrides this router mapping. Domain skills may
impose a stronger capability requirement, but may not silently weaken an explicit user choice.

If an exact profile is unavailable on a tool that permits explicit selection, do not silently substitute another model or effort. Keep the phase single-agent or leave the delegated check
`unavailable`, and disclose the material routing limitation. Do not claim that a different runtime satisfied either fixed profile.

## Host-Owned Runtime Selection

Higher-priority host rules may require omitting model or effort fields unless the user explicitly
selected them. In that case:

1. classify the responsibility and record the router's recommended Terra or Sol profile;
2. omit prohibited runtime fields instead of manufacturing user authorization;
3. label the actual runtime as `host-default` or `host-selected`, not as the recommended fixed
   profile unless the host proves an exact match; and
4. do not treat host-owned omission as silent substitution.

If an exact profile is itself necessary to make a delegated safety or data-integrity decision
acceptable, keep that decision with the current primary or mark delegation `unavailable`.
