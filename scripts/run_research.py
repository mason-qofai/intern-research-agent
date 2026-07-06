#!/usr/bin/env python3
"""
v2 dossier agent, orchestrated through Claude Code.

Usage:
    python3 scripts/run_research.py "Palladium Equity Partners"
    python3 scripts/run_research.py "Palladium Equity Partners" --dry-run   # print the prompt, don't call claude

Sources are local files dropped directly into sources/ (PDFs, plus any
.md/.txt notes). Nothing is fetched live. This script reads the governing
contracts (prompts/), lists whatever is sitting in sources/, hands both to
`claude -p` with Read access so it can open each source file itself
(Claude Code's Read tool parses PDFs natively, no extraction library
needed here), and writes the raw result to dossiers/v2-claude-code.md.

This is a thin orchestration wrapper. All the actual research judgment
(source vetting, source-type labeling, confidence labeling, dossier
structure) lives in the contracts under prompts/, not in this script.
"""

import argparse
import pathlib
import subprocess
import sys

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
PROMPTS_DIR = REPO_ROOT / "prompts"
SOURCES_DIR = REPO_ROOT / "sources"
DOSSIERS_DIR = REPO_ROOT / "dossiers"
DEFAULT_OUT = DOSSIERS_DIR / "v2-claude-code.md"

CONTRACT_FILES = [
    "research-agent.md",
    "source-rubric.md",
    "confidence-rubric.md",
]

SOURCE_SUFFIXES = (".pdf", ".md", ".txt", ".html", ".htm")


def read_required(path):
    if not path.exists():
        sys.exit(f"missing required contract file: {path}")
    text = path.read_text().strip()
    if not text:
        sys.exit(f"contract file is empty: {path}")
    return text


def load_contracts():
    blocks = []
    for name in CONTRACT_FILES:
        text = read_required(PROMPTS_DIR / name)
        blocks.append(f"=== CONTRACT: {name} ===\n{text}")
    return "\n\n".join(blocks)


def list_source_files():
    files = sorted(
        p for p in SOURCES_DIR.iterdir()
        if p.is_file() and p.suffix.lower() in SOURCE_SUFFIXES
    )
    if not files:
        sys.exit(
            f"no source files found in {SOURCES_DIR} "
            f"(expected one of {SOURCE_SUFFIXES})"
        )
    return files


def build_prompt(firm_name, contracts, source_files):
    source_listing = "\n".join(f"- sources/{f.name}" for f in source_files)
    return f"""You are the research agent defined by the contracts below. Follow them exactly: the source-availability protocol, the public document / public inference labeling, and the high / medium / low confidence labeling.

{contracts}

=== TASK ===

Produce a dossier on {firm_name}.

All sources for this run are local files already sitting in the sources/ directory of the current working directory, listed below. There is nothing to fetch from the web. Use the Read tool to open every file listed. Read handles PDFs natively, including scanned or image-based pages, so open each one directly rather than trying to convert it first.

Apply research-agent.md's source-availability protocol to these local files instead of live URLs: if a file fails to open, is corrupted, or turns out to contain no meaningful readable content (for example a blank page, an error page someone saved by mistake, or a scan with no legible text), treat that file as unreachable under the existing 40% failure-rate rule, exactly as you would a dead link. Otherwise treat every file that opens with meaningful content as a valid source.

None of these files have a confirmed public URL attached (the filenames are the researcher's own labels, not URLs). When you cite a source, cite it by the document's own title or by its filename if it has no clear title, and say so plainly rather than inventing or guessing a URL. Do not fabricate a URL for any source.

Research from every source file that passes the check above, and compile the dossier in the structure research-agent.md specifies.

=== SOURCE FILES ===

{source_listing}

=== OUTPUT ===

You have no file-writing tool available in this session, and you should not try to use one or ask for permission to use one. Do not attempt to write, save, or create any file yourself, including dossiers/v2-claude-code.md. Instead, output the finished dossier as the literal text of your final response, in markdown. A separate script (not you) will take that response text and save it to dossiers/v2-claude-code.md.

Your entire final response must be ONLY the dossier markdown. No preamble, no meta-commentary about what you are about to do, no closing summary outside the document itself, and no requests for permission of any kind.

If the contracts call for you to flag something outside the dossier body (source files excluded or flagged for manual review, internally contradictory figures that need a human to adjudicate, sections you could not compile and why, or anything else the contracts say to raise with me rather than silently resolve), put all of that under a final markdown heading called "## Notes for human review" at the end of the document. Include that heading even if there is nothing to flag; in that case write one line under it saying so.
"""


def run_claude(prompt, model, max_budget_usd, timeout):
    cmd = [
        "claude", "-p", prompt,
        "--allowedTools", "Read",
        "--output-format", "text",
        "--max-budget-usd", str(max_budget_usd),
    ]
    if model:
        cmd += ["--model", model]
    try:
        result = subprocess.run(
            cmd, cwd=REPO_ROOT, capture_output=True, text=True, timeout=timeout
        )
    except subprocess.TimeoutExpired:
        sys.exit(f"claude timed out after {timeout}s")
    except FileNotFoundError:
        sys.exit("claude CLI not found on PATH, install Claude Code first")

    if result.returncode != 0:
        sys.exit(
            f"claude exited with status {result.returncode}\n"
            f"--- stderr ---\n{result.stderr}"
        )
    if not result.stdout.strip():
        sys.exit(f"claude produced no output\n--- stderr ---\n{result.stderr}")
    return result.stdout


def main():
    parser = argparse.ArgumentParser(description=__doc__.strip().splitlines()[1])
    parser.add_argument("firm_name", help='PE firm to research, e.g. "Palladium Equity Partners"')
    parser.add_argument("--model", default=None, help="override the claude model")
    parser.add_argument("--max-budget-usd", type=float, default=10.0,
                         help="spending cap passed through to claude -p (default: 10.0)")
    parser.add_argument("--timeout", type=int, default=2400,
                         help="subprocess timeout in seconds (default: 2400)")
    parser.add_argument("--out", default=None,
                         help=f"override output path (default: {DEFAULT_OUT.relative_to(REPO_ROOT)})")
    parser.add_argument("--dry-run", action="store_true",
                         help="print the assembled prompt and exit, do not call claude")
    args = parser.parse_args()

    contracts = load_contracts()
    source_files = list_source_files()
    prompt = build_prompt(args.firm_name, contracts, source_files)

    if args.dry_run:
        print(prompt)
        return

    print(f"[run_research] researching {args.firm_name!r} from {len(source_files)} local source(s) via `claude -p` ...", file=sys.stderr)
    output = run_claude(prompt, args.model, args.max_budget_usd, args.timeout)

    out_path = pathlib.Path(args.out) if args.out else DEFAULT_OUT
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(output.strip() + "\n")
    print(f"[run_research] wrote dossier to {out_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
