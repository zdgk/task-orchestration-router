# Subagent Protocol

Read this file completely before spawning subagents for `task-orchestration-router`.

## Contents

- [Admission gates](#admission-gates)
- [Ownership and isolation](#ownership-and-isolation)
- [Boundary closure and scope amendments](#boundary-closure-and-scope-amendments)
- [Writer lifecycle](#writer-lifecycle)
- [Investigator capsule and convergence](#investigator-capsule-and-convergence)
- [Module Capsule](#module-capsule)
- [Dispatch and integration](#dispatch-and-integration)

## Admission Gates

Use subagents only when every gate passes:

1. All workstreams serve one final outcome owned by the primary task.
2. At least two current-phase workstreams are independently actionable now.
3. Each workstream has one concrete module boundary, dependency slice, review dimension, or evaluation case and an output contract.
4. Results can be summarized and integrated by the primary.
5. Expected speed, coverage, specialization, or context-isolation benefit exceeds coordination cost.
6. Writes are read-only, primary-owned, or partitioned into explicit non-overlapping sets.
7. Capsule and summary overhead is lower than the duplicated work delegation avoids.
8. Concurrency and heavy-resource budgets permit safe parallel work.
9. Each child has a distinct expected evidence contribution that is not already covered by
   the primary or another child, unless deliberate adversarial redundancy is named.
10. The primary can state an evidence-saturation stop condition before dispatch.
11. A writing workstream can complete a dependency-closure scan before its first edit and can
    name one exact core write set plus any pre-authorized mechanical closure set.

Do not spawn future-phase workers whose prerequisite decision or shared contract is unresolved. Do not spawn merely to repeat the same question, mirror the whole task, or outsource final judgment. Split nearby investigations by entrypoint, lifecycle, consumer, or failure dimension so their evidence deltas are explicit.

Evaluate every candidate independently. Multiple children may be dispatched together when all gates and resource constraints are already satisfied; do not serialize safe independent investigation merely because one child was considered first.

## Ownership And Isolation

Bind each child to one substantial behavioral boundary, not merely a directory. The primary owns the global goal, architecture, module graph, shared contracts, cross-module decisions, integration, Git staging/commits, and final verification.

- Give one write owner to each file, database, generated artifact, runtime state, and shared interface.
- Keep shared files and public contracts with the primary unless one explicit owner is assigned after consumers agree.
- Let a child read declared adjacent interfaces, but forbid write-scope expansion.
- Require cross-boundary findings to be reported rather than silently implemented.
- Use `fork_turns: none` by default. Use a small history only when a recent user decision cannot be restated accurately.
- Never pass the full transcript merely for convenience.
- For cross-module bugs, assign one named entrypoint-to-state, request-flow, lifecycle, or call-graph slice—not an unbounded repository mandate.

When a domain skill requires blind validation, write an ordinary user-like task. Do not reveal the expected answer, suspected defect, intended fix, evaluation label, or evaluator-only artifacts.

## Boundary Closure And Scope Amendments

Before the first edit in a writing workstream, verify a dependency-closure scan of the owned
behavior's direct callers and consumers, barrel exports, public types and validators, mocks and
tests, and current architecture documentation. The primary may record a completed scan and
approved sets in the initial capsule. If that scan is current and the child finds no delta, it
proceeds without a separate status message. Otherwise it reports one batched proposed closure
set, and the primary resolves overlapping owners and approves exact additions before they are
written.

Give the child two explicit path sets when useful:

- **core write set:** production paths and symbols exclusively owned by the child;
- **mechanical closure set:** exact barrels, contract tests, mocks, and current docs that the
  child may update only to keep the owned contract consistent.

When new cross-boundary findings appear after writing starts:

1. Classify each as `blocking closure`, `required contract closure`, or `adjacent follow-up`.
2. Batch all non-urgent findings found in the same scan into one Scope Amendment containing
   paths or symbols, reason, contract impact, conflicting owners, and proposed action.
3. Send an immediate message only for a blocker that prevents safe progress. Otherwise continue
   within the approved boundary or wait at the next safe checkpoint.
4. Do not edit an unapproved path. An adjacent follow-up remains evidence for the primary and
   does not silently enlarge the child task.

## Writer Lifecycle

Require writing children to communicate one current state:

- `working`: source is changing;
- `red`: an intentional test-first or known-incomplete state;
- `stable`: scoped work and local checks are complete;
- `handoff`: final summary delivered and writing stopped.

The primary must treat `working` and `red` changes as provisional. Do not run whole-repository verification, stage, commit, or diagnose their expected temporary failures. Run only non-overlapping targeted checks until required writers reach `stable` or `handoff`.

A final answer is a `handoff`: the child must stop editing. Use a follow-up task to reopen ownership, and return it to `working` explicitly.

A child reports its final deliverable as a Module Capsule handoff, never as a Relay Capsule. Only the primary may construct a Relay Capsule after it has integrated the child result, completed combined verification, and decided that every relay gate passes.

Children batch routine progress and local test/retry updates into the next permitted state
transition or final Module Capsule. They send messages only for a writer-state transition, a
blocker, a Scope Amendment, unique decision-needed evidence, or final handoff. An ordinary
green rerun, routine retry, or unchanged progress observation is not a separate message; keep
its compact evidence in the child ledger and handoff instead.

Children must not stage, commit, switch branches, rewrite history, remove unrelated files, or start a heavy shared job unless the capsule grants that exact action. If a child starts a local server or other process, it must report ownership and stop it before handoff unless transfer is explicit.

## Investigator Capsule And Convergence

Use an Investigator Capsule for a read-only child whose job is to answer one unique question,
not to own implementation. Target 250–500 tokens. If it would exceed 800 tokens, return the
current capsule with evidence pointers and request a named extension instead of continuing a
general audit.

```markdown
# Investigator Capsule

## Question
- Unique question and evidence-saturation condition

## Findings
- Up to three `confirmed`, `ruled-out`, or `unknown` conclusions

## Contract And Decision Delta
- Public-contract impact or `none`
- Primary decision required, conflict with another result, and bounded alternatives, or `none`

## Evidence
- Up to five current source, test, command, or artifact pointers; no copied logs

## Verification
- Exact read-only checks and `passed` / `failed` / `unavailable` / `not-run` status

## Stop State
- `saturated`, or one named unique uncertainty still remaining
- Confirm no writes, live processes, or transferred resources
```

An oversized narrative or a handoff missing its contract/decision delta is not
integration-ready. The primary extracts or requests the compact capsule before updating the
Phase Checkpoint; it does not paste the narrative into task state.

Before dispatching two or more investigators, keep this compact record:

```text
investigator | unique_question | saturation_condition | status | stop_action
```

Use `open`, `answered`, or `superseded` for status. Refresh the record after the first material
finding and after any change to the controlling contract or test matrix. For `answered` or
`superseded`, request the capsule immediately or interrupt the child; do not wait for a polished
report.

When investigator results materially disagree, the primary records one resolution before
implementation or final acceptance:

```text
decision_id | conflicting_evidence_or_choices | primary_resolution | affected_contracts_and_tests
```

Use a Module Capsule below for writing children or substantial delegated work that owns an
implementation, test, documentation, or other durable boundary.

## Module Capsule

Use a self-contained Module Capsule, normally about 400–800 tokens. If it approaches 1,200 tokens because it needs a broad project summary, narrow the boundary or keep the work with the primary.

```markdown
# Module Capsule

## Goal
- One owned outcome and definition of done

## Owned Boundary
- Behavior, authoritative paths and symbols
- Core write set and any pre-authorized mechanical closure set
- Forbidden paths and actions

## Contracts
- Inputs, callers, outputs, consumers, invariants
- Adjacent dependencies that may be read

## Contract Delta
- Added, changed, or removed public symbols, routes, schemas, configuration, or `none`
- Direct consumers, validators, mocks, tests, and current docs updated or still requiring action

## Evidence
- Confirmed issue or requested change
- Minimal errors, decisions, and source pointers
- Distinct evidence contribution and overlap discovered
- Evidence-saturation condition for stopping this work early

## Validation
- Targeted checks the child owns
- Heavy or combined checks reserved for the primary
- Batched retry evidence, including any `report_in_final` disposition required by the verification ledger

## Deliverable
- Result, changed files, exact checks, risks, Contract Delta, and any batched Scope Amendment
- Writer-state updates and final `handoff`

## Runtime
- Runtime profile, exact model and fixed effort, approvals, sandbox, and resource constraints
```

Omit empty sections. Prefer paths, symbols, line ranges, test names, and artifacts over copied source or narrative history.

## Dispatch And Integration

Before spawning, read `references/model-routing.md` and choose runtime by responsibility. Keep the primary productive while children work.

During execution:

1. Resolve the initial closure scan, then track each child's approved core and mechanical path
   sets, writer state, heavy-resource ownership, and expected deliverable.
   State the communication rule at dispatch: batch routine progress and test retries; do not ask
   for routine green rerun updates outside the permitted writer-state, blocker, Scope Amendment,
   unique decision-needed evidence, or final-handoff messages.
2. Do not interpret a temporary dirty worktree without checking active writer ownership.
3. Keep full suites, production builds, browser acceptance, and final cleanup in the primary's heavy-resource lane unless explicitly transferred.
4. Ask for compact conclusions, evidence pointers, changed files, exact tests, and risks—not raw logs.

5. Stop or interrupt a read-only investigator once its promised evidence is obtained, its
   remaining work becomes duplicative, or the primary can already state the controlling
   contract and test matrix from converged evidence. Keep it running only for a named unique
   uncertainty or deliberate adversarial check.

At integration:

1. Wait for every required writer to reach `stable` or `handoff`.
2. Refresh `HEAD`, staged state, and working-tree status before reviewing changes.
3. After parallel writers are stable or handed off, record the primary's cross-owner seam-review
   decision as `required` or `not-required` with a reason. When required, the primary or one
   bounded read-only reviewer checks producer/consumer identity and order, boundary strictness
   and coercion, authorization and revalidation at the mutation boundary, refactor/import
   closure, and rollback and non-authoritative behavior before combined verification.
4. Verify high-risk evidence and reconcile every Contract Delta against current consumers,
   validators, mocks, tests, and current docs without repeating every child scan.
5. Reconcile conflicts against live source and the controlling contract.
6. Record a Decision Resolution for every material cross-agent contract disagreement.
7. Run combined verification in the primary-owned resource lane.
8. Stage only explicit task paths and commit only after repository-drift checks pass.

Child-local checks never prove combined completion.
