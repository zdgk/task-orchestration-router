from pathlib import Path
import sys


root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parents[1]


def read(relative_path: str) -> str:
    """Read one required UTF-8 skill artifact from the selected root."""
    return (root / relative_path).read_text(encoding="utf-8")


skill = read("SKILL.md")
metadata = read("agents/openai.yaml")
cases = read("references/evaluation-cases.md")
subagent = read("references/subagent-protocol.md")
model = read("references/model-routing.md")
relay = read("references/relay-protocol.md")
desktop_relay = read("references/codex-desktop-relay.md")
all_docs = "\n".join((
    skill,
    metadata,
    cases,
    subagent,
    model,
    relay,
    desktop_relay,
))
model_profile_rows = [
    line for line in model.splitlines()
    if line.startswith("| **") and "`gpt-5.6-" in line
]


def has_all(text: str, *terms: str) -> bool:
    """Return whether every contract term is present in one artifact."""
    return all(term in text for term in terms)


checks = {
    "activation and shared-safety preflight": "shared-execution-safety preflight" in skill,
    "activation gate exists": has_all(skill, "## Decide Whether The Router Is Active", "`inactive`", "`active`"),
    "trivial work stays inactive": has_all(
        skill,
        "single-answer question",
        "simple rewrite",
        "one obvious low-risk local edit",
        "tiny linear sequence",
    ),
    "small high-risk work stays active": "security, safety, data-integrity, destructive, or irreversible risk" in skill,
    "active work may remain single": "an active request may still route to `single-agent`" in skill,
    "conditional reference routing exists": has_all(
        skill,
        "references/subagent-protocol.md",
        "references/model-routing.md",
        "references/relay-protocol.md",
        "references/codex-desktop-relay.md",
        "references/evaluation-cases.md",
    ),
    "inactive work avoids irrelevant references": "Do not read relay or model-allocation detail for an inactive request" in skill,
    "current phase only": has_all(skill, "Select only the current phase", "Do not dispatch future work"),
    "execution route and investigation support are separate": has_all(
        skill,
        "exactly one execution route",
        "Track investigation support separately",
        "`read-only-investigators`",
        "does not create a fourth route",
    ),
    "multi-investigator convergence is explicit": has_all(
        skill,
        "Investigation Convergence",
        "unique question",
        "saturation condition",
        "answered or superseded",
        "do not wait for a polished narrative",
    ),
    "primary owns controlling contracts": has_all(
        skill,
        "Establish the controlling contract",
        "architecture, public interfaces, invariants, and write ownership",
    ),
    "delegated boundaries close before writing": has_all(
        skill,
        "Close delegated boundaries before writing",
        "direct callers and consumers",
        "mechanical closure set",
    ),
    "primary remains productive": has_all(skill, "Keep the primary productive", "not only a scheduler"),
    "phase baseline is explicit": has_all(
        skill,
        "Capture the phase baseline",
        "branch/revision",
        "user-owned changes",
        "active writers",
        "verification ledger",
    ),
    "combined verification is mandatory": has_all(
        skill,
        "Verify the combined state",
        "Child-local checks never prove the phase complete",
    ),
    "phase re-evaluation is bounded": has_all(skill, "Re-evaluate after a major investigation", "not after every tool call"),
    "unchanged re-evaluation stays internal": "If the route and ownership remain unchanged, record the re-evaluation internally" in skill,
    "writer lifecycle is complete": has_all(skill, "`working`", "`red`", "`stable`", "`handoff`"),
    "active-writer barrier exists": has_all(
        skill,
        "While any required writer is `working` or `red`",
        "do not run whole-repository verification, stage, commit",
        "wait for `stable` or `handoff` before integration",
    ),
    "handoff freezes ownership": "A child's final handoff freezes its write ownership" in skill,
    "conditional cross-owner seam review is explicit": has_all(
        skill,
        "### Decide A Conditional Cross-Owner Seam Review",
        "parallel writers reach `stable` or `handoff`",
        "public, wire,\npersistence, mutation, or state-consumer contract",
        "required/not-required",
    ),
    "required seam review checks cross-owner integrity": has_all(
        skill,
        "producer/consumer identity and order",
        "boundary strictness and coercion",
        "authorization and revalidation at the mutation boundary",
        "refactor/import closure",
        "rollback\nand non-authoritative behavior",
    ),
    "seam review remains conditional": has_all(
        skill,
        "Otherwise record `not-required`",
        "not mandatory\nfor every delegated phase",
        "before combined verification",
    ),
    "primary owns Git by default": "The primary agent stages and commits by default" in skill,
    "repository state is refreshed": has_all(skill, "Before integration, staging, and every commit", "Re-read `HEAD`, branch, staged state, and working-tree status"),
    "repository drift is classified": has_all(skill, "Classify every new change or commit", "primary-owned", "child-owned", "user-owned", "generated", "unknown"),
    "unexpected HEAD movement is inspected": "If `HEAD` moved unexpectedly, inspect the intervening commits" in skill,
    "heavy resources are serialized": has_all(
        skill,
        "Assign one owner at a time to heavy or stateful resources",
        "Do not overlap heavy jobs",
    ),
    "primary owns combined resource lane": "The primary normally owns combined tests, production builds, browser acceptance, and final cleanup" in skill,
    "process ownership is recorded": "Record started processes and ensure the owning agent stops or hands them off explicitly" in skill,
    "runtime freshness gate is explicit": has_all(
        skill,
        "## Prove Runtime Freshness Before Acceptance",
        "PID or handle",
        "proxy target",
        "OpenAPI route",
        "unproven or stale runtime as `unavailable` evidence",
    ),
    "runtime lease rejects unknown listeners": has_all(
        skill,
        "Runtime Lease",
        "start time",
        "existing listener whose ownership or source is unknown",
        "dedicated free port",
        "Stop only a task-owned runtime",
    ),
    "verification ledger statuses are exact": has_all(skill, "`passed`", "`failed`", "`unavailable`", "`not-run`"),
    "verification retries preserve attempt history": has_all(
        skill,
        "ordered attempt history",
        "latest authoritative attempt",
        "earlier attempt remains visible",
    ),
    "verification attempts use a required schema": has_all(
        skill,
        "check_id | attempt | status | owner | command_or_acceptance | decisive_evidence | supersedes",
        "Append retries instead of rewriting history",
        "material earlier `failed` or `unavailable` attempt",
    ),
    "verification attempts carry final-report dispositions": has_all(
        skill,
        "report_in_final | report_reason",
        "Set `report_in_final` to `yes` or `no` for every attempt",
        "environment, command, or residual risk",
    ),
    "flagged attempt history survives checkpoints and compaction": has_all(
        skill,
        "Phase Checkpoint and survive compaction",
        "every\n   `report_in_final: yes` disposition and reason",
        "rehydrate every required current status and every attempt flagged",
    ),
    "finalization gate preserves material history": has_all(
        skill,
        "### Run The Finalization Gate",
        "every required check has one current status",
        "every current `unavailable` or `not-run` limitation is explicit",
        "latest `passed` attempt never erases material retry history",
    ),
    "finalization gate compares the draft and blocks omissions": has_all(
        skill,
        "compare the draft final report",
        "every attempt with `report_in_final: yes`",
        "Completion is blocked if the\ndraft omits any required current status or attempt flagged for final reporting",
    ),
    "current green checks may be grouped": has_all(
        skill,
        "routine current passes may be grouped",
        "rather than list every green subcheck",
        "covered checks are clear",
    ),
    "unavailable is truthful": has_all(skill, "`unavailable` is neither a code failure nor a pass", "fully green"),
    "checkpoints are proportionate": has_all(skill, "## Build A Proportionate Phase Checkpoint", "current plan plus live repository state", "dedicated workspace artifact only when"),
    "checkpoints have a compact recovery template": has_all(
        skill,
        "goal, done criteria, and controlling contract",
        "at most three next concrete actions",
        "300-600 tokens",
        "evidence pointers",
    ),
    "large change sets use a reconciled manifest": has_all(
        skill,
        "Change Manifest",
        "path or symbol",
        "public-contract impact",
        "git diff --name-status",
        "neither expands authority",
    ),
    "compaction prefers same-task recovery": has_all(skill, "After compaction, rehydrate from the checkpoint", "Compaction alone never justifies relay"),
    "topology changes by phase": has_all(skill, "## Choose The Current Topology", "`single-agent`", "`subagents`", "`relay-task`"),
    "subagent route loads detailed protocol": has_all(skill, "### Route To Subagents", "references/subagent-protocol.md", "references/model-routing.md"),
    "relay route is sequential and exceptional": has_all(skill, "exactly one fresh user-visible successor", "Keep relay exceptional"),
    "subagent admission gates are bounded": has_all(
        subagent,
        "At least two current-phase workstreams are independently actionable now",
        "explicit non-overlapping sets",
        "Do not spawn future-phase workers",
    ),
    "subagent evidence deltas and saturation are bounded": has_all(
        subagent,
        "distinct expected evidence contribution",
        "evidence-saturation stop condition",
        "Stop or interrupt a read-only investigator",
        "deliberate adversarial check",
    ),
    "subagent isolation uses fresh context": has_all(subagent, "Use `fork_turns: none` by default", "Never pass the full transcript merely for convenience"),
    "subagent closure scan and amendments are batched": has_all(
        subagent,
        "## Boundary Closure And Scope Amendments",
        "Before the first edit",
        "batched proposed closure",
        "blocking closure",
        "required contract closure",
        "adjacent follow-up",
        "Do not edit an unapproved path",
    ),
    "children batch routine progress and retry chatter": has_all(
        subagent,
        "batch routine progress and local test/retry updates",
        "writer-state transition",
        "unique decision-needed evidence",
        "green rerun, routine retry, or unchanged progress observation",
    ),
    "dispatch keeps routine green reruns quiet": has_all(
        subagent,
        "State the communication rule at dispatch",
        "routine green rerun updates",
        "final-handoff messages",
    ),
    "subagent integration records the seam-review decision": has_all(
        subagent,
        "After parallel writers are stable or handed off",
        "decision as `required` or `not-required` with a reason",
        "bounded read-only reviewer",
        "rollback and non-authoritative behavior before combined verification",
    ),
    "blind validation is protected": has_all(subagent, "ordinary user-like task", "expected answer", "suspected defect", "intended fix", "evaluator-only artifacts"),
    "investigator capsule is bounded": has_all(
        subagent,
        "## Investigator Capsule And Convergence",
        "Target 250–500 tokens",
        "If it would exceed 800 tokens",
        "Up to three",
        "Up to five",
        "## Stop State",
    ),
    "investigator convergence statuses are actionable": has_all(
        subagent,
        "investigator | unique_question | saturation_condition | status | stop_action",
        "Use `open`, `answered`, or `superseded`",
        "request the capsule immediately or interrupt the child",
    ),
    "cross-agent decisions are resolved": has_all(
        subagent,
        "decision_id | conflicting_evidence_or_choices | primary_resolution | affected_contracts_and_tests",
        "Decision Resolution",
        "material cross-agent contract disagreement",
    ),
    "module capsule is concrete": has_all(subagent, "# Module Capsule", "## Owned Boundary", "## Contracts", "## Validation", "## Deliverable"),
    "module capsule carries contract deltas": has_all(
        subagent,
        "## Contract Delta",
        "public symbols, routes, schemas, configuration",
        "Direct consumers, validators, mocks, tests, and current docs",
    ),
    "children cannot mutate Git by default": "Children must not stage, commit, switch branches, rewrite history" in subagent,
    "child handoff is not a relay capsule": has_all(subagent, "Module Capsule handoff, never as a Relay Capsule", "Only the primary may construct a Relay Capsule"),
    "integration waits and refreshes": has_all(subagent, "Wait for every required writer", "Refresh `HEAD`, staged state, and working-tree status", "Run combined verification"),
    "relay and subagents remain distinct": has_all(
        relay,
        "Never use relay for parallel speed",
        "Never use a subagent as a hidden long-lived successor",
        "concurrent bounded work returning to the current primary",
        "sequential transfer of the remaining goal",
    ),
    "relay readiness is strict": has_all(relay, "Every readiness gate must pass", "No unresolved approval", "active writer", "red state", "context-risk signal"),
    "relay value compares continuation": has_all(
        relay,
        "Compare against same-task checkpoint continuation explicitly",
        "context relief and phase focus must materially outweigh information loss and reacquisition cost",
    ),
    "relay capsule carries loss controls": has_all(relay, "# Relay Capsule", "## Verification Ledger", "## Relay Value And Loss Controls", "## First Action"),
    "relay capsule carries manifests leases and deltas": has_all(
        relay,
        "Change Manifest location",
        "Runtime Leases",
        "Integrated public Contract Deltas",
        "Structured attempt history",
    ),
    "relay transfer resolves drift and writers": has_all(relay, "no writer remains `working` or `red`", "no unknown repository drift is unresolved"),
    "relay requires primary integration after child handoff": has_all(relay, "A child's `stable` result is not a relay-ready primary state", "final Module Capsule handoff", "run combined verification", "The primary constructs the Relay Capsule"),
    "relay resolves live processes": has_all(relay, "Stop each task-owned live process or record an explicit", "PID", "cleanup duty"),
    "relay ownership transfers after confirmation": "Transfer ownership and stop old-task writes only after the successor confirms" in relay,
    "relay capsule is hard bounded": has_all(
        relay,
        "Target roughly 600-900 tokens",
        "1,200 tokens as a hard ceiling",
        "evidence pointers",
        "continue in the current task",
    ),
    "desktop relay adapter is conditional": has_all(
        skill,
        "references/codex-desktop-relay.md",
        "Do not load that\nhost adapter on a surface without Codex thread tools",
    ) and has_all(
        relay,
        "## Host Adapter Routing",
        "codex-desktop-relay.md",
        "Host rules",
    ),
    "desktop relay resolves project environment": has_all(
        desktop_relay,
        "List projects first",
        "prefer an isolated worktree",
        "Use the saved project's local environment only when",
        "Do not use `local` merely for\n   convenience",
    ),
    "desktop local relay uses read-only acknowledgement": has_all(
        desktop_relay,
        "first turn read-only takeover\nverification only",
        "performs no further task writes after dispatch",
        "Only after the acknowledgement may a follow-up activate successor writes",
    ),
    "desktop relay handles nonblocking creation": has_all(
        desktop_relay,
        "Thread creation is non-blocking",
        "A queued `clientThreadId` is not a thread ID",
        "must not\n   be passed to read, wait, or messaging tools",
        "successor acknowledges the checkpoint",
    ),
    "model catalog has exactly two fixed profiles": len(model_profile_rows) == 2 and has_all(
        model,
        "## Fixed Two-Profile Mapping",
        "Terra bounded-work agent",
        "Sol judgment/integration agent",
        "Use exactly one profile",
    ),
    "terra bounded profile is fixed at max": any(
        "Terra bounded-work agent" in row
        and "`gpt-5.6-terra`" in row
        and "`max`" in row
        for row in model_profile_rows
    ) and has_all(model, "Every router-selected Terra assignment uses `max`", "Do not lower, promote, or swap"),
    "sol judgment profile is fixed at xhigh": any(
        "Sol judgment/integration agent" in row
        and "`gpt-5.6-sol`" in row
        and "`xhigh`" in row
        for row in model_profile_rows
    ) and "router-selected Sol assignment uses `xhigh`" in model,
    "model catalog covers bounded routine work": has_all(
        model,
        "bounded implementation, tests, UI",
        "routine read-only checks, documentation, data organization, and repetitive work",
    ),
    "mixed work establishes judgment before execution": has_all(
        model,
        "Sol establishes or repairs the contract",
        "executes the resulting bounded work",
    ),
    "terra escalates sol-owned questions": has_all(
        model,
        "A Terra agent stops at the current safe boundary",
        "unapproved shared-interface change",
        "proposed Scope Amendment",
        "does not decide the Sol-owned question",
    ),
    "model routing follows responsibility": "Classify the assigned responsibility, not the subject" in model,
    "high-risk judgment stays with sol": has_all(
        model,
        "Sol judgment/integration profile",
        "safety or",
        "data-integrity judgment",
        "final acceptance",
    ),
    "model unavailability never silently substitutes": has_all(
        model,
        "If an exact profile is unavailable",
        "do not silently substitute another model or effort",
        "Do not claim that a different runtime satisfied either fixed profile",
    ),
    "host-owned runtime selection is explicit": has_all(
        model,
        "## Host-Owned Runtime Selection",
        "omitting model or effort fields unless the user explicitly",
        "record the router's recommended Terra or Sol profile",
        "label the actual runtime as `host-default` or `host-selected`",
        "do not treat host-owned omission as silent substitution",
    ) and has_all(
        desktop_relay,
        "Omit model and reasoning fields when host policy reserves them for an explicit user choice",
        "without claiming the host default\n   satisfied it",
    ),
    "model names are replaceable catalog": "exact model names as a replaceable catalog layer" in model,
    "execution cases cover active-writer barrier": has_all(cases, "intentional test-first `red` state", "whole-repository verification", "wait for `stable` or `handoff`"),
    "execution cases cover repository drift": has_all(cases, "`HEAD` moves", "inspect and classify the drift", "user-owned working-tree changes"),
    "execution cases cover resource ownership": has_all(cases, "heavy resource one owner at a time", "serialize combined validation"),
    "execution cases cover runtime freshness": has_all(
        cases,
        "OpenAPI or build marker does not contain the current change",
        "prove freshness before acceptance",
    ),
    "execution cases cover runtime leases": has_all(
        cases,
        "listener whose owner or source revision is unknown",
        "dedicated free port",
        "Re-prove the Runtime Lease freshness signal",
    ),
    "execution cases cover verification truth": has_all(cases, "Mark the audit `unavailable`", "Mark it `not-run`", "do not call the combined state fully green"),
    "execution cases cover retry history": has_all(
        cases,
        "approved retry",
        "current status to `passed`",
        "earlier `unavailable` attempt",
    ),
    "execution cases cover structured multi-attempt history": has_all(
        cases,
        "temporary directory",
        "fails on a real test",
        "Append all three structured attempts",
    ),
    "execution cases preserve reportable retries through compaction": has_all(
        cases,
        "implementation fix, then a later retry passes",
        "Phase Checkpoint is compacted and rehydrated",
        "Every attempt has `report_in_final` plus a reason",
        "survives the checkpoint and compaction",
    ),
    "execution cases reject an omitted flagged attempt": has_all(
        cases,
        "omits an earlier `report_in_final: yes` environmental retry",
        "The Finalization Gate fails",
        "completion remains blocked",
    ),
    "execution cases allow grouped current passes": has_all(
        cases,
        "groups routine current passes by named test suite",
        "does not require a verbose list of every green subcheck",
    ),
    "execution cases cover batched child reporting": has_all(
        cases,
        "four routine green test reruns",
        "send no separate progress messages",
        "unique decision-needed evidence or Scope Amendment",
    ),
    "execution cases cover conditional seam review": has_all(
        cases,
        "Two parallel writers reach `stable`",
        "records seam review `required`",
        "Two parallel writers reach `handoff` with no shared public, wire, persistence, mutation, or state-consumer contract",
        "seam review `not-required`",
    ),
    "execution cases cover closure and contract deltas": has_all(
        cases,
        "boundary-closure scan before editing",
        "one Scope Amendment",
        "Contract Delta at handoff",
    ),
    "execution cases cover change manifests": has_all(
        cases,
        "task-local Change Manifest",
        "reconcile it against live source",
    ),
    "execution cases cover support and saturation": has_all(
        cases,
        "`single-agent` with the `read-only-investigators` support modifier",
        "Stop or interrupt the redundant third investigator",
    ),
    "execution cases cover bounded investigator handoff": has_all(
        cases,
        "2,000-word repository narrative",
        "250–500-token Investigator Capsule",
        "not integration-ready",
    ),
    "execution cases cover convergence and decision resolution": has_all(
        cases,
        "Investigation Convergence record",
        "answered or superseded workstream",
        "primary-owned Decision Resolution",
        "affected contracts and tests",
    ),
    "execution cases enforce finalization retry history": has_all(
        cases,
        "mentions only the latest pass fails the Finalization Gate",
        "reports only the latest passing verification attempt",
    ),
    "execution cases cover quiet re-evaluation": "without routine user-facing topology commentary" in cases,
    "execution cases cover relay handoff boundary": has_all(cases, "reports `stable` but has not sent final `handoff`", "Module Capsule handoff", "run combined verification", "construct any Relay Capsule"),
    "execution cases cover desktop relay adapter": has_all(
        cases,
        "both project worktree and local environments",
        "first turn read-only takeover verification",
        "queued `clientThreadId`",
        "real `threadId` plus successor acknowledgement",
    ),
    "execution cases cover relay capsule ceiling": has_all(
        cases,
        "Relay Capsule grows past 1,200 tokens",
        "Replace repeated detail with evidence pointers",
        "sends a Relay Capsule above the 1,200-token ceiling",
    ),
    "execution cases cover host-owned runtime fields": has_all(
        cases,
        "host forbids model/effort fields",
        "label the actual runtime `host-default`/`host-selected`",
        "host policy reserves for an explicit user choice",
    ),
    "execution cases cover fixed model profiles": has_all(
        cases,
        "Terra bounded-work agent",
        "`gpt-5.6-terra` at `max`",
        "Sol judgment/integration agent",
        "`gpt-5.6-sol` at `xhigh`",
        "Scope Amendment to Sol",
    ),
    "failure cases enforce exact model efforts": has_all(
        cases,
        "`gpt-5.6-terra` any effort other than `max`",
        "`gpt-5.6-sol` any effort other than `xhigh`",
        "silently substitutes a different model or effort",
    ),
    "failure cases enforce report dispositions and conditional seam review": has_all(
        cases,
        "omits `report_in_final` or its reason from an attempt",
        "lets a final draft omit an attempt flagged for final reporting",
        "sends separate routine-progress or green-rerun messages",
        "skips the required/not-required cross-owner seam-review decision",
        "requires\n  that review for every delegated phase",
    ),
    "behavior cases preserve prior protocol": has_all(
        cases,
        "no proven root cause",
        "future-phase agents",
        "combined path is unverified",
        "Phase Checkpoint",
        "blind validation",
    ),
    "metadata reflects execution safety and model profiles": has_all(
        metadata,
        "Task Orchestration Router",
        "close delegated boundaries",
        "protect runtime and repository state",
        "Terra max",
        "Sol xhigh",
    ),
    "implicit invocation is preserved": "allow_implicit_invocation: true" in metadata,
    "no placeholders": not any(token in all_docs for token in ("TODO", "PLACEHOLDER", "FIXME")),
}

failed = []
for name, passed in checks.items():
    print(f"{'PASS' if passed else 'FAIL'}: {name}")
    if not passed:
        failed.append(name)

if failed:
    raise SystemExit(f"Contract validation failed: {len(failed)} check(s)")

print(f"Contract validation passed: {len(checks)} checks")
