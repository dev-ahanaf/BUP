"""Integration tests running all 10 canonical public sample cases through the FastAPI endpoint."""
import json
import os
import pytest
from fastapi.testclient import TestClient

from pathlib import Path
from app.main import app

LOCAL_SAMPLE_PATH = Path(__file__).resolve().parent.parent.parent / "app" / "data" / "sample_cases.json"
EXTERNAL_SAMPLE_PATH = Path("/Users/fayekahanaf/Desktop/My Computer/CISNEXUS/BUP_CSE_FEST_2026_Participant_Docs/BUP_CSE_FEST_2026_Preli_Public_Sample_Cases.json")


@pytest.fixture
def client():
    return TestClient(app)


def load_sample_cases():
    target_path = LOCAL_SAMPLE_PATH if LOCAL_SAMPLE_PATH.exists() else EXTERNAL_SAMPLE_PATH
    if not target_path.exists():
        pytest.skip(f"Sample cases file not found at {target_path}")
    with open(target_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        return data.get("cases", data)


def test_all_10_sample_cases(client):
    cases = load_sample_cases()
    assert len(cases) == 10

    for idx, case in enumerate(cases):
        req_payload = case.get("input", case.get("request"))
        expected_resp = case.get("expected_output", case.get("expected_response"))

        response = client.post("/optimize-energy", json=req_payload)
        assert response.status_code == 200, f"Case {idx} failed with {response.status_code}: {response.text}"

        data = response.json()
        assert data["scenario_id"] == expected_resp["scenario_id"]

        # Check numerical totals with small rounding tolerance
        cost_diff = abs(data["total_cost_bdt"] - expected_resp["total_cost_bdt"])
        grid_diff = abs(data["total_grid_kwh"] - expected_resp["total_grid_kwh"])
        peak_diff = abs(data["peak_grid_kwh"] - expected_resp["peak_grid_kwh"])

        assert cost_diff <= 0.05, f"Case {idx} cost mismatch: got {data['total_cost_bdt']}, expected {expected_resp['total_cost_bdt']}"
        assert grid_diff <= 0.05, f"Case {idx} grid mismatch: got {data['total_grid_kwh']}, expected {expected_resp['total_grid_kwh']}"
        assert peak_diff <= 0.05, f"Case {idx} peak mismatch: got {data['peak_grid_kwh']}, expected {expected_resp['peak_grid_kwh']}"

        # Check directive interpretations count
        assert len(data["directive_interpretation"]) == len(expected_resp["directive_interpretation"])
        for d_idx, (actual_d, exp_d) in enumerate(zip(data["directive_interpretation"], expected_resp["directive_interpretation"])):
            assert actual_d["applies"] == exp_d["applies"], f"Case {idx} directive {d_idx} applies mismatch"
            assert actual_d["directive_type"] == exp_d["directive_type"], f"Case {idx} directive {d_idx} type mismatch"
            if exp_d["structured_adjustment"] is not None:
                assert actual_d["structured_adjustment"] is not None
                exp_adj = exp_d["structured_adjustment"]
                act_adj = actual_d["structured_adjustment"]
                if "hours" in exp_adj:
                    assert act_adj["hours"] == exp_adj["hours"]
                if "factor" in exp_adj:
                    assert abs(act_adj["factor"] - exp_adj["factor"]) <= 0.01
                if "minimum_energy_kwh" in exp_adj:
                    assert abs(act_adj["minimum_energy_kwh"] - exp_adj["minimum_energy_kwh"]) <= 0.01
                if "max_grid_kwh" in exp_adj:
                    assert abs(act_adj["max_grid_kwh"] - exp_adj["max_grid_kwh"]) <= 0.01

        # Check 24-hour plan length
        assert len(data["hourly_plan"]) == 24
