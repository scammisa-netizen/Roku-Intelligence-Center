"""
Roku Intelligence Center (RIC)
Run: streamlit run app.py
Data auto-saves to data.json in the same directory.
"""

import base64
import datetime
import json
import os
import uuid
from pathlib import Path

import altair as alt
import pandas as pd
import streamlit as st

DATA_FILE     = Path(__file__).parent / "data.json"
SF_CONFIG_FILE = Path(__file__).parent / "sf_config.json"
QUARTERS   = ["Q1", "Q2", "Q3", "Q4"]
CURRENT_FY = 2026


def _current_quarter() -> str:
    return f"Q{(datetime.date.today().month - 1) // 3 + 1}"

ROKU_PURPLE  = "#662D91"
ROKU_PURPLE2 = "#8B44B8"

# Activation types
ACT_LABELS  = ["DIO", "PMP / PG", "Sponsorship", "Channel Sales", "Ads Manager"]
ACT_KEYS    = ["act_dio", "act_pmpg", "act_sponsorship", "act_channel", "act_ads"]
ACT_COLORS  = [ROKU_PURPLE, ROKU_PURPLE2, "#f59e0b", "#10b981", "#3b82f6"]

MR_FIELDS = [
    ("ctv_investment",  "CTV Investment"),
    ("buying_approach", "Buying Approach"),
    ("targeting",       "Targeting"),
    ("creative",        "Creative"),
    ("measurement",     "Measurement"),
]

# ── CSS ───────────────────────────────────────────────────────────────────────

CSS = """
<style>
.stApp { background-color: #f5f6f8; }
header[data-testid="stHeader"] { background: transparent; }
footer { display: none; }
.block-container {
    padding-top: 1.5rem !important;
    padding-bottom: 2rem !important;
    max-width: 1300px !important;
}

/* Sidebar */
[data-testid="stSidebar"] { background:#fff; border-right:1px solid #e2e5ea; }
[data-testid="stSidebar"] .stButton > button {
    width:100%; text-align:left; background:transparent; border:none;
    border-radius:8px; padding:8px 12px; font-size:13.5px; font-weight:500; color:#374151;
}
[data-testid="stSidebar"] .stButton > button:hover { background:#f3eaf9; color:#662D91; }
.sidebar-active > button {
    background:#f3eaf9 !important; color:#662D91 !important;
    font-weight:700 !important; border-left:3px solid #662D91 !important;
}

/* Cards */
div[data-testid="stVerticalBlockBorderWrapper"] {
    border-radius:12px !important; border:1px solid #e2e5ea !important;
    box-shadow:0 1px 6px rgba(0,0,0,0.06) !important; background:#fff !important;
}
.hcard {
    background:#fff; border:1px solid #e2e5ea; border-radius:12px;
    box-shadow:0 1px 6px rgba(0,0,0,0.06); padding:20px 22px;
}

/* Strips */
.strip {
    background:#fff; border:1px solid #e2e5ea; border-radius:12px;
    box-shadow:0 1px 6px rgba(0,0,0,0.06); padding:18px 24px 16px; margin-bottom:4px;
}
.strip-eyebrow {
    font-size:10px; font-weight:700; letter-spacing:1.8px;
    text-transform:uppercase; color:#9ba3ae; margin-bottom:14px;
}
.kpi-row { display:flex; gap:32px; margin-bottom:14px; align-items:flex-end; flex-wrap:wrap; }
.kpi-num { font-size:28px; font-weight:800; color:#111827; line-height:1; font-variant-numeric:tabular-nums; }
.kpi-num-sm { font-size:22px; font-weight:800; line-height:1; font-variant-numeric:tabular-nums; }
.kpi-lbl { font-size:11px; color:#6b7280; font-weight:500; margin-top:4px; }
.kpi-sep { width:1px; height:38px; background:#e5e7eb; align-self:center; }
.progress-track { background:#edf0f4; border-radius:8px; height:10px; overflow:hidden; }
.progress-fill  { height:100%; border-radius:8px; }

/* Primary KPI banner */
.pkpi-banner {
    background: linear-gradient(135deg, #662D91 0%, #8B44B8 100%);
    border-radius:12px; padding:20px 28px; color:#fff; margin-bottom:4px;
    display:flex; align-items:center; gap:32px;
}
.pkpi-value { font-size:42px; font-weight:900; line-height:1; letter-spacing:-1px; }
.pkpi-label { font-size:12px; font-weight:600; letter-spacing:1.4px; text-transform:uppercase; opacity:.8; margin-bottom:4px; }
.pkpi-sub   { font-size:13px; opacity:.7; }

/* Alert tiles */
.alert-tile {
    border-radius:10px; padding:12px 16px;
}
.alert-risk   { background:#fef2f2; border:1px solid #fecaca; }
.alert-loaded { background:#fffbeb; border:1px solid #fde68a; }
.alert-lbl { font-size:10px; font-weight:700; letter-spacing:1.3px; text-transform:uppercase; margin-bottom:4px; }
.alert-risk   .alert-lbl { color:#dc2626; }
.alert-loaded .alert-lbl { color:#d97706; }
.alert-val { font-size:22px; font-weight:800; font-variant-numeric:tabular-nums; }
.alert-risk   .alert-val { color:#dc2626; }
.alert-loaded .alert-val { color:#d97706; }

/* Card typography */
.c-eyebrow { font-size:10px; font-weight:700; letter-spacing:1.8px; text-transform:uppercase; color:#9ba3ae; margin-bottom:2px; }
.c-heading  { font-size:17px; font-weight:700; color:#111827; margin-bottom:14px; }
.c-divider  { border:none; border-top:1px solid #f0f2f5; margin:12px 0; }

/* Title */
.os-title { font-size:26px; font-weight:800; color:#0f172a; line-height:1.15; margin-bottom:2px; }
.os-sub   { font-size:13px; color:#6b7280; margin-bottom:16px; }

/* Contacts */
.contact-row { display:flex; align-items:center; gap:14px; padding:10px 0; border-bottom:1px solid #f5f6f8; }
.contact-row:last-child { border-bottom:none; }
.avatar-circle {
    width:46px; height:46px; border-radius:50%; background:#662D91; color:#fff;
    font-size:15px; font-weight:700; display:flex; align-items:center; justify-content:center; flex-shrink:0;
}
.avatar-img   { width:46px; height:46px; border-radius:50%; object-fit:cover; flex-shrink:0; }
.contact-name  { font-size:14px; font-weight:600; color:#111827; }
.contact-title { font-size:12px; color:#6b7280; margin-top:2px; }

/* Bullets */
.bullet-section-head { font-size:10px; font-weight:700; letter-spacing:1.5px; text-transform:uppercase; color:#662D91; margin:12px 0 6px; }
.bullet-item { font-size:13.5px; color:#374151; padding:3px 0 3px 16px; position:relative; line-height:1.55; }
.bullet-item::before { content:"•"; position:absolute; left:4px; color:#c4c9d4; }

/* Checkbox strikethrough */
input[type="checkbox"]:checked ~ div > p,
input[type="checkbox"]:checked + div p { text-decoration:line-through !important; color:#9ba3ae !important; }

/* MediaRadar competitor card */
.mr-card {
    background:#fff; border:1px solid #e2e5ea; border-radius:12px;
    box-shadow:0 1px 6px rgba(0,0,0,0.06); overflow:hidden;
}
.mr-card-header {
    background:#662D91; padding:12px 16px;
    font-size:13px; font-weight:700; color:#fff; letter-spacing:.3px;
}
.mr-card-row { padding:10px 16px; border-bottom:1px solid #f5f6f8; }
.mr-card-row:last-child { border-bottom:none; }
.mr-row-lbl { font-size:9px; font-weight:700; letter-spacing:1.4px; text-transform:uppercase; color:#9ba3ae; margin-bottom:3px; }
.mr-row-val { font-size:13px; color:#374151; line-height:1.5; }
.mr-row-val-em { font-size:13px; font-weight:600; color:#111827; }

/* Placeholder */
.ph { font-size:13px; color:#b0b8c4; font-style:italic; padding:6px 0 2px; }

/* Salesforce live bar */
.sf-live-bar {
    background:#fff; border:1px solid #e2e5ea; border-radius:10px;
    padding:9px 16px; display:flex; align-items:center; gap:12px;
    margin-bottom:12px; flex-wrap:wrap;
}
.sf-badge-env  { background:#dcfce7; color:#16a34a; font-size:10px; font-weight:700;
                  letter-spacing:1px; text-transform:uppercase; padding:2px 10px;
                  border-radius:20px; white-space:nowrap; }
.sf-badge-cfg  { background:#f1f5f9; color:#64748b; font-size:10px; font-weight:700;
                  letter-spacing:1px; text-transform:uppercase; padding:2px 10px;
                  border-radius:20px; white-space:nowrap; }
.sf-bar-brand  { font-size:13px; font-weight:600; color:#374151; }
.sf-bar-sync   { font-size:11px; color:#9ba3ae; margin-left:auto; }

/* Input page */
.ip-title { font-size:22px; font-weight:700; color:#0f172a; margin-bottom:2px; }
.ip-sub   { font-size:13px; color:#6b7280; margin-bottom:16px; }

/* Reminder badge */
.reminder-badge {
    background:#fff7ed; border:1px solid #fed7aa; border-radius:10px;
    padding:10px 14px; display:flex; align-items:flex-start; gap:8px;
}
.reminder-icon  { font-size:16px; flex-shrink:0; margin-top:1px; }
.reminder-label { font-size:10px; font-weight:700; letter-spacing:1.3px;
                  text-transform:uppercase; color:#ea580c; margin-bottom:3px; }
.reminder-text  { font-size:13px; color:#374151; line-height:1.5; }
</style>
"""

# ── Persistence ───────────────────────────────────────────────────────────────

def load_data() -> dict:
    if DATA_FILE.exists():
        try:
            with open(DATA_FILE) as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            pass
    return {"accounts": [], "entries": {}}


def save_data(data: dict):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)


def load_sf_config() -> dict:
    defaults = {
        # SSO / OAuth fields (preferred)
        "client_id": "", "client_secret": "",
        # Legacy fields
        "username": "", "password": "", "security_token": "",
        # Shared
        "domain": "login",
    }
    if SF_CONFIG_FILE.exists():
        try:
            with open(SF_CONFIG_FILE) as f:
                return {**defaults, **json.load(f)}
        except (json.JSONDecodeError, OSError):
            pass
    return defaults


def save_sf_config(cfg: dict):
    with open(SF_CONFIG_FILE, "w") as f:
        json.dump(cfg, f, indent=2)


def _sf_env_configured() -> bool:
    """True when enough SF env vars are set to attempt a connection."""
    import salesforce_sync
    return salesforce_sync.env_vars_configured()


def _fetch_and_apply_sf_data(
    data: dict, acc: dict, acc_idx: int, brand_name: str, fy: int
):
    """
    Connect to Salesforce (env vars → sf_config.json fallback), call
    get_salesforce_data(), and write the results into data in-place.

    Returns None on success, or an error string on failure.
    """
    try:
        import salesforce_sync
    except ImportError:
        return "simple-salesforce is not installed. Run: pip install simple-salesforce"

    try:
        # Prefer env-var auth; fall back to saved config
        if salesforce_sync.env_vars_configured():
            sf = salesforce_sync.connect_from_env()
        else:
            cfg = load_sf_config()
            if cfg.get("client_id"):
                sf = salesforce_sync.connect_oauth(
                    cfg["client_id"], cfg["client_secret"],
                    cfg["username"], cfg["password"],
                    cfg.get("domain", "login"),
                )
            elif cfg.get("username") and cfg.get("security_token"):
                sf = salesforce_sync.connect(
                    cfg["username"], cfg["password"],
                    cfg["security_token"], cfg.get("domain", "login"),
                )
            else:
                return (
                    "Salesforce credentials not configured. "
                    "Set SF_CLIENT_ID / SF_CLIENT_SECRET / SF_USERNAME / SF_PASSWORD "
                    "as environment variables (SSO), or enter credentials in the "
                    "Salesforce tab under Data Input."
                )

        sf_data = salesforce_sync.get_salesforce_data(sf, brand_name, fy)

    except Exception as exc:
        return str(exc)

    # ── Write quarterly financials ────────────────────────────────────────────
    fy_str = str(fy)
    data.setdefault("entries", {}).setdefault(fy_str, {}).setdefault(acc["id"], {})

    for q, vals in sf_data["quarterly"].items():
        existing = data["entries"][fy_str][acc["id"]].get(q, {})
        existing["booked"] = vals["booked"]
        # Only overwrite goal when SF has pipeline data (non-zero)
        if vals["goal"] > 0:
            existing["goal"] = vals["goal"]
        data["entries"][fy_str][acc["id"]][q] = existing

    # ── Write account-level fields ────────────────────────────────────────────
    acc_record = data["accounts"][acc_idx]
    acc_record["sf_account_name"] = brand_name
    acc_record["sf_last_sync"]    = sf_data["fetched_at"]
    acc_record["revenue_at_risk"] = sf_data["revenue_at_risk"]

    # Active SF opps → stored list + short-term opportunities
    active = sf_data["active_opportunities"]
    acc_record["sf_opportunities"] = [
        {
            "id":         "",
            "name":       o["name"],
            "amount":     o["amount"],
            "close_date": o.get("close_date", ""),
            "stage":      o["stage"],
            "type":       "",
            "quarter":    "",
            "year":       None,
        }
        for o in active
    ]
    acc_record["short_term_opps"] = [
        {
            "text": _format_opp_text(o),
            "completed": False,
        }
        for o in active
    ]

    save_data(data)
    return None  # success


def _format_opp_text(opp: dict) -> str:
    parts = [opp["name"]]
    amt = opp.get("amount", 0)
    if amt:
        if amt >= 1_000_000:
            parts.append(f"${amt / 1_000_000:.1f}M")
        elif amt >= 1_000:
            parts.append(f"${amt / 1_000:.0f}K")
        else:
            parts.append(f"${amt:,.0f}")
    if opp.get("stage"):
        parts.append(opp["stage"])
    if opp.get("close_date"):
        parts.append(f"Close: {opp['close_date']}")
    return " · ".join(parts)


# ── Migration ─────────────────────────────────────────────────────────────────

def _empty_competitor():
    return {"name": "", "ctv_investment": "", "buying_approach": "",
            "targeting": [], "creative": [], "measurement": []}


def migrate_account(acc: dict) -> dict:
    # Opps: old plain-string → {text, completed}
    if "short_term_opps" not in acc:
        text = acc.pop("short_term_goals", "") or ""
        acc["short_term_opps"] = [{"text": l.strip(), "completed": False}
                                   for l in text.split("\n") if l.strip()]
    if "long_term_opps" not in acc:
        text = acc.pop("long_term_goals", "") or ""
        acc["long_term_opps"] = [{"text": l.strip(), "completed": False}
                                  for l in text.split("\n") if l.strip()]
    for field in ("short_term_opps", "long_term_opps"):
        items = acc.get(field, [])
        if items and isinstance(items[0], str):
            acc[field] = [{"text": t, "completed": False} for t in items]

    if isinstance(acc.get("challenges"), str):
        acc["challenges"] = [l.strip() for l in acc["challenges"].split("\n") if l.strip()]

    acc.setdefault("challenges",       [])
    acc.setdefault("contacts",         [])
    acc.setdefault("products_pitched", [])
    acc.setdefault("additional_notes", [])
    acc.setdefault("buy_type",         {"pmp": 0.0, "sponsorship": 0.0, "video": 0.0})

    # Vertical taxonomy
    acc.setdefault("vertical",     "")
    acc.setdefault("sub_vertical", "")

    # Time-sensitive reminder
    acc.setdefault("reminder", "")

    # Salesforce
    acc.setdefault("sf_account_name", "")
    acc.setdefault("sf_last_sync", "")
    acc.setdefault("sf_opportunities", [])

    # Primary / Secondary KPIs
    acc.setdefault("primary_kpi",    {"label": "", "value": ""})
    acc.setdefault("secondary_kpis", [])
    acc.setdefault("client_kpis",    [])   # legacy — kept for compat

    # Pacing extras (account-level)
    acc.setdefault("revenue_at_risk",      0.0)
    acc.setdefault("loaded_not_spending",  0.0)
    acc.setdefault("pacing_note",          "")

    # MediaRadar — always exactly 3 competitor slots
    acc.setdefault("mediaradar", {})
    mr = acc["mediaradar"]
    mr.setdefault("ctv_investment",  "")
    mr.setdefault("buying_approach", "")
    mr.setdefault("targeting",   [])
    mr.setdefault("creative",    [])
    mr.setdefault("measurement", [])
    comps = mr.get("competitors", [])
    while len(comps) < 3:
        comps.append(_empty_competitor())
    mr["competitors"] = comps[:3]

    return acc


# ── Helpers ───────────────────────────────────────────────────────────────────

def normalize_entry(e: dict):
    goal = float(e.get("goal") or 0)
    if "dio_sponsorship" in e or "dio_video" in e:
        booked = (float(e.get("dio_sponsorship") or 0)
                  + float(e.get("dio_video") or 0)
                  + float(e.get("pmp") or 0))
        spend = float(e.get("ran") or 0)
    else:
        booked = float(e.get("booked") or 0)
        spend  = float(e.get("spend") or e.get("ran") or 0)
    return goal, booked, spend


def get_entry(data, fy, account_id, quarter):
    return data.get("entries", {}).get(str(fy), {}).get(account_id, {}).get(quarter, {})


def get_annual_metrics(data, fy, acc):
    total_goal = total_booked = total_spend = 0.0
    quarterly = {}
    act_totals = {k: 0.0 for k in ACT_KEYS}
    for q in QUARTERS:
        e    = get_entry(data, fy, acc["id"], q)
        goal, booked, spend = normalize_entry(e)
        total_goal   += goal
        total_booked += booked
        total_spend  += spend
        act = {k: float(e.get(k) or 0) for k in ACT_KEYS}
        for k in ACT_KEYS:
            act_totals[k] += act[k]
        quarterly[q] = {"goal": goal, "booked": booked, "spend": spend, "activation": act}

    pct = round(total_booked / total_goal * 100, 1) if total_goal > 0 else 0.0
    return {
        "total_goal":           total_goal,
        "total_booked":         total_booked,
        "total_spend":          total_spend,
        "pct_to_goal":          pct,
        "quarterly":            quarterly,
        "act_totals":           act_totals,
        "revenue_at_risk":      float(acc.get("revenue_at_risk")     or 0),
        "loaded_not_spending":  float(acc.get("loaded_not_spending")  or 0),
        "pacing_note":          acc.get("pacing_note", ""),
    }


def fmt_usd(v) -> str:
    if v is None or (isinstance(v, float) and (pd.isna(v) or v == 0)):
        return "—"
    if abs(v) >= 1_000_000:
        return f"${v / 1_000_000:.2f}M"
    if abs(v) >= 1_000:
        return f"${v / 1_000:.0f}K"
    return f"${v:,.0f}"


def get_initials(name):
    parts = name.strip().split()
    if not parts:    return "?"
    if len(parts)==1: return parts[0][:2].upper()
    return (parts[0][0] + parts[-1][0]).upper()


# ── Summary Components ────────────────────────────────────────────────────────

def render_primary_kpi_banner(acc: dict):
    pk    = acc.get("primary_kpi", {})
    label = pk.get("label", "").strip()

    if not label:
        st.markdown("""
<div class="strip">
  <div class="strip-eyebrow">Primary KPI</div>
  <div class="ph" style="margin:0;">No Primary KPI set. Go to Data Input → KPIs tab.</div>
</div>""", unsafe_allow_html=True)
        return

    vert     = acc.get("vertical",     "").strip()
    sub_vert = acc.get("sub_vertical", "").strip()

    sep = '<div style="width:1px;height:52px;background:rgba(255,255,255,.25);align-self:center;"></div>'

    vert_block = f"""
  {sep}
  <div>
    <div class="pkpi-label">Vertical</div>
    <div style="font-size:16px;font-weight:700;">{vert or "—"}</div>
  </div>""" if True else ""   # always render slot; shows — if empty

    sub_block = f"""
  {sep}
  <div>
    <div class="pkpi-label">Sub-Vertical</div>
    <div style="font-size:16px;font-weight:700;">{sub_vert or "—"}</div>
  </div>""" if True else ""

    st.markdown(f"""
<div class="pkpi-banner">
  <div>
    <div class="pkpi-label">Client KPI</div>
    <div class="pkpi-value" style="font-size:28px;">{label}</div>
  </div>
  {sep}
  <div>
    <div class="pkpi-label">Account</div>
    <div style="font-size:20px;font-weight:700;">{acc.get("name","")}</div>
  </div>
  {vert_block}
  {sub_block}
</div>""", unsafe_allow_html=True)


def render_pacing_strip(metrics: dict, fy: int):
    cq      = _current_quarter()
    cq_data = metrics["quarterly"].get(cq, {"goal": 0, "booked": 0, "spend": 0, "activation": {}})
    pacing  = cq_data["booked"]
    goal    = cq_data["goal"]
    pct     = round(pacing / goal * 100, 1) if goal > 0 else 0.0
    fill    = min(max(pct, 0), 100)
    rar     = metrics["revenue_at_risk"]
    note    = metrics["pacing_note"]

    if pct >= 90:
        bar_bg = "background:linear-gradient(90deg,#059669 0%,#10b981 100%);"
        clr    = "#059669"
    elif pct >= 60:
        bar_bg = f"background:linear-gradient(90deg,{ROKU_PURPLE} 0%,{ROKU_PURPLE2} 100%);"
        clr    = ROKU_PURPLE
    else:
        bar_bg = "background:linear-gradient(90deg,#dc2626 0%,#f59e0b 100%);"
        clr    = "#dc2626"

    pct_str = f"{pct:.1f}%" if goal > 0 else "—"

    rar_html = f"""
<div class="alert-tile alert-risk">
  <div class="alert-lbl">Revenue at Risk</div>
  <div class="alert-val">{fmt_usd(rar)}</div>
</div>""" if rar else ""

    note_html = (f'<div style="font-size:12px;color:#6b7280;margin-top:10px;'
                 f'font-style:italic;">{note}</div>') if note else ""

    st.markdown(f"""
<div class="strip">
  <div class="strip-eyebrow">Pacing to Goal &nbsp;·&nbsp; {cq} FY{fy}</div>
  <div style="display:flex;gap:24px;align-items:flex-start;flex-wrap:wrap;">
    <div>
      <div class="kpi-row" style="margin-bottom:12px;">
        <div>
          <div class="kpi-num">{fmt_usd(pacing)}</div>
          <div class="kpi-lbl">{cq} Booked</div>
        </div>
        <div class="kpi-sep"></div>
        <div>
          <div class="kpi-num">{fmt_usd(goal)}</div>
          <div class="kpi-lbl">{cq} Goal</div>
        </div>
        <div class="kpi-sep"></div>
        <div>
          <div class="kpi-num" style="color:{clr};">{pct_str}</div>
          <div class="kpi-lbl">% to Goal</div>
        </div>
      </div>
      <div class="progress-track" style="width:420px;max-width:100%;">
        <div class="progress-fill" style="width:{fill}%;{bar_bg}"></div>
      </div>
      {note_html}
    </div>
    <div style="display:flex;gap:12px;flex-wrap:wrap;margin-top:4px;">
      {rar_html}
    </div>
  </div>
</div>""", unsafe_allow_html=True)


def render_performance_card(metrics: dict):
    """Performance overview: dollar metrics + activation stacked bar."""
    with st.container(border=True):
        st.markdown(
            '<div class="c-eyebrow">Client Direct Revenue</div>'
            '<div class="c-heading">Performance Overview</div>',
            unsafe_allow_html=True,
        )

        cols = st.columns(3)
        cols[0].metric("Total Booked", fmt_usd(metrics["total_booked"]))
        cols[1].metric("Annual Goal",  fmt_usd(metrics["total_goal"]))
        cols[2].metric("Total Spend",  fmt_usd(metrics["total_spend"]))

        st.markdown('<hr class="c-divider">', unsafe_allow_html=True)

        # Activation stacked bar chart
        q_data = metrics["quarterly"]
        rows = []
        for q in QUARTERS:
            act = q_data[q]["activation"]
            for key, label in zip(ACT_KEYS, ACT_LABELS):
                rows.append({"Quarter": q, "Type": label, "Amount": act[key]})

        act_df = pd.DataFrame(rows)
        has_act = act_df["Amount"].sum() > 0

        if has_act:
            chart = (
                alt.Chart(act_df)
                .mark_bar(cornerRadiusTopLeft=3, cornerRadiusTopRight=3)
                .encode(
                    x=alt.X("Quarter:N", axis=alt.Axis(labelAngle=0, title=None)),
                    y=alt.Y("Amount:Q", stack="zero",
                            axis=alt.Axis(format="$~s", title=None, gridColor="#f0f2f5")),
                    color=alt.Color(
                        "Type:N",
                        scale=alt.Scale(domain=ACT_LABELS, range=ACT_COLORS),
                        legend=alt.Legend(orient="bottom", title=None,
                                          labelFontSize=11, symbolSize=80,
                                          columns=5),
                    ),
                    order=alt.Order("Type:N", sort="ascending"),
                    tooltip=[
                        alt.Tooltip("Quarter:N", title="Quarter"),
                        alt.Tooltip("Type:N", title="Type"),
                        alt.Tooltip("Amount:Q", format="$,.0f", title="Amount"),
                    ],
                )
                .properties(
                    title=alt.TitleParams("Activation Type Breakdown by Quarter",
                                          fontSize=13, fontWeight="bold", color="#374151"),
                    height=220,
                )
                .configure_view(strokeWidth=0)
                .configure_axis(labelColor="#6b7280", labelFontSize=11)
            )
            st.altair_chart(chart, use_container_width=True)
        else:
            # Fallback: quarterly spend bar
            spend_df = pd.DataFrame([
                {"Quarter": q, "Spend": q_data[q]["spend"]} for q in QUARTERS
            ])
            bar = (
                alt.Chart(spend_df)
                .mark_bar(cornerRadiusTopLeft=4, cornerRadiusTopRight=4, color=ROKU_PURPLE)
                .encode(
                    x=alt.X("Quarter:N", axis=alt.Axis(labelAngle=0, title=None)),
                    y=alt.Y("Spend:Q",   axis=alt.Axis(format="$~s", title=None,
                                                       gridColor="#f0f2f5")),
                    tooltip=[alt.Tooltip("Quarter:N"), alt.Tooltip("Spend:Q", format="$,.0f")],
                )
                .properties(
                    title=alt.TitleParams("Quarterly Spend — enter Activation Breakdown for full chart",
                                          fontSize=12, fontWeight="normal", color="#9ba3ae"),
                    height=220,
                )
                .configure_view(strokeWidth=0)
                .configure_axis(labelColor="#6b7280", labelFontSize=11)
            )
            st.altair_chart(bar, use_container_width=True)


def _contact_html(c):
    name,  title    = c.get("name",""),    c.get("title","")
    email, linkedin = c.get("email",""),   c.get("linkedin","")
    b64,   mime     = c.get("photo",""),   c.get("photo_mime","image/jpeg")
    if b64:
        av = f'<img class="avatar-img" src="data:{mime};base64,{b64}" />'
    else:
        av = f'<div class="avatar-circle">{get_initials(name) if name else "?"}</div>'
    link_parts = []
    if email:
        link_parts.append(f'<a href="mailto:{email}" style="font-size:11px;color:{ROKU_PURPLE};text-decoration:none;">{email}</a>')
    if linkedin:
        link_parts.append(f'<a href="{linkedin}" target="_blank" style="font-size:11px;color:{ROKU_PURPLE};text-decoration:none;">LinkedIn ↗</a>')
    links_html = (f'<div style="margin-top:3px;">{" &nbsp;·&nbsp; ".join(link_parts)}</div>'
                  if link_parts else "")
    return (f'<div class="contact-row">{av}'
            f'<div><div class="contact-name">{name or "—"}</div>'
            f'<div class="contact-title">{title}</div>'
            f'{links_html}</div></div>')


def render_contacts_card(acc):
    contacts = acc.get("contacts", [])
    inner = "".join(_contact_html(c) for c in contacts) if contacts else \
            '<div class="ph">No contacts added.</div>'
    st.markdown(f"""
<div class="hcard">
  <div class="c-eyebrow">Contacts</div>
  <div class="c-heading">Primary Client Contacts</div>
  {inner}
</div>""", unsafe_allow_html=True)


def _bullets(items):
    if not items:
        return '<div class="ph">None added.</div>'
    return "".join(f'<div class="bullet-item">{i}</div>' for i in items)


def render_opportunities_card(data, acc, acc_idx):
    with st.container(border=True):
        st.markdown(
            '<div class="c-eyebrow">Strategic Alignment</div>'
            '<div class="c-heading">Opportunities</div>',
            unsafe_allow_html=True,
        )
        for section, key in [("Short-Term","short_term_opps"),("Long-Term","long_term_opps")]:
            st.markdown(f'<div class="bullet-section-head">{section}</div>', unsafe_allow_html=True)
            opps = acc.get(key, [])
            if opps:
                for i, opp in enumerate(opps):
                    text = opp["text"] if isinstance(opp, dict) else opp
                    done = opp.get("completed", False) if isinstance(opp, dict) else False
                    checked = st.checkbox(text, value=done, key=f"{key}_{acc['id']}_{i}")
                    if checked != done:
                        data["accounts"][acc_idx][key][i]["completed"] = checked
                        save_data(data)
                        st.rerun()
            else:
                st.markdown('<div class="ph">None added.</div>', unsafe_allow_html=True)


def render_challenges_card(acc):
    st.markdown(f"""
<div class="hcard">
  <div class="c-eyebrow">Risk &amp; Considerations</div>
  <div class="c-heading">Challenges</div>
  {_bullets(acc.get("challenges", []))}
</div>""", unsafe_allow_html=True)


def render_products_card(acc):
    rows = acc.get("products_pitched", [])
    if rows:
        inner = ""
        for r in rows:
            product  = r.get("product",  "") or "—"
            response = r.get("response", "") or "—"
            date     = r.get("date", "") or ""
            date_cell = (f'<div style="flex:0 0 88px;font-size:12px;color:#9ba3ae;">{date}</div>'
                         if date else '<div style="flex:0 0 88px;"></div>')
            inner += (f'<div style="display:flex;gap:12px;padding:6px 0;border-bottom:1px solid #f5f6f8;">'
                      f'{date_cell}'
                      f'<div style="flex:1;font-size:13.5px;font-weight:600;color:#111827;">{product}</div>'
                      f'<div style="flex:2;font-size:13.5px;color:#374151;">{response}</div>'
                      f'</div>')
        header = ('<div style="display:flex;gap:12px;padding:0 0 6px;border-bottom:2px solid #e2e5ea;margin-bottom:2px;">'
                  '<div style="flex:0 0 88px;font-size:10px;font-weight:700;letter-spacing:1.3px;text-transform:uppercase;color:#9ba3ae;">Date</div>'
                  '<div style="flex:1;font-size:10px;font-weight:700;letter-spacing:1.3px;text-transform:uppercase;color:#9ba3ae;">Product</div>'
                  '<div style="flex:2;font-size:10px;font-weight:700;letter-spacing:1.3px;text-transform:uppercase;color:#9ba3ae;">Client Response</div>'
                  '</div>')
    else:
        header, inner = "", '<div class="ph">No products added.</div>'

    st.markdown(f"""
<div class="hcard">
  <div class="c-eyebrow">Sales Activity</div>
  <div class="c-heading">Products Pitched &amp; Response</div>
  {header}{inner}
</div>""", unsafe_allow_html=True)


def render_additional_notes_card(acc):
    st.markdown(f"""
<div class="hcard">
  <div class="c-eyebrow">General</div>
  <div class="c-heading">Additional Notes</div>
  {_bullets(acc.get("additional_notes", []))}
</div>""", unsafe_allow_html=True)


# ── MediaRadar ────────────────────────────────────────────────────────────────

def _mr_lines_html(val) -> str:
    if not val:
        return '<span style="color:#b0b8c4;font-style:italic;font-size:12px;">—</span>'
    if isinstance(val, list):
        lines = [v for v in val if v]
        if not lines:
            return '<span style="color:#b0b8c4;font-style:italic;font-size:12px;">—</span>'
        return "".join(
            f'<div style="font-size:13px;color:#374151;padding:1px 0 1px 12px;position:relative;">'
            f'<span style="position:absolute;left:3px;color:#c4c9d4;">•</span>{l}</div>'
            for l in lines
        )
    return f'<span class="mr-row-val-em">{val}</span>'


def render_mediaradar_section(acc: dict):
    mr    = acc.get("mediaradar", {})
    comps = mr.get("competitors", [])
    active = [c for c in comps if c.get("name","").strip()]

    st.markdown(
        '<div class="c-eyebrow" style="margin-bottom:12px;">MediaRadar Intelligence &nbsp;·&nbsp; Top Competitors</div>',
        unsafe_allow_html=True,
    )

    if not active:
        st.markdown('<div class="ph">No competitors added. Go to Data Input → MediaRadar tab.</div>',
                    unsafe_allow_html=True)
        return

    cols = st.columns(len(active), gap="medium")
    for col, comp in zip(cols, active):
        name = comp.get("name", "Competitor")
        rows_html = ""
        for key, label in MR_FIELDS:
            val = comp.get(key, "")
            val_html = _mr_lines_html(val)
            rows_html += f"""
<div class="mr-card-row">
  <div class="mr-row-lbl">{label}</div>
  <div class="mr-row-val">{val_html}</div>
</div>"""
        with col:
            st.markdown(f"""
<div class="mr-card">
  <div class="mr-card-header">{name}</div>
  {rows_html}
</div>""", unsafe_allow_html=True)


# ── Salesforce Opportunities (Summary) ───────────────────────────────────────

def render_sf_opportunities_section(acc: dict):
    opps = acc.get("sf_opportunities", [])
    if not opps:
        return

    brand = acc.get("sf_account_name", acc.get("name", ""))
    last_sync = acc.get("sf_last_sync", "")
    sync_note = f" · Last fetched {last_sync[:10]}" if last_sync else ""

    total_val = sum(o.get("amount", 0) for o in opps)
    closed_count = sum(1 for o in opps if o.get("stage") == "Closed Won")
    open_count   = len(opps) - closed_count

    rows = []
    for o in opps:
        amt = o.get("amount", 0)
        rows.append({
            "Name":       o.get("name", ""),
            "Stage":      o.get("stage", ""),
            "Amount":     fmt_usd(amt) if amt else "—",
            "Close Date": o.get("close_date", ""),
            "Quarter":    f"{o.get('quarter','')} {o.get('year','')}" if o.get("quarter") else "",
        })

    df = pd.DataFrame(rows)

    st.markdown(
        f'<div class="c-eyebrow">Salesforce{sync_note}</div>'
        f'<div class="c-heading">Linked Opportunities · {brand}</div>',
        unsafe_allow_html=True,
    )

    kpi_html = (
        f'<div class="kpi-row">'
        f'<div><div class="kpi-num">{len(opps)}</div><div class="kpi-lbl">Total Opps</div></div>'
        f'<div class="kpi-sep"></div>'
        f'<div><div class="kpi-num">{closed_count}</div><div class="kpi-lbl">Closed Won</div></div>'
        f'<div class="kpi-sep"></div>'
        f'<div><div class="kpi-num">{open_count}</div><div class="kpi-lbl">Open / Active</div></div>'
        f'<div class="kpi-sep"></div>'
        f'<div><div class="kpi-num">{fmt_usd(total_val)}</div><div class="kpi-lbl">Total Value</div></div>'
        f'</div>'
    )
    st.markdown(kpi_html, unsafe_allow_html=True)
    st.dataframe(df, hide_index=True, use_container_width=True)


# ── Page 1: Summary ───────────────────────────────────────────────────────────

def render_summary_page(data: dict):
    if not data["accounts"]:
        st.info("No accounts found. Go to **Data Input** to create your first account.")
        return

    selected = st.session_state.get("selected_account", data["accounts"][0]["name"])
    acc_idx  = next((i for i, a in enumerate(data["accounts"]) if a["name"] == selected), 0)
    acc      = migrate_account(data["accounts"][acc_idx])
    data["accounts"][acc_idx] = acc

    fy_col, _, notif_col = st.columns([1, 3, 2])
    fy = fy_col.selectbox("FY", list(range(2023, 2030)),
                          index=list(range(2023, 2030)).index(CURRENT_FY),
                          label_visibility="collapsed", key="sum_fy")
    reminder = acc.get("reminder", "").strip()
    if reminder:
        notif_col.markdown(f"""
<div class="reminder-badge">
  <div class="reminder-icon">⏰</div>
  <div>
    <div class="reminder-label">Reminder</div>
    <div class="reminder-text">{reminder}</div>
  </div>
</div>""", unsafe_allow_html=True)

    metrics = get_annual_metrics(data, fy, acc)
    segment = acc.get("segment", "")

    sub_parts = ["Roku Intelligence Center"]
    if segment:
        sub_parts.append(segment)
    sub_parts.append(f"FY{fy}")
    st.markdown(
        f'<div class="os-title">{selected}</div>'
        f'<div class="os-sub">{" &nbsp;·&nbsp; ".join(sub_parts)}</div>',
        unsafe_allow_html=True,
    )

    # ── Salesforce live-fetch bar ─────────────────────────────────────────────
    sf_env = _sf_env_configured()
    last_sync  = acc.get("sf_last_sync", "")
    sync_label = f"Last synced {last_sync[:10]}" if last_sync else "Never synced"
    import salesforce_sync as _ssync_badge
    _sf_mode = _ssync_badge.auth_mode()
    if _sf_mode == "oauth":
        badge_html = '<span class="sf-badge-env">Live · SSO / OAuth</span>'
    elif _sf_mode == "legacy":
        badge_html = '<span class="sf-badge-env">Live · Username + Token</span>'
    else:
        badge_html = '<span class="sf-badge-cfg">Manual · Set SF env vars to enable auto-sync</span>'
    st.markdown(
        f'<div class="sf-live-bar">'
        f'{badge_html}'
        f'<span class="sf-bar-brand">Salesforce</span>'
        f'<span class="sf-bar-sync">{sync_label}</span>'
        f'</div>',
        unsafe_allow_html=True,
    )

    sf_col1, sf_col2 = st.columns([4, 1])
    brand_input = sf_col1.text_input(
        "brand_fetch",
        value=acc.get("sf_account_name", "") or acc.get("name", ""),
        placeholder="Enter Brand / Advertiser name (must match Salesforce Account Name)",
        label_visibility="collapsed",
        key=f"sf_brand_top_{acc['id']}",
    )
    fetch_clicked = sf_col2.button(
        "Fetch from Salesforce",
        key=f"sf_fetch_top_{acc['id']}",
        disabled=not (sf_env or load_sf_config().get("username")),
        use_container_width=True,
    )

    if fetch_clicked and brand_input.strip():
        with st.spinner(f'Fetching Salesforce data for "{brand_input.strip()}"...'):
            err = _fetch_and_apply_sf_data(data, acc, acc_idx, brand_input.strip(), fy)
        if err:
            st.error(f"Salesforce fetch failed: {err}")
        else:
            # Check for name suggestions (no data found)
            suggestions = st.session_state.get(f"sf_suggestions_{acc['id']}", [])
            if suggestions:
                st.warning(
                    f"No data found for **{brand_input.strip()}**. "
                    f"Did you mean one of these? {', '.join(f'`{s}`' for s in suggestions)}"
                )
            else:
                st.rerun()

    # Primary KPI Banner
    render_primary_kpi_banner(acc)
    st.write("")

    # Pacing strip
    render_pacing_strip(metrics, fy)
    st.write("")

    # Row 1: Performance card (full width)
    render_performance_card(metrics)
    st.write("")

    # Row 2: Opportunities (left) | Contacts + Products Pitched (right, stacked)
    opp_col, right_col = st.columns([1, 1], gap="medium")
    with opp_col:
        render_opportunities_card(data, acc, acc_idx)
    with right_col:
        render_contacts_card(acc)
        st.write("")
        render_products_card(acc)
    st.write("")

    # Row 3: Challenges + Additional Notes
    chal_col, notes_col = st.columns(2, gap="medium")
    with chal_col:
        render_challenges_card(acc)
    with notes_col:
        render_additional_notes_card(acc)
    st.write("")

    # Row 4: MediaRadar
    st.markdown('<hr style="border:none;border-top:1px solid #e2e5ea;margin:4px 0 16px;">',
                unsafe_allow_html=True)
    render_mediaradar_section(acc)

    # Row 5: Salesforce Opportunities (only if linked)
    if acc.get("sf_opportunities"):
        st.markdown('<hr style="border:none;border-top:1px solid #e2e5ea;margin:16px 0 16px;">',
                    unsafe_allow_html=True)
        with st.container(border=True):
            render_sf_opportunities_section(acc)


# ── Data Input Sections ───────────────────────────────────────────────────────

def _input_kpis(data, acc, acc_idx):
    # ── Account taxonomy ──────────────────────────────────────────────────────
    with st.form(f"tax_{acc['id']}"):
        tc1, tc2 = st.columns(2)
        vert_in    = tc1.text_input("Vertical",     value=acc.get("vertical",""),
                                     placeholder="e.g. Education")
        subvert_in = tc2.text_input("Sub-Vertical", value=acc.get("sub_vertical",""),
                                     placeholder="e.g. Online Learning")
        if st.form_submit_button("Save Vertical / Sub-Vertical"):
            data["accounts"][acc_idx]["vertical"]     = vert_in.strip()
            data["accounts"][acc_idx]["sub_vertical"] = subvert_in.strip()
            save_data(data)
            st.success("Saved.")

    st.markdown("---")
    with st.form(f"rem_{acc['id']}"):
        rem_val = st.text_input("⏰  Time-Sensitive Reminder",
                                value=acc.get("reminder",""),
                                placeholder="e.g. Tag delay on Takeover Pod — follow up by 4/15")
        if st.form_submit_button("Save Reminder"):
            data["accounts"][acc_idx]["reminder"] = rem_val.strip()
            save_data(data)
            st.success("Reminder saved.")

    st.markdown("---")
    st.markdown("**Primary KPI** — displayed prominently at the top of the Account Plan.")
    pk = acc.get("primary_kpi", {})

    with st.form(f"pk_{acc['id']}"):
        pk_label = st.text_input("KPI Label", value=pk.get("label",""),
                                  placeholder="e.g. Client Goal: Site Visits +40% YoY")
        if st.form_submit_button("Save Primary KPI"):
            data["accounts"][acc_idx]["primary_kpi"] = {
                "label": pk_label.strip(),
                "value": pk.get("value", ""),   # preserve existing value if stored
            }
            save_data(data)
            st.success("Primary KPI saved.")

    st.markdown("---")
    st.markdown("**Secondary KPIs** — stored for future use, not yet displayed on the summary page.")
    sec = list(acc.get("secondary_kpis", []))

    with st.expander("＋ Add Secondary KPI", expanded=not sec):
        with st.form(f"addsk_{acc['id']}", clear_on_submit=True):
            sc1, sc2 = st.columns(2)
            sl = sc1.text_input("Label *", placeholder="e.g. Brand Lift")
            sv = sc2.text_input("Value *", placeholder="e.g. +12 pts")
            if st.form_submit_button("Add") and sl.strip() and sv.strip():
                sec.append({"label": sl.strip(), "value": sv.strip()})
                data["accounts"][acc_idx]["secondary_kpis"] = sec
                save_data(data)
                st.rerun()

    for i, sk in enumerate(sec):
        with st.container(border=True):
            sc1, sc2, sc3 = st.columns([3, 2, 1])
            nl = sc1.text_input("Label", value=sk.get("label",""), key=f"skl_{acc['id']}_{i}")
            nv = sc2.text_input("Value", value=sk.get("value",""), key=f"skv_{acc['id']}_{i}")
            if sc3.button("Remove", key=f"skr_{acc['id']}_{i}", type="secondary"):
                sec.pop(i)
                data["accounts"][acc_idx]["secondary_kpis"] = sec
                save_data(data)
                st.rerun()
            if st.button("Save", key=f"sks_{acc['id']}_{i}"):
                sec[i] = {"label": nl, "value": nv}
                data["accounts"][acc_idx]["secondary_kpis"] = sec
                save_data(data)
                st.success("Saved.")


def _input_financial(data, acc, acc_idx, fy):
    acc_id = acc["id"]

    # ── Quarterly financial table ─────────────────────────────────────────────
    st.markdown("**Quarterly Financials** — goals, booked, and actuals.")
    rows = []
    for q in QUARTERS:
        e = get_entry(data, fy, acc_id, q)
        goal, booked, spend = normalize_entry(e)
        rows.append({
            "Quarter":    q,
            "Goal ($)":   goal,
            "Booked ($)": booked,
            "Spend ($)":  spend,
            "Notes":      e.get("notes", ""),
            "Rating":     int(e["rating"]) if e.get("rating") else None,
        })

    df     = pd.DataFrame(rows)
    edited = st.data_editor(
        df, key=f"fin_{acc_id}_{fy}", hide_index=True, use_container_width=True,
        column_config={
            "Quarter":    st.column_config.TextColumn(disabled=True, width="small"),
            "Goal ($)":   st.column_config.NumberColumn(format="$%d", min_value=0),
            "Booked ($)": st.column_config.NumberColumn(format="$%d", min_value=0),
            "Spend ($)":  st.column_config.NumberColumn(format="$%d", min_value=0),
            "Notes":      st.column_config.TextColumn(width="large"),
            "Rating":     st.column_config.SelectboxColumn(options=[1,2,3,4,5],
                                                            required=False, width="small"),
        },
    )

    tg = edited["Goal ($)"].sum()
    tb = edited["Booked ($)"].sum()
    ts = edited["Spend ($)"].sum()
    mc1, mc2, mc3 = st.columns(3)
    mc1.metric("Total Goal",   fmt_usd(tg))
    mc2.metric("Total Booked", fmt_usd(tb))
    mc3.metric("Total Spend",  fmt_usd(ts))

    fy_str = str(fy)
    data.setdefault("entries",{}).setdefault(fy_str,{}).setdefault(acc_id,{})
    for _, row in edited.iterrows():
        q = row["Quarter"]
        existing = data["entries"][fy_str][acc_id].get(q, {})
        existing.update({
            "goal":   float(row.get("Goal ($)")   or 0),
            "booked": float(row.get("Booked ($)") or 0),
            "spend":  float(row.get("Spend ($)")  or 0),
            "notes":  str(row.get("Notes")         or ""),
            "rating": int(row["Rating"]) if pd.notna(row.get("Rating")) else None,
        })
        data["entries"][fy_str][acc_id][q] = existing
    save_data(data)

    # ── Pacing extras ─────────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("**Pacing Insights** — displayed alongside the pacing bar on the summary page.")

    with st.form(f"pac_{acc['id']}_{fy}"):
        pc1, pc2 = st.columns(2)
        rar = pc1.number_input(
            "Revenue at Risk ($)",
            value=float(acc.get("revenue_at_risk") or 0),
            min_value=0.0, step=10_000.0, format="%.0f",
        )
        lns = pc2.number_input(
            "3P Loaded, Not Yet Spending ($)",
            value=float(acc.get("loaded_not_spending") or 0),
            min_value=0.0, step=10_000.0, format="%.0f",
        )
        note = st.text_input(
            "Pacing Note",
            value=acc.get("pacing_note", ""),
            placeholder="e.g. Q2 DIO campaign paused pending creative approval",
        )
        if st.form_submit_button("Save Pacing Insights"):
            data["accounts"][acc_idx]["revenue_at_risk"]     = rar
            data["accounts"][acc_idx]["loaded_not_spending"] = lns
            data["accounts"][acc_idx]["pacing_note"]         = note.strip()
            save_data(data)
            st.success("Pacing insights saved.")


def _input_activation(data, acc, acc_idx, fy):
    acc_id = acc["id"]
    st.markdown("**Activation Type Breakdown** — quarterly revenue by activation type.")
    st.caption("These values power the stacked bar chart on the summary page.")

    fy_str = str(fy)
    data.setdefault("entries",{}).setdefault(fy_str,{}).setdefault(acc_id,{})

    rows = []
    for q in QUARTERS:
        e = data["entries"][fy_str][acc_id].get(q, {})
        row = {"Quarter": q}
        for key, label in zip(ACT_KEYS, ACT_LABELS):
            row[label] = float(e.get(key) or 0)
        rows.append(row)

    df = pd.DataFrame(rows)
    col_cfg = {"Quarter": st.column_config.TextColumn(disabled=True, width="small")}
    for label in ACT_LABELS:
        col_cfg[label] = st.column_config.NumberColumn(format="$%d", min_value=0)

    edited = st.data_editor(
        df, key=f"act_{acc_id}_{fy}", hide_index=True,
        use_container_width=True, column_config=col_cfg,
    )

    # Totals row
    tcols = st.columns(len(ACT_LABELS) + 1)
    tcols[0].markdown("**Total**")
    for ci, label in enumerate(ACT_LABELS, 1):
        tcols[ci].metric(label, fmt_usd(edited[label].sum()))

    for _, row in edited.iterrows():
        q = row["Quarter"]
        existing = data["entries"][fy_str][acc_id].get(q, {})
        for key, label in zip(ACT_KEYS, ACT_LABELS):
            existing[key] = float(row.get(label) or 0)
        data["entries"][fy_str][acc_id][q] = existing
    save_data(data)


def _input_contacts(data, acc, acc_idx):
    st.markdown("**Client Contacts** — appear as profile cards on the summary page.")
    contacts = list(acc.get("contacts", []))

    with st.expander("＋ Add Contact", expanded=not contacts):
        with st.form(f"add_c_{acc['id']}", clear_on_submit=True):
            cc1, cc2 = st.columns(2)
            cname  = cc1.text_input("Name *")
            ctitle = cc2.text_input("Title")
            cc3, cc4 = st.columns(2)
            cemail    = cc3.text_input("Email", placeholder="name@company.com")
            clinkedin = cc4.text_input("LinkedIn URL", placeholder="https://linkedin.com/in/...")
            photo_file = st.file_uploader("Photo (optional)", type=["png","jpg","jpeg"],
                                          key=f"ph_new_{acc['id']}")
            if st.form_submit_button("Add Contact") and cname.strip():
                b64  = base64.b64encode(photo_file.read()).decode() if photo_file else ""
                mime = photo_file.type if photo_file else "image/jpeg"
                contacts.append({"id": str(uuid.uuid4())[:8], "name": cname.strip(),
                                  "title": ctitle.strip(), "email": cemail.strip(),
                                  "linkedin": clinkedin.strip(), "photo": b64, "photo_mime": mime})
                data["accounts"][acc_idx]["contacts"] = contacts
                save_data(data)
                st.rerun()

    if not contacts:
        st.caption("No contacts yet.")
        return

    for i, c in enumerate(contacts):
        with st.container(border=True):
            ec1, ec2, ec3 = st.columns([3, 3, 1])
            nn = ec1.text_input("Name",  value=c.get("name",""),  key=f"en_{acc['id']}_{i}")
            nt = ec2.text_input("Title", value=c.get("title",""), key=f"et_{acc['id']}_{i}")
            if ec3.button("Remove", key=f"rem_{acc['id']}_{i}", type="secondary"):
                contacts.pop(i)
                data["accounts"][acc_idx]["contacts"] = contacts
                save_data(data)
                st.rerun()
            el1, el2 = st.columns(2)
            ne = el1.text_input("Email",        value=c.get("email",""),    key=f"ee_{acc['id']}_{i}",
                                 placeholder="name@company.com")
            nl = el2.text_input("LinkedIn URL", value=c.get("linkedin",""), key=f"eli_{acc['id']}_{i}",
                                 placeholder="https://linkedin.com/in/...")
            new_photo = st.file_uploader("Replace photo", type=["png","jpg","jpeg"],
                                         key=f"rph_{acc['id']}_{i}")
            if st.button("Save Contact", key=f"sv_{acc['id']}_{i}"):
                contacts[i] = {**c, "name": nn, "title": nt, "email": ne.strip(), "linkedin": nl.strip()}
                if new_photo:
                    contacts[i]["photo"]      = base64.b64encode(new_photo.read()).decode()
                    contacts[i]["photo_mime"] = new_photo.type
                data["accounts"][acc_idx]["contacts"] = contacts
                save_data(data)
                st.success("Saved.")


def _input_opps(data, acc, acc_idx):
    def opps_to_text(field):
        return "\n".join(o["text"] if isinstance(o,dict) else o for o in acc.get(field,[]))

    def text_to_opps(raw, existing):
        m = {(o["text"] if isinstance(o,dict) else o): (o.get("completed",False) if isinstance(o,dict) else False)
             for o in existing}
        return [{"text": l.strip(), "completed": m.get(l.strip(), False)}
                for l in raw.split("\n") if l.strip()]

    st.markdown("**Opportunities & Challenges**")
    with st.form(f"txt_{acc['id']}"):
        tc1, tc2 = st.columns(2)
        st_opps = tc1.text_area("Short-Term Opportunities", value=opps_to_text("short_term_opps"),
                                 height=160, placeholder="One per line…")
        lt_opps = tc2.text_area("Long-Term Opportunities",  value=opps_to_text("long_term_opps"),
                                 height=160, placeholder="One per line…")
        challenges = st.text_area("Challenges", value="\n".join(acc.get("challenges",[])),
                                  height=110, placeholder="One per line…")
        if st.form_submit_button("Save Opportunities & Challenges"):
            data["accounts"][acc_idx]["short_term_opps"] = text_to_opps(st_opps, acc.get("short_term_opps",[]))
            data["accounts"][acc_idx]["long_term_opps"]  = text_to_opps(lt_opps, acc.get("long_term_opps",[]))
            data["accounts"][acc_idx]["challenges"]      = [l.strip() for l in challenges.split("\n") if l.strip()]
            save_data(data)
            st.success("Saved.")

    st.markdown("---")
    st.markdown("**Products Pitched & Response**")
    products = list(acc.get("products_pitched", []))

    with st.expander("＋ Add Product", expanded=not products):
        with st.form(f"addprod_{acc['id']}", clear_on_submit=True):
            pc1, pc2, pc3 = st.columns([2, 2, 1])
            new_p = pc1.text_input("Product *")
            new_r = pc2.text_input("Client Response")
            new_d = pc3.text_input("Date", placeholder="e.g. Mar 2026")
            if st.form_submit_button("Add") and new_p.strip():
                products.append({"product": new_p.strip(), "response": new_r.strip(), "date": new_d.strip()})
                data["accounts"][acc_idx]["products_pitched"] = products
                save_data(data)
                st.rerun()

    for i, p in enumerate(products):
        with st.container(border=True):
            pr1, pr2, pr3, pr4 = st.columns([2,2,1,1])
            ep = pr1.text_input("Product",  value=p.get("product",""),  key=f"pp_{acc['id']}_{i}")
            er = pr2.text_input("Response", value=p.get("response",""), key=f"pr_{acc['id']}_{i}")
            ed = pr3.text_input("Date",     value=p.get("date",""),     key=f"pd_{acc['id']}_{i}")
            if pr4.button("Remove", key=f"rmp_{acc['id']}_{i}", type="secondary"):
                products.pop(i)
                data["accounts"][acc_idx]["products_pitched"] = products
                save_data(data)
                st.rerun()
            if st.button("Save", key=f"svp_{acc['id']}_{i}"):
                products[i] = {"product": ep, "response": er, "date": ed}
                data["accounts"][acc_idx]["products_pitched"] = products
                save_data(data)
                st.success("Saved.")

    st.markdown("---")
    st.markdown("**Additional Notes**")
    with st.form(f"notes_{acc['id']}"):
        an = st.text_area("Notes", value="\n".join(acc.get("additional_notes",[])),
                          height=120, placeholder="One per line…", label_visibility="collapsed")
        if st.form_submit_button("Save Notes"):
            data["accounts"][acc_idx]["additional_notes"] = [l.strip() for l in an.split("\n") if l.strip()]
            save_data(data)
            st.success("Saved.")


def _input_mediaradar(data, acc, acc_idx):
    mr    = acc["mediaradar"]
    comps = mr["competitors"]   # always exactly 3 slots after migration

    for slot in range(3):
        comp  = comps[slot]
        label = comp.get("name","").strip() or f"Competitor {slot+1}"
        with st.expander(f"🏢 {label}", expanded=(slot == 0 and not comp.get("name",""))):
            with st.form(f"mr_{acc['id']}_{slot}"):
                cc1, cc2 = st.columns(2)
                cname = cc1.text_input("Competitor Name", value=comp.get("name",""),
                                       placeholder=f"Competitor {slot+1} name",
                                       key=f"mrn_{acc['id']}_{slot}")
                cctv  = cc2.text_input("CTV Investment",  value=comp.get("ctv_investment",""),
                                       placeholder="e.g. $6.1M ↑15% YoY",
                                       key=f"mrci_{acc['id']}_{slot}")
                cbuy  = st.text_input("Buying Approach",  value=comp.get("buying_approach",""),
                                      placeholder="e.g. Programmatic + Direct IO",
                                      key=f"mrba_{acc['id']}_{slot}")
                rc1, rc2, rc3 = st.columns(3)
                ctarg = rc1.text_area("Targeting",   value="\n".join(comp.get("targeting",[])),
                                      height=110, key=f"mrt_{acc['id']}_{slot}")
                ccreat= rc2.text_area("Creative",    value="\n".join(comp.get("creative",[])),
                                      height=110, key=f"mrc_{acc['id']}_{slot}")
                cmeas = rc3.text_area("Measurement", value="\n".join(comp.get("measurement",[])),
                                      height=110, key=f"mrm_{acc['id']}_{slot}")

                if st.form_submit_button(f"Save Competitor {slot+1}"):
                    comps[slot] = {
                        "name":           cname.strip(),
                        "ctv_investment":  cctv.strip(),
                        "buying_approach": cbuy.strip(),
                        "targeting":   [l.strip() for l in ctarg.split("\n")  if l.strip()],
                        "creative":    [l.strip() for l in ccreat.split("\n") if l.strip()],
                        "measurement": [l.strip() for l in cmeas.split("\n")  if l.strip()],
                    }
                    data["accounts"][acc_idx]["mediaradar"]["competitors"] = comps
                    save_data(data)
                    st.success("Saved.")


# ── Sidebar ───────────────────────────────────────────────────────────────────

def render_sidebar(data: dict):
    with st.sidebar:
        st.markdown(
            '<div style="font-size:12px;font-weight:800;color:#662D91;'
            'letter-spacing:.5px;margin-bottom:4px;">RIC</div>'
            '<div style="font-size:10px;font-weight:500;color:#9ba3ae;'
            'margin-bottom:16px;">Roku Intelligence Center</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div style="font-size:10px;font-weight:700;letter-spacing:1.8px;'
            'text-transform:uppercase;color:#9ba3ae;margin-bottom:8px;">Accounts</div>',
            unsafe_allow_html=True,
        )

        current = st.session_state.get("selected_account", "")
        if not current and data["accounts"]:
            current = data["accounts"][0]["name"]
            st.session_state["selected_account"] = current

        for acc in data["accounts"]:
            is_active = acc["name"] == current
            with st.container():
                if is_active:
                    st.markdown('<div class="sidebar-active">', unsafe_allow_html=True)
                if st.button(acc["name"], key=f"sb_{acc['id']}", use_container_width=True):
                    st.session_state["selected_account"] = acc["name"]
                    st.rerun()
                if is_active:
                    st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("---")
        st.caption("Add accounts in the **Data Input** tab.")


# ── Salesforce Sync ───────────────────────────────────────────────────────────

_ACT_LABEL_TO_KEY = {label: key for key, label in zip(ACT_KEYS, ACT_LABELS)}
_ACT_KEY_TO_LABEL = {key: label for key, label in zip(ACT_KEYS, ACT_LABELS)}


def _input_salesforce(data: dict, acc: dict, acc_idx: int, fy: int):
    try:
        import simple_salesforce  # noqa
    except ImportError:
        st.warning("**simple-salesforce** is not installed. Run: `pip install simple-salesforce`")
        return

    import salesforce_sync

    sf_env  = _sf_env_configured()
    sf_mode = salesforce_sync.auth_mode()

    # ── Auth status ───────────────────────────────────────────────────────────
    if sf_env:
        mode_label = "SSO · OAuth 2.0" if sf_mode == "oauth" else "Username / Password / Token"
        st.success(
            f"Salesforce credentials loaded from environment variables ({mode_label}). "
            "No manual credential entry required.",
            icon="✓",
        )
        if sf_mode == "oauth":
            st.caption(
                "Using: `SF_CLIENT_ID` · `SF_CLIENT_SECRET` · `SF_USERNAME` · `SF_PASSWORD`"
            )
        else:
            st.caption("Using: `SF_USERNAME` · `SF_PASSWORD` · `SF_SECURITY_TOKEN`")

        if st.button("Test Connection", key=f"sf_test_env_{acc['id']}"):
            with st.spinner("Testing connection..."):
                try:
                    sf_conn = salesforce_sync.connect_from_env()
                    ok, msg = salesforce_sync.test_connection(sf_conn)
                    if ok:
                        st.success(f"Connected: {msg}")
                    else:
                        st.error(f"Failed: {msg}")
                except Exception as exc:
                    st.error(f"Connection failed: {exc}")
    else:
        sf_cfg = load_sf_config()
        with st.expander(
            "Salesforce Credentials (fallback — prefer environment variables in production)",
            expanded=not (sf_cfg.get("client_id") or sf_cfg.get("username")),
        ):
            st.caption(
                "Environment variables are the recommended approach — credentials are never "
                "written to disk. The form below is a local fallback only."
            )

            cred_tab_sso, cred_tab_legacy = st.tabs(["SSO / OAuth 2.0", "Legacy (Security Token)"])

            with cred_tab_sso:
                st.caption(
                    "For Okta / SSO-federated Salesforce orgs. Requires a Connected App "
                    "with the `api` OAuth scope and password grant enabled.\n\n"
                    "Environment variables: `SF_CLIENT_ID`, `SF_CLIENT_SECRET`, "
                    "`SF_USERNAME`, `SF_PASSWORD`, `SF_DOMAIN` (optional)"
                )
                with st.form("sf_creds_sso"):
                    s1, s2 = st.columns(2)
                    sf_client_id     = s1.text_input("Consumer Key (Client ID)",
                                                      value=sf_cfg.get("client_id", ""))
                    sf_client_secret = s2.text_input("Consumer Secret (Client Secret)",
                                                      value=sf_cfg.get("client_secret", ""),
                                                      type="password")
                    s3, s4 = st.columns(2)
                    sf_sso_user   = s3.text_input("Username", value=sf_cfg.get("username", ""))
                    sf_sso_pass   = s4.text_input("Password", value=sf_cfg.get("password", ""),
                                                   type="password")
                    sf_sso_domain = st.text_input(
                        "My Domain (SF_DOMAIN)",
                        value=sf_cfg.get("domain", "login"),
                        help="Use 'login' for standard orgs, or your My Domain slug "
                             "(e.g. 'roku.my') for SSO orgs",
                    )
                    if st.form_submit_button("Save & Test SSO Connection"):
                        sf_cfg.update({
                            "client_id": sf_client_id.strip(),
                            "client_secret": sf_client_secret,
                            "username": sf_sso_user.strip(),
                            "password": sf_sso_pass,
                            "domain": sf_sso_domain.strip() or "login",
                        })
                        save_sf_config(sf_cfg)
                        with st.spinner("Testing SSO connection..."):
                            try:
                                sf_conn = salesforce_sync.connect_oauth(
                                    sf_client_id, sf_client_secret,
                                    sf_sso_user, sf_sso_pass,
                                    sf_sso_domain or "login",
                                )
                                ok, msg = salesforce_sync.test_connection(sf_conn)
                                if ok:
                                    st.success(f"Connected: {msg}")
                                else:
                                    st.error(f"Failed: {msg}")
                            except Exception as exc:
                                st.error(f"SSO connection failed: {exc}")

            with cred_tab_legacy:
                st.caption(
                    "For standard Salesforce orgs without SSO. Requires a security token "
                    "(reset via Salesforce → Settings → Reset Security Token).\n\n"
                    "Environment variables: `SF_USERNAME`, `SF_PASSWORD`, "
                    "`SF_SECURITY_TOKEN`, `SF_DOMAIN` (optional)"
                )
                with st.form("sf_creds_legacy"):
                    l1, l2 = st.columns(2)
                    sf_user   = l1.text_input("Username",       value=sf_cfg.get("username", ""))
                    sf_domain = l2.selectbox(
                        "Instance", ["login", "test"],
                        index=0 if sf_cfg.get("domain", "login") == "login" else 1,
                    )
                    sf_pass  = l1.text_input("Password",       value=sf_cfg.get("password", ""),
                                              type="password")
                    sf_token = l2.text_input("Security Token", value=sf_cfg.get("security_token", ""),
                                              type="password")
                    if st.form_submit_button("Save & Test Connection"):
                        sf_cfg.update({
                            "username": sf_user, "password": sf_pass,
                            "security_token": sf_token, "domain": sf_domain,
                        })
                        save_sf_config(sf_cfg)
                        with st.spinner("Testing connection..."):
                            try:
                                sf_conn = salesforce_sync.connect(
                                    sf_user, sf_pass, sf_token, sf_domain
                                )
                                ok, msg = salesforce_sync.test_connection(sf_conn)
                                if ok:
                                    st.success(f"Connected: {msg}")
                                else:
                                    st.error(f"Failed: {msg}")
                            except Exception as exc:
                                st.error(f"Connection failed: {exc}")

    st.markdown("---")

    # ── Brand / Advertiser fetch ──────────────────────────────────────────────
    st.markdown(f"**Fetch Salesforce Data — {acc['name']}**")
    st.caption(
        "Enter the exact Account Name as it appears in Salesforce. "
        "Fetches: quarterly booked, revenue at risk, active opportunities, and FY pipeline."
    )

    with st.form(f"sf_brand_{acc['id']}"):
        brand_name = st.text_input(
            "Salesforce Brand / Advertiser Name",
            value=acc.get("sf_account_name", "") or acc.get("name", ""),
            placeholder="e.g. Nike, Inc.",
            help="Must match the exact Account Name in Salesforce",
        )
        fetch_fy = st.selectbox(
            "Fiscal Year",
            list(range(2023, 2030)),
            index=list(range(2023, 2030)).index(fy),
            key=f"sf_fetch_fy_{acc['id']}",
        )
        fetch_submitted = st.form_submit_button("Fetch from Salesforce", type="primary")

    last_sync = acc.get("sf_last_sync", "")
    if last_sync:
        st.caption(f"Last synced: {last_sync}")

    if fetch_submitted:
        if not brand_name.strip():
            st.warning("Enter the Salesforce Brand / Advertiser Name.")
        else:
            with st.spinner(f'Fetching data for "{brand_name.strip()}"...'):
                err = _fetch_and_apply_sf_data(
                    data, acc, acc_idx, brand_name.strip(), fetch_fy
                )
            if err:
                st.error(f"Fetch failed: {err}")
            else:
                # Surface name suggestions if no data was found
                acc_after = data["accounts"][acc_idx]
                active_count = len(acc_after.get("sf_opportunities", []))
                fy_booked = sum(
                    data.get("entries", {}).get(str(fetch_fy), {})
                    .get(acc["id"], {}).get(q, {}).get("booked", 0)
                    for q in QUARTERS
                )
                if active_count == 0 and fy_booked == 0:
                    # Try to suggest correct names via a LIKE query
                    try:
                        import salesforce_sync as _ssync
                        _cfg = load_sf_config()
                        if _ssync.env_vars_configured():
                            _sf = _ssync.connect_from_env()
                        elif _cfg.get("client_id"):
                            _sf = _ssync.connect_oauth(
                                _cfg["client_id"], _cfg["client_secret"],
                                _cfg["username"], _cfg["password"],
                                _cfg.get("domain", "login"),
                            )
                        else:
                            _sf = _ssync.connect(
                                _cfg["username"], _cfg["password"],
                                _cfg["security_token"], _cfg.get("domain", "login"),
                            )
                        suggestions = _ssync._suggest_account_names(_sf, brand_name.strip())
                        if suggestions:
                            st.warning(
                                f"No data found for **{brand_name.strip()}**. "
                                f"Did you mean: {', '.join(f'`{s}`' for s in suggestions)}?"
                            )
                        else:
                            st.info(f"No opportunities found for **{brand_name.strip()}** in FY{fetch_fy}.")
                    except Exception:
                        st.info(f"No data found for **{brand_name.strip()}** in FY{fetch_fy}.")
                else:
                    st.success(
                        f"Synced: {active_count} active opp(s) · "
                        f"FY{fetch_fy} booked: {fmt_usd(fy_booked)}"
                    )
                    st.rerun()

    # ── Linked opportunities table ────────────────────────────────────────────
    opps = acc.get("sf_opportunities", [])
    if opps:
        st.markdown("---")
        closed_count = sum(1 for o in opps if o.get("stage") == "Closed Won")
        open_count   = len(opps) - closed_count
        total_val    = sum(o.get("amount", 0) for o in opps)

        kc1, kc2, kc3, kc4 = st.columns(4)
        kc1.metric("Total Opportunities", len(opps))
        kc2.metric("Active / Open", open_count)
        kc3.metric("Closed Won", closed_count)
        kc4.metric("Total Value", fmt_usd(total_val))

        rows = [
            {
                "Name":       o.get("name", ""),
                "Stage":      o.get("stage", ""),
                "Amount":     fmt_usd(o.get("amount", 0)) if o.get("amount") else "—",
                "Close Date": o.get("close_date", ""),
            }
            for o in opps
        ]
        st.dataframe(pd.DataFrame(rows), hide_index=True, use_container_width=True)


# ── Page 2: Data Input ────────────────────────────────────────────────────────

def render_input_page(data: dict):
    st.markdown('<div class="ip-title">Data Input</div>', unsafe_allow_html=True)
    st.markdown('<div class="ip-sub">Manage accounts and enter all dashboard content here.</div>',
                unsafe_allow_html=True)

    with st.expander("＋ Add New Account", expanded=not data["accounts"]):
        with st.form("add_account", clear_on_submit=True):
            nc1, nc2 = st.columns(2)
            name     = nc1.text_input("Account Name *")
            segment  = nc2.text_input("Segment")
            nc3, nc4 = st.columns(2)
            vertical    = nc3.text_input("Vertical", placeholder="e.g. Education")
            sub_vertical = nc4.text_input("Sub-Vertical", placeholder="e.g. Online Learning")
            if st.form_submit_button("Add Account") and name.strip():
                data["accounts"].append({
                    "id": str(uuid.uuid4())[:8],
                    "name": name.strip(), "segment": segment.strip(),
                    "vertical": vertical.strip(), "sub_vertical": sub_vertical.strip(),
                    "contacts": [], "short_term_opps": [], "long_term_opps": [],
                    "challenges": [], "products_pitched": [], "additional_notes": [],
                    "buy_type": {"pmp":0.0,"sponsorship":0.0,"video":0.0},
                    "primary_kpi": {"label":"","value":""}, "secondary_kpis": [], "client_kpis": [],
                    "revenue_at_risk": 0.0, "loaded_not_spending": 0.0, "pacing_note": "",
                    "mediaradar": {
                        "ctv_investment":"","buying_approach":"",
                        "targeting":[],"creative":[],"measurement":[],
                        "competitors": [_empty_competitor(), _empty_competitor(), _empty_competitor()],
                    },
                })
                save_data(data)
                st.rerun()

    if not data["accounts"]:
        return

    ac1, ac2, ac3 = st.columns([3, 1, 1])
    account_names = [a["name"] for a in data["accounts"]]
    selected = ac1.selectbox("Account", account_names, key="inp_acct")
    fy       = ac2.selectbox("FY", list(range(2023, 2030)),
                              index=list(range(2023,2030)).index(CURRENT_FY), key="inp_fy")

    acc_idx = next(i for i, a in enumerate(data["accounts"]) if a["name"] == selected)
    acc     = migrate_account(data["accounts"][acc_idx])
    data["accounts"][acc_idx] = acc

    if ac3.button("Delete Account", type="secondary", use_container_width=True):
        if st.session_state.get("_confirm_del") == acc["id"]:
            data["accounts"].pop(acc_idx)
            save_data(data)
            st.session_state.pop("_confirm_del", None)
            st.rerun()
        else:
            st.session_state["_confirm_del"] = acc["id"]
    if st.session_state.get("_confirm_del") == acc["id"]:
        st.warning(f"Click **Delete Account** again to permanently remove **{selected}**.")

    st.divider()

    t_kpi, t_fin, t_act, t_contacts, t_opps, t_mr, t_sf = st.tabs([
        "🎯  KPIs",
        "📊  Financials",
        "📈  Activation Breakdown",
        "👤  Contacts",
        "📝  Opportunities",
        "📡  MediaRadar",
        "🔗  Salesforce",
    ])

    with t_kpi:      _input_kpis(data, acc, acc_idx)
    with t_fin:      _input_financial(data, acc, acc_idx, fy)
    with t_act:      _input_activation(data, acc, acc_idx, fy)
    with t_contacts: _input_contacts(data, acc, acc_idx)
    with t_opps:     _input_opps(data, acc, acc_idx)
    with t_mr:       _input_mediaradar(data, acc, acc_idx)
    with t_sf:       _input_salesforce(data, acc, acc_idx, fy)


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    st.set_page_config(
        page_title="Roku Intelligence Center",
        page_icon="📡",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    st.markdown(CSS, unsafe_allow_html=True)

    data = load_data()
    for i, acc in enumerate(data["accounts"]):
        data["accounts"][i] = migrate_account(acc)

    render_sidebar(data)

    summary_tab, input_tab = st.tabs(["📡  Account Plan", "⚙️  Data Input"])
    with summary_tab:
        render_summary_page(data)
    with input_tab:
        render_input_page(data)


if __name__ == "__main__":
    main()
