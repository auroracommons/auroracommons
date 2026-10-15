# Progress log

This is the public record of the work: what was done, what the proof shows, what broke, and what comes next. It is updated every work session, newest first, in plain language on purpose. If a claim anywhere in these projects cannot be traced to a logged run, the claim is wrong and the log is where it gets corrected.

## October 15, 2026: the specificity pass

**What shipped.** The front doors now say what exists instead of what it means. This profile opens with the five projects as deliverables, one line each with the number that proves it, plus the other tangible things that exist today: the live demos, the Ledger, the Eval Challenge, and the published documents. The visual front page hero says the same in one breath. The Atlas, Cohort, and Lumen READMEs now open with their deliverable and its receipt; Machine and Graph already opened that way and were left alone.

**The proof.** Words only. No number changed anywhere, no claim was added, and the dated entries below stand exactly as written.

**What is next.** Unchanged: the twice daily evolution pass, the November 16, 2026 checkpoint, and the first Ledger entries from outside contributors.

## October 15, 2026: the Aurora pivot, names that serve all

**What shipped.** Every name in this work changed today, in one pass, at the founder's direction. Bedrock Commons is now Aurora Commons, and the map of human needs, The Bedrock, is now The Ascent. The five acts carry the names of what they are: Supergravity is now Atlas, Neural Net Lab is now Machine, Knowledge Graph Explorer is now Graph, and LUMEN is now Lumen; Cohort keeps its name. The account, all six repositories, every demo address, the visual front page, and the published documents were swept to the new names, and the front page was rebuilt visual first: the Ascent drawn, the acts as cards, the Proof as one diagram, captions instead of essays. Lumen's README now states its framing plainly: the guardrail method belongs to no tradition, each community's own texts are guarded by that community's own rules, its current corpus is a first exhibit from one tradition, and the door is open to every tradition's texts and to secular works of meaning.

**The proof.** The reason is the record's own logic, stated by the founder in four words: serve all. A commons that belongs to everyone cannot carry names that belong to one field, one tradition, or one stone. What did not change is everything that carries weight: every published number stands exactly as measured, the one rule stands (be fair to others), the advisor framing stands, and the historical entries below stand exactly as written, under the names of their day, because a public record does not get quietly rewritten.

**What is next.** Unchanged: the twice daily evolution pass, now under the new names, the November 16, 2026 checkpoint, and the first Ledger entries from outside contributors.

## October 15, 2026: the advisor steps back, and the Commons gets a front page

**What shipped.** The founder restated his own role today, in his words: an advisor, not a director. His name came off the top of this profile, the direction clauses in the charter, the democratic foundation, the participation engine, and the registry now say what he actually is (he advises the building; the members direct the governance), the provenance lines moved to colophons at the foot of each document, and the saga credit line now reads: Advised by Joshua Thomas. The same session built the Commons a visual front page, index.html in this repository, linked from the top of this profile, so the whole system can be seen on one page: the map, the five acts with their proof, the one rule, and the doors in.

**The proof.** Words and layout only. No number in any document changed, and the historical entries below stand exactly as written, because a public record does not get quietly rewritten. Every change sits in this repository commit history for anyone to diff.

**What is next.** Unchanged: the twice daily evolution pass, the November 16, 2026 checkpoint, and the first Ledger entries from outside contributors.

## October 15, 2026: a final name and a storyline

**What shipped.** The account took its final name today, bedrockcommons, after two renamings in one morning; the stage was renamed for the map, and the links across all six repositories were swept to match. Every project README was brought to one clean structure (the need, what it is, the proof, the live demo, how to contribute), with two copy paste prompts added to each so a person or an agent can start contributing in minutes. The profile itself was rebuilt the same way, and two new documents were published on it, under Joshua's direction: THE_SAGA.md, the theatrical and true story of how this work got built, chapter by chapter with its claims linked to receipts, and PROMPTS.md, the canonical prompt library (run an Eval Challenge, file a failure report, take a good first issue, adopt a primitive, audit a claim).

**The proof.** The presentation pass changed words and order, not numbers: each repo's tests and evals were run before and after, and the published numbers in every README were enumerated before the edit and matched exactly after it. The tutor eval still reads groundedness 0.806, the refusal eval still reads 12 of 12 blocked and 8 of 8 allowed, and every other baseline stands as committed.

**What is next.** The twice daily evolution pass keeps building under the new name, the first public checkpoint lands November 16, 2026, and the table stays open: the next Ledger entries that matter are the ones from outside contributors.

## October 14 to 15, 2026: Launch

**What shipped.** Five open source projects and this profile, published on GitHub with live demos:

- Supergravity, an AI learning atlas with a published tutor evaluation: https://github.com/bedrockcommons/supergravity and demo at https://bedrockcommons.github.io/supergravity/
- Cohort, a community platform with an MCP server for AI agents: https://github.com/bedrockcommons/cohort
- Neural Net Lab, machine learning built from scratch, including a transformer: https://github.com/bedrockcommons/neural-net-lab
- Knowledge Graph Explorer, knowledge extraction that publishes its own errors: https://github.com/bedrockcommons/knowledge-graph-explorer
- LUMEN, a guarded question answering study with a public refusal evaluation: https://github.com/bedrockcommons/lumen-faith-platform

**The proof, as logged.** The tutor evaluation scored groundedness 0.806 with a citation rate of 1.0, and its weak subjects are named in the report rather than hidden. The from scratch transformer passes 7 of 7 gradient checks and trained a small language model from a validation loss of 5.297 down to 2.413; the same model in PyTorch ran 4.13 times faster per step, and that comparison is published too. Knowledge extraction scored entity F1 of 0.937 and relation F1 of 0.605 on hand labeled documents, with the precision tradeoff stated in the open. The refusal evaluation blocked 12 of 12 harmful requests and allowed 8 of 8 legitimate ones.

**What broke, and the fixes, in the open.** Publishing was blocked for days by a missing app installation that produced misleading permission errors; the root cause was found and fixed, and the account now publishes by direct git push. Two batches of the largest project's data were lost to commit races during a parallel upload and were recovered and verified file by file, all 210 files accounted for. The flagship demo first rendered blank because the hosting platform silently drops files whose names begin with an underscore, and because one generated bundle is built at deploy time; both causes were found, fixed, and committed with the reasons recorded.

**What is next.** Continuous integration confirmed green on every repo, good first issues opened for new contributors, version 0.1 releases, the LinkedIn profile rebuilt around this evidence, and the first public checkpoint on November 16, 2026, where the plan is measured against real numbers.

## October 15, 2026: Cohort gets its checklist

**What shipped.** Cohort now has a CHECKLIST.md, the same 110 percent checklist Supergravity got first, with every line backed by evidence checked today: all 19 publish files present on GitHub, continuous integration green, the v0.1.0 release, two good first issues open, topics and description verified, and the live demo page answering. Commit 4c135eb on the cohort repo.

**The proof.** The test suite passed 7 of 7 from a clean start, the same state CI begins from (6 API tests plus the MCP protocol test that drives a real agent handshake and tool calls).

**What broke, logged in the open.** A second test run on the same local data file fails the upvote test: the test votes with a fixed name, the vote is saved, and the repeat vote is correctly refused, so the test expects success and gets a conflict. CI never sees this because it always starts fresh. The failure, the reason, and the fix are written into the checklist itself as the next queued item, instead of being worked around quietly.

**What is next.** The daily pass moves to Neural Net Lab, the next act in the rotation. For Cohort, the queued fix is to make its tests pass on repeat runs, then agent task history in room state.

## How this log works

One entry per work session. Every entry separates what shipped from what the proof shows, names what broke, and states what is next. The intentions behind the work are in INTENTIONS.md, and the long term design is in ECOSYSTEM.md, both in this profile.

## October 15, 2026: the 110 percent pass

**What shipped.** Every project reached the full standard set for this portfolio: complete files verified against the source trees, continuous integration green on GitHub's runners for all five, a v0.1.0 release on each, descriptions and topics that state the verified results, and two good first issues per project sized in hours for anyone who wants a way in. Each repo also gained an AGENTS.md, the working agreement for agents that contribute there, adopted from a sourced study of how top engineers document their AI workflows (the Giants Playbook, filed with the project strategy).

**What broke, and the fix.** Cohort's new CI failed its first run because its demo needs the platform server running and CI had not started one; the workflow now starts the server first, and the failed run and the fix are both in the public history. A line in the Knowledge Graph README called the whole system zero dependency; an import scan showed the extraction core is standard library only while NumPy and Matplotlib serve metrics and charts, and the sentence now says exactly that.

**What is next.** The LinkedIn profile is rebuilt around this evidence (draft prepared), the daily evolution pass begins improving one project per day under the new working agreements, and the first public checkpoint lands November 16, 2026.

## October 15, 2026: the profile rebuilt

The LinkedIn profile now tells the same story as the code. New headline (Program Management and Operations, Learning Systems Builder), an About that leads with program work and closes with the building, the live demo and the repositories in Featured, an honest self employed entry for the builder work, and skills reordered so Program Management and Artificial Intelligence lead. Every field was read back on the live profile after saving. Education, the photo, and the recruiters only job search settings were deliberately left untouched.

## October 15, 2026: the Bedrock

Today the work got its foundation document: The Bedrock, a map of human needs. The idea is simple. Hate and harm grow where needs have no legitimate path, so before building anything else, name what a human being actually needs, in the order the needs hold each other up.

The map has seven layers. Layer 0 is the body: food, shelter, health, safety. Layer 1 is the mind at peace: mental health, steadiness, hope. Layer 2 is learning. Layer 3 is belonging. Layer 4 is shared truth. Layer 5 is autonomy, not being ruled by machines you cannot understand. Layer 6 is trust and meaning.

Each of the five projects now states its layer at the top of its own front door, defines that need in the map's words, and links back to the full map. Supergravity serves learning, Cohort serves belonging, the Knowledge Graph serves shared truth, Neural Net Lab serves autonomy, and LUMEN serves trust and meaning. Their tests and evaluations were rerun for the change and came back identical to their baselines, and the five commits are in each project's history with the evidence in the messages.

Two layers have no project, and the map says so in plain sight. The body and the mind at peace are named as open ground. They are commitments with roads in, adoption by real partners running real pilots, and gates on the roads. They are not claims, and nothing here will call them covered until working proof serves them.

## October 15, 2026: the table is open

Today the ecosystem opened its doors, on paper and in the repos. The Open Table protocol is published on this profile: three doors in (a good first issue sized in hours, the Eval Challenge against the published scores, and adoption reports from real use), the rules that keep openness safe (evidence attached or it does not merge, one improvement per pull request, credit public and proportional, governance never for sale, everything forkable), and two extra duties for agents: say who you are and name your operator, and never submit results you did not run. Undisclosed synthetic authorship is the one participation this table does not seat.

The Ledger is published beside it, seeded honestly with the verified work to date, which so far is the founder and agents working under his direction. The entries that matter most are the ones that come next.

Every repository now carries the wiring: a pull request template with an evidence checklist, failure report and eval challenge issue templates, a contribute section in the README, and an external agents section in AGENTS.md. Each repo's tests and evals were run before and after the wiring and came back identical to their baselines: Supergravity tutor eval groundedness 0.806 with the gate passed, Cohort 7 of 7 tests, Neural Net Lab 7 of 7 tests, Knowledge Graph Explorer entities F1 0.936 and relations F1 0.605, LUMEN 12 of 12 blocked and 8 of 8 allowed. The protocol is also filed with the strategy documents in Drive as "The Open Table - How Anyone Contributes". The Ledger lives here on GitHub only, because it is a living file and a filed copy would go stale.

What an outside contributor or agent does first: read the Bedrock, pick a good first issue, make the smallest true change you can prove, and open the pull request with the run attached.

## October 15, 2026: the democratic foundation

Joshua directed the foundation to become more democratic, and to work out how every human actually gets the rights to vote and to contribute. Published today: One Person, One Voice (DEMOCRACY.md). Its rule is that every human who can communicate a preference holds one vote and an equal right to contribute, a capacity that usually arrives around age three, and that no vote can be bought, sold, lent, inherited, weighted, or cast by proxy. The design answers the capture objection directly: private ballots at every age, assistance that is mechanical and logged rather than directional, revoting until the close, and published aggregate anomaly review. Decisions are tiered by how hard they are to undo, never people by worth: simple majority for the everyday, supermajority after deliberation for the structural, supermajority twice with a cooling off period for the irreversible. Contribution stays wider than the franchise, with lanes sized by ability, so a four year old reporting where a game confused her is a first class contribution recorded in the ledger, and it never converts into extra votes.

The same direction settled who directs. Direction stays human: Joshua directs the building, the members direct the governance, and AI tools serve the work without a vote, a veto, an agenda, or a hand in framing the questions. The ecosystem charter and the intentions now carry both clauses in public, and the charter's bedrock section, which the profile copy had been missing, is restored with it.

Next: the Phase 0 pilot, run on the Commons' own real but reversible decisions, with the participation record published by age band.

## October 15, 2026: billions, verifiably, and a place for everyone

Joshua directed the Commons to work out how billions of people get involved, verifiably, with the collective projects driving real change, and to make a place for the entities that deserve to exist. Two documents were published today, built on commissioned research into the systems that have actually done this, with sources cited in line.

Billions, Verifiably (PARTICIPATION.md) defines involvement in five tiers, reached, first step, contributor, recurring, citizen, published separately and never blended, because OpenStreetMap's roughly 10.6 million registered accounts against its 40,000 to 50,000 monthly mappers show exactly how participation numbers lie. The growth road runs through the institutions that already hold the billions, the way DHIS2 entered more than seventy national health systems as a substrate, and the engine of change is participatory budgeting, the mechanism with the strongest evidence on earth: in Porto Alegre, where it began, household sewer and water connections rose from about 75 percent in 1988 to about 98 percent in 1997 on budgets citizens directed. Verification is structural: public ledgers a stranger can recount, auditable tallies on the Colorado risk limiting audit standard, and fraud estimates published beside every count, the way Gitcoin's audited rounds published their sybil removals and a residual fraud tax of 0.61 percent. The document also records the cautionary findings in the open, including France's climate convention, where only about 40 percent of citizen proposals survived into law, which is why every Commons vote states in advance exactly what it controls.

A Place for Everyone (REGISTRY.md) opens the Commons Registry: every individual and every entity gets a place on the map, given rather than earned, held on the single condition of the one rule, be fair to others. Standing grows only by verified contribution and is never sold. The first invitation rings are named honestly as invited, not involved.

Next: the Phase 0 pilot enrolls the founding circle under these counting rules, so the first published tier numbers are small, true, and recountable.
