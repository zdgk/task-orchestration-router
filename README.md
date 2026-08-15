# Task Orchestration Router

An Agent Skill for choosing the smallest reliable execution topology for complex Codex work.

It helps an agent decide when to stay single-agent, delegate bounded work to subagents, or hand a stable phase to a sequential relay. The workflow also protects shared repositories, active writers, scarce runtimes, and the integrity of verification evidence.

## What it covers

- Activation gates for trivial versus genuinely complex work
- Phase-scoped topology selection
- Single-writer and repository-drift safeguards
- Bounded subagent admission, ownership, and handoff contracts
- Sequential relay readiness and context-loss controls
- Runtime leases for browser, server, and stateful preview evidence
- Verification ledgers that preserve failed and unavailable attempts
- Conditional cross-owner seam review
- Host-aware model routing

## Install

Ask Codex to install the skill from this repository:

```text
Use $skill-installer to install https://github.com/zdgk/task-orchestration-router
```

For a manual user-level installation, clone or copy this repository to:

```text
$HOME/.agents/skills/task-orchestration-router
```

The directory containing `SKILL.md` is the skill root.

## Use

Invoke it explicitly:

```text
Use $task-orchestration-router to plan and execute this multi-phase migration safely.
```

The included OpenAI metadata also permits implicit invocation when a request matches the skill description. The router remains inactive for trivial work and may still select a single-agent route for complex but tightly coupled tasks.

## Structure

```text
task-orchestration-router/
├── SKILL.md
├── agents/openai.yaml
├── references/
│   ├── codex-desktop-relay.md
│   ├── evaluation-cases.md
│   ├── model-routing.md
│   ├── relay-protocol.md
│   └── subagent-protocol.md
└── scripts/validate_contract.py
```

The main skill loads detailed protocols only when the selected route needs them.

## Validation

Run the bundled contract validator:

```bash
python scripts/validate_contract.py
```

The validator checks activation, topology, writer safety, repository drift, runtime freshness, verification truth, relay boundaries, model routing, and evaluation-case coverage.

## Compatibility notes

- The core workflow degrades to single-agent execution when subagent or thread tools are unavailable.
- The Codex Desktop relay adapter is conditional and should not be loaded on hosts without compatible thread tools.
- The bundled model catalog names Codex Terra and Sol profiles. Explicit user choices and higher-priority host rules take precedence; unavailable profiles must not be silently substituted.
- This is a control-layer skill. Domain-specific skills remain responsible for implementation details and quality gates.

## License

MIT
