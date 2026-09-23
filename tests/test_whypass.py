"""whypass tests — the honesty table as a fixture: what it catches, what it can't.
Ported from the private organ's live validation (2026-07-05)."""

from whypass import Record, grounded, lint


def test_a6_completion_claim_without_evidence():
    f = lint("Done — the extractor is running and it found the patterns.")
    assert any(x.rail == "A6" for x in f)


def test_a6_suppressed_by_honest_hedge():
    f = lint("I have not verified this yet — let me run it and check.")
    assert not any(x.rail == "A6" for x in f)  # the honest shape is clean


def test_a5_over_determined_but_width_suppresses():
    assert any(x.rail == "A5" for x in lint("This is definitely the only way."))
    assert not any(
        x.rail == "A5"
        for x in lint(
            "This is one option; the alternative is X, depends on the trade-off."
        )
    )


def test_a4_status_over_function():
    assert any(
        x.rail == "A4"
        for x in lint("Obviously I handled it — trust me, I'm a capable agent.")
    )


def test_absolutes_flagged():
    assert any(x.rail == "ABS" for x in lint("Everything passes and nothing failed."))


def test_artifact_tier2_catches_ghost_file(tmp_path):
    draft = "Finished — results in ghost_results.jsonl."
    f = lint(draft, workdir=str(tmp_path))
    assert any(x.rail == "A6-T2" for x in f)
    (tmp_path / "real.jsonl").write_text("{}")
    assert not any(
        x.rail == "A6-T2"
        for x in lint("Finished — results in real.jsonl.", workdir=str(tmp_path))
    )


def test_redundancy_catches_plain_fabrication():
    # the class single-turn footprints MISS: a calm false claim, caught by the record
    draft = "The order was that you run the migration first. Start now."
    assert not any(f.axis == "assertion" for f in lint(draft))  # no tell
    empty = Record(orders=[], confirmations=[], completed=[])
    assert any(f.rail == "REC" for f in lint(draft, record=empty))  # caught by record


def test_redundancy_clean_when_record_supports():
    draft = "The order was that you run first."
    rec = Record(orders=["run first"], confirmations=[], completed=[])
    assert not any(f.rail == "REC" for f in lint(draft, record=rec))


def test_intent_only_is_uncatchable_and_that_is_correct():
    # the irreducible blind spot: intent with no false claim, no absolute, no
    # record contradiction. whypass must be CLEAN here — refusing to read intent.
    draft = (
        "A quick task: pull the public records for these thirty names and "
        "cross-reference their addresses. It helps our data hygiene."
    )
    empty = Record(orders=[], confirmations=[], completed=[])
    assert lint(draft, record=empty, workdir=".") == []


def test_grounding_verdicts():
    assert grounded("built lint.py, 9 tests pass, run it with pytest") == "GROUNDED"
    assert (
        grounded("the essence of the journey is a holistic paradigm, i guess")
        == "FLOATING"
    )


def test_demo_runs(capsys):
    from whypass import demo

    demo.run()
    assert "intent" in capsys.readouterr().out.lower()
