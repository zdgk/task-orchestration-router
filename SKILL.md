---
name: task-orchestration-router
description: Activation, execution-topology, model-selection, and shared-execution-safety preflight for work that is multi-step, broad, long-running, context-heavy, multi-surface, risk-sensitive, or contains multiple meaningful workstreams. Decide whether orchestration is warranted; if active, organize work into recoverable phases and choose checkpoint-driven single-agent execution, bounded in-task subagents, or one evidence-justified sequential relay. Protect active writers, repository drift, scarce runtime resources, and verification truth at every phase boundary. Do not use for single-answer questions, trivial formatting, simple rewrites, one obvious low-risk local edit, or tiny linear work.
---

# Task Orchestration Router

Select the smallest execution topology that can complete the user's goal reliably. This skill is a control layer only; domain skills continue to own implementation workflows, tools, and quality gates.

Do not ask whether to use subagents when applicable instructions already authorize automatic delegation. Do not expose an inactive or unchanged routine preflight; continue normally unless topology, ownership, risk, or a blocking condition materially changes.

## Respect Boundaries

1. Follow system, developer, user, mode, repository, and domain-skill instructions before this router.
2. Delegation and relay do not broaden scope or authority.
3. Use only agent or thread tools available in the current surface. Fall back to `single-agent` when the safer route is unavailable.
4. Keep approvals, destructive actions, external side effects, unresolved user decisions, shared contracts, integration, and final acceptance with the primary agent.
5. Never create hidden user-owned tasks for ordinary subtasks. Use subagents for bounded current-task work.

## Load Conditional Protocols

Keep this core file sufficient for activation, phase control, and execution safety. Load detailed references only when the selected route needs them:

- Before spawning any subagent, read [references/subagent-protocol.md](references/subagent-protocol.md) and [references/model-routing.md](references/model-routing.md) completely.
- Before creating or preparing a relay successor, read [references/relay-protocol.md](references/relay-protocol.md) and [references/model-routing.md](references/model-routing.md) completely.
- When changing this router, read [references/evaluation-cases.md](references/evaluation-cases.md) completely, then run the bundled validators and forward-tests described under **Maintain The Router**.

The relay protocol conditionally routes Codex Desktop/app thread creation through
[references/codex-desktop-relay.md](references/codex-desktop-relay.md). Do not load that
host adapter on a surface without Codex thread tools.

Do not read relay or model-allocation detail for an inactive request or a same-task single-agent route that needs no model decision.

## Decide Whether The Router Is Active

Evaluate activation once at task start from the user's goal and known scope.

- **`inactive`:** a single-answer question, trivial formatting or translation, simple rewrite, status-only reply, one obvious low-risk local edit, or tiny linear sequence with no meaningful topology choice.
- **`active`:** broad, multi-phase, cross-module, cross-surface, likely long or context-heavy work; at least two plausible workstreams; a meaningful specialization or context-isolation opportunity; or security, safety, data-integrity, destructive, or irreversible risk that makes ownership important.

Do not activate merely because tools or several commands are involved. Do not deactivate merely because one agent can do the work: an active request may still route to `single-agent` when coupling, state, risk, or one coherent reasoning trail makes that safest. Explicit invocation requires this activation check but does not force delegation or relay.

If inactive, stop this control workflow. Do not spawn a child or create another conversation. Continue with applicable domain skills.

## Run The Phase Preflight

For active work, classify only the current phase as exactly one execution route:

- `single-agent`
- `subagents`
- `relay-task` - one sequential successor conversation

Track investigation support separately as exactly one modifier:

- `none`
- `read-only-investigators`

The modifier does not create a fourth route. `single-agent + read-only-investigators`
means the primary remains the sole writer and controlling reasoner while bounded children
collect distinct evidence. Use `subagents` when the phase itself is materially partitioned
into independently owned workstreams. Any spawned investigator still follows the full
subagent protocol.

When two or more investigators run, keep a compact **Investigation Convergence** record for
each unique question, saturation condition, current evidence state, and stop action. Re-check
it after the first material finding and whenever the controlling contract or test matrix
changes. Request an Investigator Capsule immediately or interrupt a child whose question is
answered or superseded; do not wait for a polished narrative.

At task start choose between `single-agent` and `subagents`. Consider `relay-task` only at a stable phase boundary. Re-evaluate after a major investigation, design decision, implementation milestone, migration batch, or verification phase, not after every tool call.

If the route and ownership remain unchanged, record the re-evaluation internally. Send commentary only when the route, write ownership, risk, required approval, or user-visible execution state materially changes.

## Run Complex Work In Recoverable Phases

For every active complex task:

1. **Map the goal and dependency graph.** Record done criteria, constraints, phases, prerequisites, mutable state, shared contracts, and combined verification.
2. **Select only the current phase.** Do not dispatch future work whose investigation, design, approval, or interface is unsettled.
3. **Establish the controlling contract.** Keep architecture, public interfaces, invariants, and write ownership with the primary until stable.
4. **Close delegated boundaries before writing.** For each proposed writing child, inspect direct callers and consumers, barrel exports, wire types and validators, mocks and tests, and current architecture documentation. Approve an exact core write set and any mechanical closure set, or keep shared files with the primary.
5. **Capture the phase baseline.** Record branch/revision, working-tree state, user-owned changes, active writers, resource ownership, and the verification ledger.
6. **Choose the current topology and support modifier.** Delegate only independently actionable work with explicit boundaries and a distinct expected evidence contribution.
7. **Keep the primary productive.** The primary owns substantial investigation, architecture, shared-state, integration, or verification work; it is not only a scheduler.
8. **Integrate against live evidence.** Reconcile child results with current source, current revision, designated ownership, each public Contract Delta, and every material Decision Resolution. After parallel writers reach a stable boundary, make and record the conditional cross-owner seam-review decision before combined verification.
9. **Verify the combined state.** Child-local checks never prove the phase complete.
10. **Refresh the Phase Checkpoint**, then re-evaluate the next phase.

A complex task may change topology by phase, for example:

```text
single-agent investigation
  -> bounded subagents for unlocked slices
  -> single-agent integration and verification
  -> Phase Checkpoint
  -> next-phase preflight
```

## Protect Shared Execution State

### Track Writer Stability

Maintain one write owner per file, module, database, generated artifact, runtime state, or shared interface. Treat each writing child as one of:

- `working`: source may change and is not integration-ready;
- `red`: an intentional test-first or otherwise known-incomplete state;
- `stable`: scoped implementation and child-local checks are complete;
- `handoff`: final result delivered and the child has stopped writing.

While any required writer is `working` or `red`:

- do not run whole-repository verification, stage, commit, or make conclusions from its temporary failures;
- run only read-only or targeted checks that cannot observe or mutate that writer's boundary;
- wait for `stable` or `handoff` before integration.

A child's final handoff freezes its write ownership. Further edits require a new explicit follow-up task and state transition.

### Decide A Conditional Cross-Owner Seam Review

After all required parallel writers reach `stable` or `handoff`, and before combined
verification, the primary records one seam-review decision:

```text
seam_review | required/not-required | reason | affected_contract_deltas | reviewer | status
```

Mark it `required` when parallel writers changed or jointly depend on a public, wire,
persistence, mutation, or state-consumer contract. Otherwise record `not-required` and why
the independently owned boundaries do not create such a seam. A seam review is not mandatory
for every delegated phase.

When required, the primary or one bounded read-only reviewer checks the integrated seam before
combined verification: producer/consumer identity and order; boundary strictness and coercion;
authorization and revalidation at the mutation boundary; refactor/import closure; and rollback
and non-authoritative behavior. Record the evidence and resolve any discrepancy before moving
to combined verification. The review supplements rather than replaces combined tests.

### Guard Repository Drift And Git Ownership

The primary agent stages and commits by default. A child must not stage, commit, switch branches, rewrite history, or clean unrelated files unless its capsule explicitly grants that action.

Before integration, staging, and every commit:

1. Re-read `HEAD`, branch, staged state, and working-tree status.
2. Compare them with the phase baseline.
3. Classify every new change or commit as primary-owned, child-owned, user-owned, generated, or unknown.
4. Preserve unrelated and unknown state; never infer that a concurrent change belongs to the task.
5. If `HEAD` moved unexpectedly, inspect the intervening commits and re-verify affected assumptions before continuing.

Use explicit staging paths. Do not let a successful child check authorize a broad commit.

### Serialize Scarce Or Heavy Resources

Assign one owner at a time to heavy or stateful resources such as full test suites, builds, browsers, local servers, databases, emulators, package managers, or hardware-intensive jobs.

- Children normally run only targeted checks for their owned boundary.
- The primary normally owns combined tests, production builds, browser acceptance, and final cleanup.
- Do not overlap heavy jobs merely because workstreams are code-independent.
- Record started processes and ensure the owning agent stops or hands them off explicitly.

### Prove Runtime Freshness Before Acceptance

Before starting, reusing, or accepting evidence from a stateful preview runtime, acquire a
**Runtime Lease**. Acceptance is blocked until the lease is complete.

1. Inspect the target port or handle first. Record the runtime owner, PID or handle, process
   start time, launch command, port, proxy target, purpose, and cleanup duty.
2. Do not reuse, restart, or stop an existing listener whose ownership or source is unknown.
   Prefer a task-owned runtime on a dedicated free port; otherwise mark runtime acceptance
   `unavailable`.
3. Record the expected source revision or build identity and the authoritative freshness signal,
   such as an OpenAPI route, build/version marker, loaded asset hash, or confirmed hot reload.
4. Prove that the runtime serves that source after startup and after every restart. Treat an
   unproven or stale runtime as `unavailable` evidence; its behavior may be reported only as an
   observation, never as acceptance of current code.
5. Stop only a task-owned runtime. Before handoff, either stop it or transfer the lease with its
   owner, PID, purpose, freshness evidence, and cleanup duty.

### Keep A Verification Ledger

Record every required check with exactly one current status:

- `passed`: command or acceptance check completed successfully;
- `failed`: check ran and found a defect;
- `unavailable`: an external service, permission, credential, network, or environment dependency prevented a result;
- `not-run`: the check was intentionally or accidentally omitted.

Keep an ordered attempt history when a check is retried. Each attempt uses the same four
statuses and records the command or acceptance check plus its decisive evidence and concise
final-report disposition. The current status is the latest authoritative attempt; a later
`passed` attempt may supersede an earlier environmental `unavailable`, but the earlier attempt remains visible. For each non-passed current item, record the exact limitation and the evidence
that was still obtained. `unavailable` is neither a code failure nor a pass. Do not call the
combined state fully green while a required check is currently unavailable or not run.

Use one structured record per attempt with these required fields:

```text
check_id | attempt | status | owner | command_or_acceptance | decisive_evidence | supersedes | report_in_final | report_reason
```

Set `report_in_final` to `yes` or `no` for every attempt and keep `report_reason` concise. Set
it to `yes` for every earlier `failed` or `unavailable` attempt that changed the implementation,
environment, command, or residual risk; that flagged attempt and its reason must remain in the
Phase Checkpoint and survive compaction. Append retries instead of rewriting history. The final
report states each required check's current status and summarizes every material earlier `failed` or `unavailable` attempt flagged for final reporting. It may group routine current passes rather than list every green subcheck, as long as the group identifies the covered checks
and no current non-pass or flagged attempt is hidden.

### Run The Finalization Gate

Immediately before the final response, compare the draft final report against the verification
ledger and confirm:

1. every required check has one current status and the draft reports that status; routine current passes may be grouped when the covered checks are clear;
2. every attempt with `report_in_final: yes`, including every material earlier `failed` or
   `unavailable` attempt that changed implementation, environment, command, or residual risk,
   appears in the draft with its report reason;
3. every current `unavailable` or `not-run` limitation is explicit; and
4. every runtime acceptance marked `passed` has a current Runtime Lease.

A latest `passed` attempt never erases material retry history. Completion is blocked if the
draft omits any required current status or attempt flagged for final reporting. Correct the
ledger and final report before claiming completion if any item above is unsupported.

## Build A Proportionate Phase Checkpoint

Keep checkpoints compact and factual. Use the lightest durable form that can recover the task:

- For a short active phase with committed or easily discoverable state, the current plan plus live repository state is enough.
- For multi-phase or uncommitted work, keep an in-task checkpoint covering goal, completed work, decisions, ownership, revision/status, verification ledger, remaining dependencies, and next action.
- Create a dedicated workspace artifact only when source and normal task state cannot reliably preserve correctness-critical context.

For an in-task checkpoint, prefer this compact order:

1. goal, done criteria, and controlling contract;
2. completed decisions and work not to repeat;
3. branch/revision plus task-owned, child-owned, user-owned, generated, and unknown changes;
4. writer and heavy-resource ownership, including live runtime freshness;
5. verification ledger with current status, exceptional attempt history, and every
   `report_in_final: yes` disposition and reason;
6. remaining dependencies, risks, and blockers;
7. at most three next concrete actions.

Normally keep this checkpoint around 300-600 tokens. If it approaches 900 tokens, replace
child narratives, logs, and copied source with evidence pointers. Do not paste multiple child
reports when one integrated conclusion and their source locations are sufficient.

When an exact multi-owner change set cannot fit compactly, keep a separate **Change Manifest**
in task-local scratch state and reference it from the checkpoint. Record each path or symbol,
owner, writer state, repository classification, public-contract impact, and verification state.
Reconcile the manifest against live source and `git diff --name-status` at every integration or
commit boundary. The manifest is evidence only: it neither expands authority nor makes an
unknown change task-owned. Do not add it to the user's repository unless explicitly requested.

After compaction, rehydrate from the checkpoint: rehydrate every required current status and every attempt flagged
`report_in_final: yes`, then verify them against live state before
delegating or editing. Compaction alone never justifies relay.

## Choose The Current Topology

| Current condition | Route |
| --- | --- |
| Root cause, architecture, shared contract, or write ownership is unresolved. | Primary-led `single-agent`, optionally with the `read-only-investigators` support modifier. |
| Two or more current-phase workstreams are independent and coordination benefit exceeds cost. | `subagents`; primary integrates one result. |
| A stable contract unlocks non-overlapping implementation modules. | Partitioned `subagents`, one write owner per module. |
| Work shares files, runtime state, schema, or an unresolved decision. | Same-task sequential `single-agent` or one explicit owner. |
| Integration, cross-module verification, or final acceptance is due. | Primary-led `single-agent`. |
| Work is long but serial and coherent. | Same-task checkpoints, not relay. |
| A materially different substantial phase passes every relay gate. | One sequential `relay-task`. |

### Route To Single Agent

Use `single-agent` when work is small or linear, later steps depend on unresolved results, workers would share mutable state, frequent approval or user choice is required, heavy resources would contend, or one coherent reasoning trail is more valuable than isolated work. The route remains `single-agent` when bounded read-only investigators only support the primary's coherent investigation and own no implementation partition. Complexity alone is not a reason to delegate.

### Route To Subagents

Use subagents only when at least two workstreams are independently actionable now, each has a bounded output contract, results return to this primary, the benefit exceeds coordination cost, writes are read-only or non-overlapping, and capsule overhead is lower than duplicated work.

Before spawning, read and follow [references/subagent-protocol.md](references/subagent-protocol.md) and [references/model-routing.md](references/model-routing.md). Keep shared contracts and final verification with the primary.

### Route To A Sequential Relay

A relay is exactly one fresh user-visible successor that starts after the current phase is stable, integrated, verified, and recoverable. It is not parallel execution, specialization, extra capacity, or a model-selection shortcut.

Keep relay exceptional. Before preparing or creating one, read and follow [references/relay-protocol.md](references/relay-protocol.md) and [references/model-routing.md](references/model-routing.md). If host rules require explicit confirmation, prepare the capsule and ask rather than substituting a subagent.

## Report The Result

- Pass the Finalization Gate before reporting any completed active phase.
- For inactive or `single-agent` work, report the task outcome, verification ledger including material retry history, and material limits, not the routine preflight.
- For `subagents`, report the integrated outcome, public Contract Deltas, and material combined validation; mention delegation only when it explains coverage or risk.
- For `relay-task`, report the completed phase, preserved state, net context benefit, loss controls, next phase, and created successor. Do not claim the overall goal is complete merely because a relay exists.
- Report browser or runtime acceptance as `passed` only when its Runtime Lease proves current-source freshness; otherwise distinguish observation from acceptance and use `unavailable`.

## Maintain The Router

When changing topology, writer-safety, repository-drift, resource, verification, model, capsule, or relay rules:

1. Read [references/evaluation-cases.md](references/evaluation-cases.md) completely.
2. Update behavior cases for every material rule change.
3. Run `scripts/validate_contract.py`.
4. Run the skill-creator `scripts/quick_validate.py` structural validator.
5. Forward-test material behavior changes with fresh isolated agents using ordinary task prompts. Keep expected outcomes in the evaluator, never in child prompts.
