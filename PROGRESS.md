# Progress log

This is the public record of the work: what was done, what the proof shows, what broke, and what comes next. It is updated every work session, newest first, in plain language on purpose. If a claim anywhere in these projects cannot be traced to a logged run, the claim is wrong and the log is where it gets corrected.

## October 14 to 15, 2026: Launch

**What shipped.** Five open source projects and this profile, published on GitHub with live demos:

- Supergravity, an AI learning atlas with a published tutor evaluation: https://github.com/jthomas48896f/supergravity and demo at https://jthomas48896f.github.io/supergravity/
- Cohort, a community platform with an MCP server for AI agents: https://github.com/jthomas48896f/cohort
- Neural Net Lab, machine learning built from scratch, including a transformer: https://github.com/jthomas48896f/neural-net-lab
- Knowledge Graph Explorer, knowledge extraction that publishes its own errors: https://github.com/jthomas48896f/knowledge-graph-explorer
- LUMEN, a guarded question answering study with a public refusal evaluation: https://github.com/jthomas48896f/lumen-faith-platform

**The proof, as logged.** The tutor evaluation scored groundedness 0.806 with a citation rate of 1.0, and its weak subjects are named in the report rather than hidden. The from scratch transformer passes 7 of 7 gradient checks and trained a small language model from a validation loss of 5.297 down to 2.413; the same model in PyTorch ran 4.13 times faster per step, and that comparison is published too. Knowledge extraction scored entity F1 of 0.937 and relation F1 of 0.605 on hand labeled documents, with the precision tradeoff stated in the open. The refusal evaluation blocked 12 of 12 harmful requests and allowed 8 of 8 legitimate ones.

**What broke, and the fixes, in the open.** Publishing was blocked for days by a missing app installation that produced misleading permission errors; the root cause was found and fixed, and the account now publishes by direct git push. Two batches of the largest project's data were lost to commit races during a parallel upload and were recovered and verified file by file, all 210 files accounted for. The flagship demo first rendered blank because the hosting platform silently drops files whose names begin with an underscore, and because one generated bundle is built at deploy time; both causes were found, fixed, and committed with the reasons recorded.

**What is next.** Continuous integration confirmed green on every repo, good first issues opened for new contributors, version 0.1 releases, the LinkedIn profile rebuilt around this evidence, and the first public checkpoint on November 16, 2026, where the plan is measured against real numbers.

## How this log works

One entry per work session. Every entry separates what shipped from what the proof shows, names what broke, and states what is next. The intentions behind the work are in INTENTIONS.md, and the long term design is in ECOSYSTEM.md, both in this profile.
