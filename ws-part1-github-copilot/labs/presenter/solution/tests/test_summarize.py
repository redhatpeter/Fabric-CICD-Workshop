from pathlib import Path
import subprocess
import sys

import pytest

from summarize import load_rows, summarize, top_region


SCRIPT = Path(__file__).resolve().parents[1] / "summarize.py"
DATA = Path(__file__).resolve().parents[3] / "starter" / "data"
NORMAL_OUTPUT = (
    "East: 150.00\nNorth: 75.00\nWest: 250.00\nAverage per region: 158.33\n"
)


def run_report(path, *arguments):
    return subprocess.run(
        [sys.executable, str(SCRIPT), str(path), *arguments],
        capture_output=True,
        text=True,
        check=False,
    )


def test_normal_summary():
    rows = load_rows(str(DATA / "sales.csv"))
    assert len(rows) == 4
    totals, average = summarize(rows)
    assert totals == {"East": 150.0, "West": 250.0, "North": 75.0}
    assert average == pytest.approx(475 / 3)


@pytest.mark.parametrize(
    ("totals", "expected"),
    [
        ({"East": 150.0, "West": 250.0}, ("West", 250.0)),
        ({"West": 100.0, "East": 100.0}, ("East", 100.0)),
        ({}, None),
    ],
)
def test_top_region(totals, expected):
    assert top_region(totals) == expected


def test_default_cli():
    result = run_report(DATA / "sales.csv")
    assert result.returncode == 0
    assert result.stdout == NORMAL_OUTPUT
    assert result.stderr == ""


def test_region_filter():
    result = run_report(DATA / "sales.csv", "--region", "East")
    assert result.returncode == 0
    assert result.stdout == "East: 150.00\nAverage per region: 150.00\n"
    assert result.stderr == ""


def test_unknown_region():
    result = run_report(DATA / "sales.csv", "--region", "Unknown")
    assert result.returncode != 0
    assert result.stdout == ""
    assert "Unknown region" in result.stderr
    assert "Traceback" not in result.stderr


@pytest.mark.parametrize(
    ("fixture", "message"),
    [
        ("invalid-amount.csv", "Line 3: amount must be a number"),
        ("missing-column.csv", "region and amount columns"),
    ],
)
def test_invalid_fixture(fixture, message):
    result = run_report(DATA / fixture)
    assert result.returncode != 0
    assert result.stdout == ""
    assert message in result.stderr
    assert "Traceback" not in result.stderr


@pytest.mark.parametrize(
    ("content", "message"),
    [
        ("region,amount\nEast,-1\n", "nonnegative"),
        ("region,amount\nEast,nan\n", "finite"),
        ("region,amount\nEast,inf\n", "finite"),
        ("region,amount\nEast,1e999\n", "finite"),
        ("region,amount\n ,100\n", "blank"),
        ("region,amount\nEast\n", "malformed"),
        ("region,amount\nEast,100,extra\n", "malformed"),
        ('region,amount\n"East,100\n', "invalid CSV"),
    ],
)
def test_bad_row_reports_line(tmp_path, content, message):
    path = tmp_path / "bad.csv"
    path.write_text(content, encoding="utf-8")
    result = run_report(path)
    assert result.returncode != 0
    assert result.stdout == ""
    assert "Line 2" in result.stderr
    assert message in result.stderr
    assert "Traceback" not in result.stderr


def test_trim_regions_and_allow_zero(tmp_path):
    path = tmp_path / "trimmed.csv"
    path.write_text("region,amount\n East ,0\nEast,10\n", encoding="utf-8")
    totals, average = summarize(load_rows(str(path)))
    assert totals == {"East": 10.0}
    assert average == 10.0


def test_header_only_summary():
    assert summarize(load_rows(str(DATA / "empty.csv"))) == ({}, 0.0)


def test_header_only_cli():
    result = run_report(DATA / "empty.csv")
    assert result.returncode == 0
    assert result.stdout == "Average per region: 0.00\n"
    assert result.stderr == ""


def test_zero_byte_file_is_not_header_only(tmp_path):
    path = tmp_path / "no-header.csv"
    path.write_text("", encoding="utf-8")
    result = run_report(path)
    assert result.returncode != 0
    assert "region and amount columns" in result.stderr
    assert "Traceback" not in result.stderr


def test_malformed_header(tmp_path):
    path = tmp_path / "bad-header.csv"
    path.write_text('"region,amount\n', encoding="utf-8")
    result = run_report(path)
    assert result.returncode != 0
    assert result.stdout == ""
    assert "Line 1: invalid CSV" in result.stderr
    assert "Traceback" not in result.stderr


def test_missing_file(tmp_path):
    result = run_report(tmp_path / "does-not-exist.csv")
    assert result.returncode != 0
    assert result.stdout == ""
    assert "Error:" in result.stderr
    assert "Traceback" not in result.stderr


def test_invalid_encoding(tmp_path):
    path = tmp_path / "bad-encoding.csv"
    path.write_bytes(b"region,amount\n\xff,100\n")
    result = run_report(path)
    assert result.returncode != 0
    assert result.stdout == ""
    assert "Error:" in result.stderr
    assert "Traceback" not in result.stderr
