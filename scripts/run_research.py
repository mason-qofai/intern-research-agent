#!/usr/bin/env python3
"""
v3 dossier agent, decomposed into per-skill Claude Code invocations.

This is a thin orchestrator. No research judgment lives here. Each skill's
SKILL.md (under skills/<name>/SKILL.md) carries its own trigger condition,
input contract, output contract, and worked examples. This script's only
jobs are: call each skill in the right order via `claude -p`, parse the
hybrid output format (markdown body + trailing JSON claims block, per
skill), and pass structured data forward to the next skill.

This is v3: sequential, one call at a time. Module 8 refactors this into
a parallel orchestrator with subagent fan-out. Building sequential
composition first is the required predecessor to that refactor, not a
throwaway step.

Usage:
    python3 scripts/run_research.py "Palladium Equity Partners"
    python3 scripts/run_research.py "Palladium Equity Partners" --dry-run
"""

import argparse
import datetime
import hashlib
import json
import pathlib
import re
import subprocess
import sys

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO_ROOT / "skills"
SOURCES_DIR = REPO_ROOT / "sources"
RUNS_DIR = REPO_ROOT / "runs"
DOSSIERS_DIR = REPO_ROOT / "dossiers"
DEFAULT_OUT = DOSSIERS_DIR / "v3-skillified.md"

SOURCE_SUFFIXES = (".pdf", ".md", ".txt", ".html", ".htm")

# Skills that read sources/ (local files only, no web access).
SOURCE_BASED_SKILLS = {"firm-profiler", "portfolio-discoverer", "portco-profiler"}

# The one skill that uses live web search instead of sources/, per the
# source-tier rules in its own contract (SEC/EDGAR preferred, tier 2 only
# when tier 1 can't supply it, no paraphrasing from paywalled snippets).
WEB_SEARCH_SKILLS = {"private-data-approximator"}

# Skills whose entire output is JSON (batch claims list in, same list back
# out with one field filled in). No markdown body, no trailing claims block.
JSON_ONLY_SKILLS = {"confidence-scorer", "source-typer"}

# Skills whose output is pure markdown, the human-facing document itself.
# No trailing JSON claims block, nothing here for the orchestrator to parse
# out and forward, the whole returned text is the artifact.
PURE_MARKDOWN_SKILLS = {"dossier-assembler", "audit-pass"}


def read_skill_md(skill_name):
    path = SKILLS_DIR / skill_name / "SKILL.md"
    if not path.exists():
        sys.exit(
            f"missing SKILL.md for {skill_name}: {path}\n"
            f"(skills/ folders exist but are empty until you drop the "
            f"finished SKILL.md files in, per your own build process)"
        )
    text = path.read_text().strip()
    if not text:
        sys.exit(f"SKILL.md is empty: {path}")
    return text


def list_source_files():
    if not SOURCES_DIR.exists():
        return []
    return sorted(
        p for p in SOURCES_DIR.iterdir()
        if p.is_file() and p.suffix.lower() in SOURCE_SUFFIXES
    )


def extract_trailing_json_block(text):
    """
    Pulls the JSON content out of a '## Claims' fenced block at the end of
    a markdown + hybrid-format output. Returns (markdown_body, claims_list).
    If no '## Claims' heading is found, falls back to the last fenced
    ```json block in the text. Raises if neither is found, since every
    skill in SOURCE_BASED_SKILLS | WEB_SEARCH_SKILLS is contractually
    required to end in one.
    """
    claims_heading_match = re.search(r"##\s*Claims\s*\n", text)
    if claims_heading_match:
        after_heading = text[claims_heading_match.end():]
        fence_match = re.search(r"```json\s*(.*?)```", after_heading, re.DOTALL)
        if not fence_match:
            raise ValueError("found '## Claims' heading but no fenced json block after it")
        json_text = fence_match.group(1)
        markdown_body = text[:claims_heading_match.start()].strip()
    else:
        fence_matches = list(re.finditer(r"```json\s*(.*?)```", text, re.DOTALL))
        if not fence_matches:
            raise ValueError("no '## Claims' heading and no fenced json block found at all")
        last = fence_matches[-1]
        json_text = last.group(1)
        markdown_body = text[:last.start()].strip()

    try:
        claims = json.loads(json_text)
    except json.JSONDecodeError as e:
        raise ValueError(f"claims block did not parse as JSON: {e}\nraw:\n{json_text}")

    return markdown_body, claims


def parse_json_only(text):
    """For confidence-scorer / source-typer: whole output is a JSON array."""
    cleaned = re.sub(r"^```json\s*|\s*```$", "", text.strip())
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as e:
        raise ValueError(f"expected pure JSON array, got unparseable text: {e}\nraw:\n{text}")


def build_prompt(skill_name, skill_md, input_payload, extra_instructions=""):
    return f"""You are the {skill_name} skill. Follow the contract, trigger condition, and worked examples in your SKILL.md exactly.

=== SKILL.md: {skill_name} ===

{skill_md}

=== INPUT (matches this skill's input contract) ===

{json.dumps(input_payload, indent=2)}

{extra_instructions}

=== OUTPUT ===

Return your output in exactly the format your SKILL.md's "Output format (hybrid)" section specifies for this skill. No preamble, no meta-commentary, no requests for permission. Your entire response is the deliverable.
"""


def call_skill(skill_name, input_payload, model, max_budget_usd, timeout, run_dir, invocation_label=None):
    skill_md = read_skill_md(skill_name)

    extra = ""
    if skill_name in SOURCE_BASED_SKILLS:
        source_files = list_source_files()
        if not source_files:
            sys.exit(f"no source files found in {SOURCES_DIR}, required for {skill_name}")
        listing = "\n".join(f"- sources/{f.name}" for f in source_files)
        extra = (
            "All sources for this call are local files in sources/, listed below. "
            "Use the Read tool to open each one. Nothing is fetched from the web "
            "for this skill.\n\n=== SOURCE FILES ===\n\n" + listing
        )
        allowed_tools = "Read"
    elif skill_name in WEB_SEARCH_SKILLS:
        extra = (
            "This skill uses live web search, per the source-tier rules in its "
            "own SKILL.md (SEC/EDGAR preferred, tier 2 sources only when fully "
            "readable, never paraphrase from a paywalled snippet)."
        )
        allowed_tools = "Read,WebSearch,WebFetch"
    else:
        allowed_tools = "Read"

    prompt = build_prompt(skill_name, skill_md, input_payload, extra)

    cmd = [
        "claude", "-p", prompt,
        "--allowedTools", allowed_tools,
        "--output-format", "text",
        "--max-budget-usd", str(max_budget_usd),
    ]
    if model:
        cmd += ["--model", model]

    label = invocation_label or skill_name
    print(f"[run_research] calling {label} ...", file=sys.stderr)

    try:
        result = subprocess.run(
            cmd, cwd=REPO_ROOT, capture_output=True, text=True, timeout=timeout
        )
    except subprocess.TimeoutExpired:
        sys.exit(f"{label} timed out after {timeout}s")
    except FileNotFoundError:
        sys.exit("claude CLI not found on PATH, install Claude Code first")

    if result.returncode != 0:
        sys.exit(f"{label} exited with status {result.returncode}\n{result.stderr}")

    raw = result.stdout.strip()
    if not raw:
        sys.exit(f"{label} produced no output\n{result.stderr}")

    save_raw_output(run_dir, label, raw)
    return raw


def save_raw_output(run_dir, label, raw_text):
    run_dir.mkdir(parents=True, exist_ok=True)
    safe_label = re.sub(r"[^A-Za-z0-9._-]", "-", label)
    # Cap well under filesystem limits (macOS/most Linux: 255 bytes). A
    # malformed label (e.g. an entire flagged sentence used as a company
    # name) should never be able to crash the run over a filename length.
    if len(safe_label) > 100:
        digest = hashlib.sha256(safe_label.encode()).hexdigest()[:8]
        safe_label = safe_label[:90] + "-" + digest
    (run_dir / f"{safe_label}.md").write_text(raw_text)


def append_log(run_dir, message):
    run_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.datetime.now().isoformat(timespec="seconds")
    with open(run_dir / "run_log.txt", "a") as f:
        f.write(f"[{timestamp}] {message}\n")


def collect_claims(claim_sources):
    """
    claim_sources: list of raw claims lists already extracted from upstream
    skill outputs (firm-profiler, portfolio-discoverer, each portco-profiler
    call, each private-data-approximator call).

    Splits into:
      - ratable: claims with no flagged/withheld True, these go into the
        confidence-scorer and source-typer batch.
      - pre_flagged: claims already flagged (e.g. portfolio-discoverer's
        untraceable-hop candidates) or withheld (private-data-approximator's
        withheld estimates). These skip confidence-scorer and source-typer
        entirely, per contract, since there's nothing to rate, and go
        straight into the flagged-for-review pile dossier-assembler and
        audit-pass need to know about.
    """
    ratable = []
    pre_flagged = []
    for claims_list in claim_sources:
        for claim in claims_list:
            if claim.get("flagged") or claim.get("withheld"):
                pre_flagged.append(claim)
            else:
                ratable.append(claim)
    return ratable, pre_flagged


def merge_rated_claims(ratable_claims, confidence_results, source_type_results):
    """Merges confidence-scorer and source-typer's batch outputs back onto
    the original claim objects by claim_id, so nothing downstream has to
    re-join three separate lists itself."""
    conf_by_id = {c["claim_id"]: c for c in confidence_results}
    source_by_id = {c["claim_id"]: c for c in source_type_results}

    merged = []
    for claim in ratable_claims:
        cid = claim["claim_id"]
        conf = conf_by_id.get(cid, {})
        source = source_by_id.get(cid, {})
        merged_claim = {
            **claim,
            "confidence": conf.get("confidence"),
            "confidence_rationale": conf.get("rationale"),
            "confidence_flagged": conf.get("flagged", False),
            "source_type": source.get("source_type"),
            "source_evidence": source.get("evidence_url_or_note"),
            "source_flagged": source.get("flagged", False),
        }
        merged.append(merged_claim)
    return merged


def run_pipeline(firm_name, model, max_budget_usd, timeout, run_dir):
    append_log(run_dir, f"pipeline start for {firm_name!r}")

    # --- Stage 1: firm-profiler and portfolio-discoverer ---
    # These don't depend on each other. Called sequentially here; module 8
    # is where these two become genuinely concurrent.
    firm_raw = call_skill(
        "firm-profiler", {"firm_name": firm_name, "research_depth": "standard"},
        model, max_budget_usd, timeout, run_dir,
    )
    firm_md, firm_claims = extract_trailing_json_block(firm_raw)
    append_log(run_dir, f"firm-profiler complete, {len(firm_claims)} claims")

    portfolio_raw = call_skill(
        "portfolio-discoverer", {"firm_name": firm_name, "scope": "active_only"},
        model, max_budget_usd, timeout, run_dir,
    )
    portfolio_md, portfolio_claims = extract_trailing_json_block(portfolio_raw)
    append_log(run_dir, f"portfolio-discoverer complete, {len(portfolio_claims)} claims")

    # Company names now come directly from the required "company_name"
    # field on each claim, per the updated portfolio-discoverer contract.
    # No more parsing names out of the "text" field's prose, that was
    # tonight's actual root cause: a claim whose text was a long status
    # dispute got treated as a company name because nothing forced a
    # clean, separate field to read instead.
    #
    # The length check stays as a defensive fallback, not the primary
    # mechanism, in case a claim is missing company_name or an older/
    # non-conforming SKILL.md is still in place somewhere.
    MAX_NAME_LENGTH = 80

    def extract_company_name(claim):
        name = claim.get("company_name")
        if not name:
            raise ValueError(
                f"claim has no company_name field, contract violation: {claim!r}"
            )
        name = name.strip()
        if len(name) > MAX_NAME_LENGTH:
            raise ValueError(
                f"company_name is {len(name)} chars, too long to be a real "
                f"company name, likely a contract violation upstream: {name!r}"
            )
        return name

    company_names = []
    for c in portfolio_claims:
        if c.get("field") != "company_name" or c.get("flagged"):
            continue
        try:
            company_names.append(extract_company_name(c))
        except ValueError as e:
            append_log(run_dir, f"SKIPPED a portfolio-discoverer claim during name extraction: {e}")

    append_log(run_dir, f"extracted {len(company_names)} company names: {company_names}")

    # --- Stage 2: portco-profiler + private-data-approximator, per company ---
    # Sequential loop here. Module 8 fans this out into one subagent per
    # company running concurrently.
    #
    # Wrapped in try/except per company: if one company's output fails to
    # parse (e.g. the model ends its response on a self-check note instead
    # of the required Claims block), that company is logged as skipped and
    # the loop moves on, rather than the whole multi-hour run crashing and
    # losing every company already completed. Skipped companies are a real
    # gap to fix in portco-profiler's SKILL.md later, not something to
    # silently ignore, they're reported at the end.
    portco_mds = []
    portco_claims_lists = []
    financial_mds = []
    financial_claims_lists = []
    skipped_companies = []

    for company_name in company_names:
        try:
            portco_raw = call_skill(
                "portco-profiler", {"company_name": company_name, "parent_firm": firm_name},
                model, max_budget_usd, timeout, run_dir,
                invocation_label=f"portco-profiler-{company_name}",
            )
            portco_md, portco_claims = extract_trailing_json_block(portco_raw)

            financial_raw = call_skill(
                "private-data-approximator", {"portco_profile": {"company_name": company_name, "profile_markdown": portco_md}},
                model, max_budget_usd, timeout, run_dir,
                invocation_label=f"private-data-approximator-{company_name}",
            )
            financial_md, financial_claims = extract_trailing_json_block(financial_raw)
        except (Exception, SystemExit) as e:
            append_log(run_dir, f"SKIPPED {company_name}: {type(e).__name__}: {e}")
            skipped_companies.append(company_name)
            continue

        portco_mds.append((company_name, portco_md))
        portco_claims_lists.append(portco_claims)
        financial_mds.append((company_name, financial_md))
        financial_claims_lists.append(financial_claims)

        append_log(run_dir, f"profiled and estimated {company_name}")

    if skipped_companies:
        append_log(run_dir, f"SKIPPED {len(skipped_companies)} companies total: {skipped_companies}")

    # --- Stage 3: confidence-scorer + source-typer, batch, adjacent ---
    ratable_claims, pre_flagged_claims = collect_claims(
        [firm_claims, portfolio_claims] + portco_claims_lists + financial_claims_lists
    )
    append_log(run_dir, f"{len(ratable_claims)} claims to rate, {len(pre_flagged_claims)} pre-flagged")

    confidence_input = [
        {"claim_id": c["claim_id"], "claim_text": c["text"], "evidence": c.get("citation")}
        for c in ratable_claims
    ]
    confidence_raw = call_skill(
        "confidence-scorer", confidence_input, model, max_budget_usd, timeout, run_dir,
    )
    confidence_results = parse_json_only(confidence_raw)

    source_raw = call_skill(
        "source-typer", confidence_input, model, max_budget_usd, timeout, run_dir,
    )
    source_results = parse_json_only(source_raw)

    merged_claims = merge_rated_claims(ratable_claims, confidence_results, source_results)
    append_log(run_dir, "confidence-scorer and source-typer complete")

    # --- Stage 4: dossier-assembler ---
    assembler_input = {
        "firm_profile_markdown": firm_md,
        "portfolio_markdown": portfolio_md,
        "portco_profiles": [{"company": name, "markdown": md} for name, md in portco_mds],
        "financial_estimates": [{"company": name, "markdown": md} for name, md in financial_mds],
        "rated_claims": merged_claims,
        "pre_flagged_claims": pre_flagged_claims,
        "skipped_companies": skipped_companies,
    }
    dossier_raw = call_skill(
        "dossier-assembler", assembler_input, model, max_budget_usd, timeout, run_dir,
    )
    append_log(run_dir, "dossier-assembler complete, sections 1-6 plus section 7 placeholder")

    # --- Stage 5: audit-pass ---
    full_dossier_raw = call_skill(
        "audit-pass", {"dossier_markdown": dossier_raw}, model, max_budget_usd, timeout, run_dir,
    )
    append_log(run_dir, "audit-pass complete, final dossier assembled")

    return full_dossier_raw, skipped_companies


def main():
    parser = argparse.ArgumentParser(description=__doc__.strip().splitlines()[1])
    parser.add_argument("firm_name")
    parser.add_argument("--model", default=None)
    parser.add_argument("--max-budget-usd", type=float, default=2.0,
                         help="cap PER SKILL CALL (default: 2.0)")
    parser.add_argument("--timeout", type=int, default=600)
    parser.add_argument("--out", default=None)
    parser.add_argument("--dry-run", action="store_true",
                         help="print the planned call sequence and exit, do not call claude")
    args = parser.parse_args()

    run_id = datetime.datetime.now().strftime("%Y%m%dT%H%M%S")
    run_dir = RUNS_DIR / run_id

    if args.dry_run:
        print(f"Would research: {args.firm_name}")
        print(f"Run log would be written to: {run_dir}")
        print("Call sequence: firm-profiler, portfolio-discoverer, "
              "[portco-profiler + private-data-approximator per company], "
              "confidence-scorer, source-typer, dossier-assembler, audit-pass")
        return

    full_dossier, skipped_companies = run_pipeline(
        args.firm_name, args.model, args.max_budget_usd, args.timeout, run_dir
    )

    out_path = pathlib.Path(args.out) if args.out else DEFAULT_OUT
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(full_dossier.strip() + "\n")
    print(f"[run_research] wrote dossier to {out_path}", file=sys.stderr)
    print(f"[run_research] run log at {run_dir / 'run_log.txt'}", file=sys.stderr)
    if skipped_companies:
        print(f"[run_research] WARNING: {len(skipped_companies)} companies skipped "
              f"due to parse failures, dossier is incomplete: {skipped_companies}", file=sys.stderr)


if __name__ == "__main__":
    main()
