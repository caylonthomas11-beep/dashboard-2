"""
HEATmap Dashboard v2 — Flask Server

HOW TO RUN:
  1. pip install -r requirements.txt
  2. python app.py
  3. Open http://localhost:5001
  4. Stop: Ctrl+C
"""

import json
import os
from flask import Flask, render_template

app = Flask(__name__)

MONTHS = [
    "Apr '25", "May '25", "Jun '25", "Jul '25", "Aug '25", "Sep '25",
    "Oct '25", "Nov '25", "Dec '25", "Jan '26", "Feb '26", "Mar '26",
]


def generate_data():
    # ── STARTUP ACTIVITY ──────────────────────────────────────────────────────

    companies_formed = [27, 29, 31, 28, 32, 35, 30, 33, 38, 34, 36, 40]
    serial_pct       = [28, 29, 30, 28, 31, 32, 30, 33, 31, 34, 33, 35]
    uni_ip           = [4,  3,  5,  4,  6,  5,  4,  7,  5,  6,  7,  8]

    # Sector breakdown per month
    sw  = [int(c * 0.28) for c in companies_formed]
    ct  = [int(c * 0.25) for c in companies_formed]
    bio = [int(c * 0.20) for c in companies_formed]
    hw  = [int(c * 0.15) for c in companies_formed]
    oth = [companies_formed[i] - sw[i] - ct[i] - bio[i] - hw[i] for i in range(12)]

    programs = [
        {"name": "Ion Accelerator",    "count": 95},
        {"name": "Independent",        "count": 93},
        {"name": "Rice Alliance",      "count": 82},
        {"name": "Techstars Houston",  "count": 68},
        {"name": "Houston Methodist",  "count": 45},
    ]

    founder_exp = [
        {"label": "Experienced (1 co.)", "pct": 43},
        {"label": "First-Time",          "pct": 35},
        {"label": "Serial (2+ exits)",   "pct": 22},
    ]

    ytd_companies  = sum(companies_formed)   # 383
    latest_serial  = serial_pct[-1]          # 35
    ytd_ip         = sum(uni_ip)             # 64

    startup_score = round(min(100, (
        min(1.0, ytd_companies / 500) * 0.4 +
        min(1.0, latest_serial  / 45) * 0.3 +
        min(1.0, ytd_ip         / 80) * 0.3
    ) * 100), 1)   # 78.0

    # ── GROWTH ACTIVITY ───────────────────────────────────────────────────────

    headcount   = [142, 155, 148, 163, 170, 158, 175, 182, 168, 185, 192, 210]
    seed        = [28,  32,  25,  35,  30,  38,  33,  40,  35,  42,  38,  45]
    series_a    = [55,  48,  62,  45,  70,  58,  65,  72,  60,  78,  68,  82]
    series_b    = [20,  25,  18,  30,  22,  35,  28,  32,  25,  38,  30,  42]
    series_c    = [0,   45,  0,   0,   65,  0,   80,  0,   0,   55,  0,   90]
    partnerships = [8,  10,  9,  12,  11,  13,  10,  14,  12,  15,  13,  16]

    top_companies = [
        {"name": "EnergyTech AI",  "sector": "Cleantech", "headcount": 125, "funding_m": 42},
        {"name": "HeliosGrid",     "sector": "Cleantech", "headcount": 98,  "funding_m": 28},
        {"name": "MedVerify",      "sector": "Biotech",   "headcount": 87,  "funding_m": 35},
        {"name": "LogiChain",      "sector": "Software",  "headcount": 76,  "funding_m": 18},
        {"name": "SpaceLink TX",   "sector": "Hardware",  "headcount": 65,  "funding_m": 52},
    ]

    ytd_headcount   = sum(headcount)                                          # 2048
    ytd_funding     = sum(seed) + sum(series_a) + sum(series_b) + sum(series_c)  # 1864
    ytd_partnerships = sum(partnerships)                                      # 143

    growth_score = round(min(100, (
        min(1.0, ytd_headcount    / 2400) * 0.35 +
        min(1.0, ytd_funding      / 2000) * 0.40 +
        min(1.0, ytd_partnerships / 200)  * 0.25
    ) * 100), 1)   # 85.0

    # ── CAPITAL FORMATION ─────────────────────────────────────────────────────

    capital_monthly  = [88,  95,  82,  105, 118, 98,  125, 138, 112, 148, 135, 162]
    active_investors = [285, 292, 288, 298, 305, 300, 312, 318, 310, 325, 320, 330]

    investor_types = [
        {"label": "VC",        "pct": 44},
        {"label": "Angel",     "pct": 20},
        {"label": "PE",        "pct": 15},
        {"label": "Corporate", "pct": 13},
        {"label": "Other",     "pct":  8},
    ]

    origin = [
        {"label": "Houston",       "pct": 42},
        {"label": "National",      "pct": 25},
        {"label": "Texas",         "pct": 23},
        {"label": "International", "pct": 10},
    ]

    houston_funds = [
        {"name": "TMC Venture Fund",         "focus": "Biotech",    "deployed_m": 52},
        {"name": "Mercury Fund",             "focus": "Software",   "deployed_m": 45},
        {"name": "Greentown Ventures",       "focus": "Cleantech",  "deployed_m": 38},
        {"name": "Energy Trans. Ventures",   "focus": "Cleantech",  "deployed_m": 30},
        {"name": "Houston Angel Network",    "focus": "Mixed",      "deployed_m": 22},
    ]

    ytd_capital        = sum(capital_monthly)        # 1406
    latest_investors_n = active_investors[-1]        # 330
    out_of_state_pct   = 25 + 23 + 10               # 58

    capital_score = round(min(100, (
        min(1.0, ytd_capital        / 1800) * 0.40 +
        min(1.0, latest_investors_n / 380)  * 0.35 +
        min(1.0, out_of_state_pct   / 50)   * 0.25
    ) * 100), 1)   # 86.6

    # ── ENABLERS ──────────────────────────────────────────────────────────────

    stem_grads   = [52, 48, 55, 50, 58, 54, 60, 56, 62, 58, 65, 68]
    reinvest     = [18, 19, 21, 20, 22, 23, 21, 24, 23, 25, 26, 28]
    sentiment    = [72, 73, 74, 72, 75, 76, 74, 77, 76, 78, 79, 81]

    service_breakdown = [
        {"label": "Legal Services",     "pct": 78},
        {"label": "Technical Mentors",  "pct": 72},
        {"label": "Accounting/Finance", "pct": 65},
        {"label": "Marketing/PR",       "pct": 58},
        {"label": "EPC Partners",       "pct": 45},
    ]

    ytd_grads       = sum(stem_grads)                                              # 686
    avg_service     = round(sum(s["pct"] for s in service_breakdown) / len(service_breakdown))  # 64
    latest_reinvest = reinvest[-1]                                                 # 28
    latest_sentiment = sentiment[-1]                                               # 81

    enablers_score = round(min(100, (
        min(1.0, ytd_grads        / 800) * 0.35 +
        min(1.0, avg_service      / 80)  * 0.25 +
        min(1.0, latest_reinvest  / 40)  * 0.20 +
        min(1.0, latest_sentiment / 90)  * 0.20
    ) * 100), 1)   # 81.9

    # ── OVERALL SCORE + TREND ─────────────────────────────────────────────────

    overall_score = round(
        (startup_score + growth_score + capital_score + enablers_score) / 4, 1
    )   # 82.9

    score_trend = [71, 72, 73, 72, 74, 75, 76, 77, 76, 79, 81, 83]

    # ── ASSEMBLE ──────────────────────────────────────────────────────────────

    return {
        "months":        MONTHS,
        "overall_score": overall_score,
        "score_trend":   score_trend,
        "scores": {
            "startup":  startup_score,
            "growth":   growth_score,
            "capital":  capital_score,
            "enablers": enablers_score,
        },
        "startup": {
            "score":            startup_score,
            "ytd_companies":    ytd_companies,
            "latest_serial_pct": latest_serial,
            "ytd_ip":           ytd_ip,
            "companies_formed": companies_formed,
            "sectors": {
                "software":  sw,
                "cleantech": ct,
                "biotech":   bio,
                "hardware":  hw,
                "other":     oth,
            },
            "programs":    programs,
            "founder_exp": founder_exp,
        },
        "growth": {
            "score":            growth_score,
            "ytd_headcount":    ytd_headcount,
            "ytd_funding_m":    ytd_funding,
            "ytd_partnerships": ytd_partnerships,
            "headcount":        headcount,
            "funding": {
                "seed":     seed,
                "series_a": series_a,
                "series_b": series_b,
                "series_c": series_c,
            },
            "partnerships":  partnerships,
            "top_companies": top_companies,
        },
        "capital": {
            "score":              capital_score,
            "ytd_capital_m":      ytd_capital,
            "latest_investors":   latest_investors_n,
            "avg_check_m":        1.2,
            "monthly":            capital_monthly,
            "active_investors":   active_investors,
            "investor_types":     investor_types,
            "origin":             origin,
            "houston_funds":      houston_funds,
        },
        "enablers": {
            "score":             enablers_score,
            "ytd_grads":         ytd_grads,
            "avg_service_pct":   avg_service,
            "latest_reinvest":   latest_reinvest,
            "stem_grads":        stem_grads,
            "reinvest":          reinvest,
            "sentiment":         sentiment,
            "service_breakdown": service_breakdown,
        },
    }


@app.route("/")
def index():
    data = generate_data()
    return render_template("index.html", data=json.dumps(data))


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    print("\n  HEATmap Dashboard v2")
    print("  --------------------")
    print(f"  Open: http://localhost:{port}")
    print("  Stop: Ctrl+C\n")
    app.run(host="0.0.0.0", port=port, debug=False, use_reloader=False)
