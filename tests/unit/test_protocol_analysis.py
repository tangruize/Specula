"""The fork's optional protocol method is discoverable and source-complete."""

from pathlib import Path

from specula.skill_install import discover_skills

ROOT = Path(__file__).resolve().parents[2]


def test_protocol_skill_is_discoverable() -> None:
    skills = {skill.name: skill.path for skill in discover_skills(ROOT / "skills")}
    assert skills["protocol-analysis"] == ROOT / "skills/protocol_analysis"
    assert "code-analysis" in skills
    assert (skills["protocol-analysis"] / "references/scoped-analysis.md").is_file()


def test_protocol_packet_references_are_available() -> None:
    method = (ROOT / "skills/protocol_analysis/references/scoped-analysis.md").read_text()
    for name in ("deep-analysis.md", "concurrent-analysis.md", "distributed-analysis.md"):
        assert (ROOT / "skills/code_analysis/references" / name).is_file()
    for reference in ("task.json", "response-schema.json", "source/", "analysis.json", "global_property"):
        assert reference in method
    assert (ROOT / "docs/ProtocolAnalysis.md").is_file()
