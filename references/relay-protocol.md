# Sequential Relay Protocol

Read this file completely before preparing or creating a `relay-task`.

## Contents

- [Meaning and separation](#meaning-and-separation)
- [Host adapter routing](#host-adapter-routing)
- [Readiness gates](#readiness-gates)
- [Relay value gate](#relay-value-gate)
- [Relay Capsule](#relay-capsule)
- [Safe transfer](#safe-transfer)

## Meaning And Separation

A relay is exactly one sequential successor user-visible task, thread, chat, or conversation for the next substantial phase of the same oversized goal. It begins only after the current phase is integrated and checkpointed; once ownership transfers, the old task stops writing.

Never use relay for parallel speed, specialization, independent review, extra capacity, or model selection. Those needs belong to bounded subagents. Never use a subagent as a hidden long-lived successor for context relief.

Use time and ownership as the tie-breaker:

- concurrent bounded work returning to the current primary means `subagents`;
- sequential transfer of the remaining goal to a fresh primary means `relay-task`;
- if neither is clearly justified, continue `single-agent` with checkpoints.

Use subagent-spawning tools only for subagents and user-visible task/thread tools only for relay. If the user explicitly requests separate conversations, follow the host's thread-management rules rather than treating that as automatic orchestration.

## Host Adapter Routing

Follow the current surface's thread-management rules before creating a successor. When the
surface is Codex Desktop or another Codex app surface exposing project/thread tools, read and
follow [codex-desktop-relay.md](codex-desktop-relay.md). On other surfaces, do not imitate its
tool names; apply this relay contract through the available host-native tools.

Host rules for project selection, worktree use, runtime overrides, queued task handles, and
user-facing directives outrank router preferences. Apply `model-routing.md` only to fields the
host permits the agent to choose.

## Readiness Gates

Keep relay exceptional. Every readiness gate must pass:

1. The current phase has a stable boundary and is completed or explicitly checkpointed.
2. Current state is recoverable from source, commits, files, recorded external state, or an authorized working-tree transfer.
3. The next phase is substantial and self-contained.
4. No unresolved approval, user decision, hidden assumption, active writer, red state, heavy resource, or external side effect remains in the old task.
5. Durable instructions or the user's prompt authorize automatic relay creation; otherwise prepare the capsule and request confirmation.

Also require at least one context-risk signal:

- compaction occurred and substantial work remains;
- large obsolete logs, screenshots, tool output, or discarded hypotheses crowd the reasoning trail;
- several phases completed and the next phase needs materially different focus;
- a compact factual handoff is now more useful than the transcript.

Compaction, complexity, or length alone is not a benefit.

## Relay Value Gate

After readiness and context-risk gates pass, require every value condition:

1. Name the specific impairment the successor removes.
2. Externalize every correctness-critical decision, invariant, approval, ownership fact, verification limitation, and unresolved risk.
3. Confirm the successor can access the authoritative workspace, revision, checkpoint, artifacts, and external state.
4. Confirm remaining work is large enough to amortize handoff, live-state verification, and reacquisition.
5. Compare against same-task checkpoint continuation explicitly; context relief and phase focus must materially outweigh information loss and reacquisition cost.

If uncertain, stay in the current task. If externalization is incomplete, repair the checkpoint before reconsidering relay.

Do not relay during unstable debugging, while a child is `working` or `red`, when the next step is small, when the reasoning trail remains coherent, or when runtime/external state cannot transfer safely.

A child's `stable` result is not a relay-ready primary state. Obtain its final Module Capsule handoff, freeze that writer, integrate the result, run combined verification, and update the Phase Checkpoint before constructing any Relay Capsule. The primary constructs the Relay Capsule; never ask a child to substitute its local handoff for primary-owned integration evidence.

## Relay Capsule

Use a concise, factual capsule in the successor's initial prompt. Target roughly 600-900 tokens
and treat 1,200 tokens as a hard ceiling. Omit empty sections and details already recoverable
from named commits, plans, manifests, or current source. If correctness-critical state cannot
fit after using evidence pointers, create one successor-accessible durable artifact only when
the task authorizes that write; otherwise continue in the current task. Never solve context
pressure by pasting an oversized transcript into the successor prompt.

```markdown
# Relay Capsule

## Goal And Done Criteria
- Final outcome, constraints, non-goals, verification

## Completed Phase
- Completed work and evidence
- Work not to repeat

## Current State
- Project, working directory, branch, revision
- Modified, staged, and untracked files
- Change Manifest location when the exact change set is too large for this capsule
- Active processes, Runtime Leases, runtime or external state
- Authoritative files, symbols, and artifacts

## Decisions And Ownership
- Decisions, rationale, invariants
- Integrated public Contract Deltas
- User-owned changes and write owners

## Verification Ledger
- Structured attempt history and current passed, failed, unavailable, and not-run statuses
- Exact commands or acceptance checks, decisive evidence, superseded attempts, and residual risk

## Relay Value And Loss Controls
- Context impairment removed
- Knowledge at risk and recovery location
- Why remaining work amortizes handoff
- Why same-task continuation is materially worse

## Remaining Work
- Next-phase outcome, sequence, risks, blockers, open questions

## First Action
- Exact live-state checks and first concrete action

## Successor Runtime
- Terra bounded-work or Sol judgment/integration profile, exact model/effort, and availability handling
```

Reference files and artifacts instead of pasting logs. Do not rely on tacit conversation memory. Read `references/model-routing.md` before assigning the successor runtime.

## Safe Transfer

1. Complete current-phase subagents, integration, combined verification, and cleanup.
2. Refresh `HEAD`, branch, staged state, working-tree status, Change Manifest, active processes,
   Runtime Leases, and external state. Stop each task-owned live process or record an explicit
   successor transfer with its owner, PID, port, purpose, freshness evidence, and cleanup duty.
3. Update the Phase Checkpoint and verification ledger.
4. Confirm no writer remains `working` or `red` and no unknown repository drift is unresolved.
5. Build the Relay Capsule and create only one successor.
6. Require the successor to verify live source, revision, checkpoint, decisions, and remaining scope.
7. Transfer ownership and stop old-task writes only after the successor confirms it can continue without reconstructing the completed phase.

Prefer a fresh task created with the host's task-creation tool. Do not use full-history fork for context relief and do not use Git-environment handoff as a substitute for conversation handoff.

If uncommitted work cannot transfer safely, continue in the current task or request authorization. Never assume a clean worktree contains required edits. Never run old and successor tasks as concurrent writers.

Leave the old task available as evidence unless the user asks to archive it. The successor re-runs the router at its next major phase boundary.
