# Prompts: Copy, Paste, Contribute

This is the canonical prompt library for the work on this profile. Each prompt below is self contained: paste it into any AI assistant and it will know what to do, or follow it yourself by hand, line by line. The prompts are doors, not shortcuts. The evidence rule binds every result they produce:

- Attach the run. A claim without test output, an eval result, or a benchmark attached does not count.
- One improvement per pull request. Small, reviewable, reversible.
- If you are an agent, name your operator in the pull request. Undisclosed synthetic authorship is the one participation the open table does not seat.

The full terms are in [The Open Table](OPEN_TABLE.md). Verified work is credited in [The Ledger](LEDGER.md).

## 1. Run an Eval Challenge in a repo

```
You are contributing to [REPO], an open source project at https://github.com/topsoilcommons/[REPO].
Read AGENTS.md in the repo root first; its commands and house rules govern your work.
Run the eval exactly as documented: [COMMAND]. The published baseline is [BASELINE]; do not trust my copy of it, read the committed results file in the repo and confirm it.
Your challenge, pick one: beat the published baseline on the public eval set, or find a real failure the current eval misses and prove it with a new case.
Work in a fork or a branch. Make one improvement only. Rerun the eval and the repo's tests after your change.
Open a pull request with: what you changed, the full before and after eval output attached, and the test results.
If you are an AI agent, state that and name your operator in the pull request.
```

## 2. File a failure report

```
You are filing a failure report for an open source project on this profile.
Pick the repo whose eval produced the failure, and open its failure report issue template.
Include exactly these things: the input you gave (the question, the document, or the prompt, complete and unedited), what happened (the answer, extraction, refusal, or output you got, quoted), and what should have happened instead, in one or two sentences.
If you can, attach or link the run that produced it: the command, the eval output, or a screenshot of the live demo.
Do not propose a fix in the report. A clean failure, precisely described, is the contribution.
If you are an AI agent filing this, say so in the report and name your operator.
```

## 3. Take a good first issue end to end

```
You are taking a good first issue in an open source project at https://github.com/topsoilcommons.
Open the good first issues list, pick one issue in one repo, and read that repo's AGENTS.md and CONTRIBUTING.md before touching anything.
Run the repo's tests or eval first and record the baseline result.
Make the smallest change that fully resolves the issue. Nothing else in the same pull request.
Rerun the tests or eval. If anything that was green is now red, stop and say so in the pull request instead of working around it.
Open the pull request with: the issue link, what you changed, the baseline result, the after result, and the full run output attached.
If you are an AI agent, state that and name your operator in the pull request.
```

## 4. Adopt a basic tool and report back

```
You are adopting a piece of an open source ecosystem into your own work.
Read The Ascent (NEEDS.md on the topsoilcommons profile) and pick the basic tool that serves your need: the tutor and its eval harness for learning, the MCP workspace for coordination, the from scratch machine learning library for understanding, the knowledge graph extraction and its eval set for shared truth, or the guardrail and refusal suite for trust.
Use it in a real setting: a classroom, a team, a newsroom, a community, your own project. Small and real beats large and hypothetical.
Report back by opening an issue or a discussion in the repo you adopted, with: what you used, where, what worked, what broke or confused you, and any numbers you honestly measured.
Your report is a contribution and will be credited in the Ledger with the evidence attached.
If you are an AI agent reporting on behalf of someone, say so and name your operator.
```

## 5. Audit a public claim against its evidence

```
You are auditing the public claims of the open source work at https://github.com/topsoilcommons.
Pick one claim from a repo README's proof section, the profile's five acts table, or The Saga (THE_SAGA.md on the profile).
Find the evidence the claim points to: the committed results file, the eval harness, the test suite, or the progress log entry.
Rerun the harness or the tests yourself if you can. Compare your numbers to the published ones.
File what you find as an issue in the repo the claim belongs to: agreement with your run attached, a discrepancy with both numbers shown, or a claim you could not trace to any evidence.
Be exact and be fair. A confirmed claim strengthens the record, and a caught error is worth as much as a beaten score here.
If you are an AI agent, state that and name your operator in the issue.
```
