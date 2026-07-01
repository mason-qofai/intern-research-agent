# intern-research-agent

An agent built to research public sources and compile a dossier on a single middle-market PE firm, for internal use at QofAI. The repo demonstrates progression from manual research to subagent orchestration across four dossier versions of the same firm.

## Structure

```
intern-research-agent/
├── prompts/    # Three contract documents governing agent behavior:
│               #   research-agent.md, source-rubric.md, confidence-rubric.md
├── skills/     # Eight skill folders used by the agent
├── scripts/    # Executable entry points and utilities
├── sources/    # Raw input material pulled from public research
├── dossiers/   # Four dossier versions, manual through orchestrated
├── audits/     # Self-audit and reflection
├── evals/      # 50-example eval set, labels, results, and capstone-memo.md
├── runs/       # Run log demonstrating subagent orchestration (pending)
└── README.md
```

## Governing contracts

Three documents under prompts/ set the rules the agent follows: how it selects and weighs sources, how it classifies source types, and how confident it states its conclusions to be. Their contents are intentionally not summarized here; refer to the documents directly for the full protocol.

## Setup

Pending. No dependencies or scripts exist yet.

## Run

Pending. This section will be filled in once the agent has a working entry point.

## Status

Scaffold complete. Contract documents, skills, dossiers, evals, and run log are in progress.
