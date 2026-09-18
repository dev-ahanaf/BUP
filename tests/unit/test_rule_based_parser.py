"""Unit tests for deterministic rule-based directive parser."""
import pytest
from app.llm.rule_based import RuleBasedParser


def test_solar_reduction_parsing():
    # Reduced by percentage
    res = RuleBasedParser.parse_note(0, "Dust storm expected between 1 PM and 3 PM. Solar generation reduced by 30%.")
    assert res.applies is True
    assert res.directive_type == "solar_reduction"
    assert res.hours == [13, 14]
    assert abs(res.factor - 0.70) < 1e-4

    # Reduced to percentage
    res2 = RuleBasedParser.parse_note(0, "Cloud cover from noon until 2 PM. Solar output drops to 25%.")
    assert res2.applies is True
    assert res2.directive_type == "solar_reduction"
    assert res2.hours == [12, 13]
    assert abs(res2.factor - 0.25) < 1e-4

    # Panels offline
    res3 = RuleBasedParser.parse_note(0, "Inverter inspection from 10 AM until noon. Solar panels offline.")
    assert res3.applies is True
    assert res3.directive_type == "solar_reduction"
    assert res3.hours == [10, 11]
    assert res3.factor == 0.0


def test_battery_reserve_parsing():
    res = RuleBasedParser.parse_note(1, "Storm warning in evening. Maintain at least 50 kWh reserve between 6 PM and 10 PM.")
    assert res.applies is True
    assert res.directive_type == "minimum_battery_reserve"
    assert res.hours == [18, 19, 20, 21]
    assert res.minimum_energy_kwh == 50.0


def test_no_charge_window_parsing():
    res = RuleBasedParser.parse_note(0, "Grid stability alert. Do not charge battery from 18:00 to 21:00.")
    assert res.applies is True
    assert res.directive_type == "no_charge_window"
    assert res.hours == [18, 19, 20]


def test_no_discharge_window_parsing():
    res = RuleBasedParser.parse_note(0, "Battery system balancing from 2 AM until 5 AM. No discharging permitted.")
    assert res.applies is True
    assert res.directive_type == "no_discharge_window"
    assert res.hours == [2, 3, 4]


def test_max_grid_window_parsing():
    res = RuleBasedParser.parse_note(0, "Feeder maintenance from 13:00 to 16:00. Limit grid import to 60 kWh.")
    assert res.applies is True
    assert res.directive_type == "max_grid_window"
    assert res.hours == [13, 14, 15]
    assert res.max_grid_kwh == 60.0


def test_noop_informational_parsing():
    res1 = RuleBasedParser.parse_note(0, "Clear skies expected all day. Normal operation.")
    assert res1.applies is False
    assert res1.directive_type == "no_op"

    res2 = RuleBasedParser.parse_note(1, "Routine morning report: all microgrid systems operating nominally.")
    assert res2.applies is False
    assert res2.directive_type == "no_op"
