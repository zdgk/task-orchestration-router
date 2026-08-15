# Codex Desktop Relay Adapter

Read this file only when a sequential relay uses Codex Desktop/app project and thread tools.
The generic readiness, value, capsule, and safe-transfer gates remain authoritative.

## Resolve The Destination

1. List projects first and select the exact saved project. Record its project ID, host ID,
   path, and whether it is a Git repository.
2. For a Git repository, prefer an isolated worktree when all required state is committed or
   otherwise recoverable there. Use the host's default starting state unless the user explicitly
   requested a particular existing branch, ref, or working-tree state.
3. Use the saved project's local environment only when the user explicitly asked to continue
   in that direct workspace, or when required state cannot safely transfer to a worktree and the
   strict sequential handoff can protect the shared tree. Do not use `local` merely for
   convenience.
4. If neither environment can recover the authoritative revision and required state, do not
   create the relay.

## Protect A Shared Local Workspace

When the successor will use the same local working tree, make its first turn read-only takeover
verification only. Require it to check the project path, branch, HEAD, staged and unstaged state,
user-owned artifacts, active writers, processes, and the next-phase boundary, then stop that
turn with an acknowledgement. The predecessor performs no further task writes after dispatch.
Only after the acknowledgement may a follow-up activate successor writes.

For an isolated worktree, source writes cannot collide, but the relay is still sequential: the
predecessor does not continue the remaining goal after dispatch.

## Create And Confirm

1. Create exactly one project thread. Thread creation is non-blocking.
2. Omit model and reasoning fields when host policy reserves them for an explicit user choice.
   Record the router's recommended profile in the capsule without claiming the host default
   satisfied it.
3. A returned `threadId` is waitable. A queued `clientThreadId` is not a thread ID and must not
   be passed to read, wait, or messaging tools. Do not transfer ownership until the host resolves
   a real thread and the successor acknowledges the checkpoint.
4. Wait using the host's thread-wait tool and an up-to-date cursor. Treat commentary as progress,
   not as transfer confirmation unless the host contract makes it terminal.
5. If the successor reports drift, missing state, a decision request, or inability to continue,
   keep the goal with the predecessor until the condition is resolved.

## Finish The Predecessor

After acknowledgement, stop predecessor writes, report only the completed phase and relay
state, and emit the host-required created-thread directive. Do not archive the predecessor
unless the user asks. Never emit a created-thread, Git, or completion directive before the
underlying action succeeds.
