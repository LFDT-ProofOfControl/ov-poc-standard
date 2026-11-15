# Copyright 2026 Pamela Norton
# SPDX-License-Identifier: Apache-2.0
"""Verify synthetic compounding and drawdown; no authority evidence is supplied."""
from decimal import Decimal, localcontext
from fractions import Fraction
import json
from pathlib import Path


def decimal_series(start, returns):
    with localcontext() as context:
        context.prec = 50
        value, peak = Decimal(start), Decimal(start)
        series, drawdown = [], Decimal(0)
        for rate in returns:
            value *= 1 + Decimal(rate)
            peak = max(peak, value)
            drawdown = max(drawdown, 1 - value / peak)
            series.append(value)
        return series, drawdown


def rational_series(start, returns):
    values = [Fraction(start)]
    for rate in returns:
        values.append(values[-1] * (1 + Fraction(rate)))
    drawdown = max(1 - value / max(values[:i + 1])
                   for i, value in enumerate(values))
    return values[1:], drawdown


if __name__ == "__main__":
    fixture = json.loads(Path(__file__).with_name("scientific-calculator.json").read_text())
    inputs, expected = fixture["input"], fixture["expected"]
    decimal_nav, decimal_drawdown = decimal_series(inputs["opening_nav"], inputs["monthly_simple_returns"])
    rational_nav, rational_drawdown = rational_series(inputs["opening_nav"], inputs["monthly_simple_returns"])
    expected_nav = [Fraction(value) for value in expected["nav"]]
    if [Fraction(value) for value in decimal_nav] != rational_nav or rational_nav != expected_nav:
        raise SystemExit("FAIL: NAV differs from the published vector")
    if Fraction(decimal_drawdown) != rational_drawdown or rational_drawdown != Fraction(expected["max_drawdown_fraction"]):
        raise SystemExit("FAIL: drawdown differs from the published vector")
    print("PASS: synthetic NAV and drawdown agree in decimal and rational arithmetic")
