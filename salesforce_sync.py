"""
Salesforce sync utilities for Roku Intelligence Center.
All simple_salesforce imports are lazy so the module can be imported
even if the package isn't installed yet.

Authentication — two supported modes (env-var driven):

  SSO / OAuth 2.0 (recommended for corporate / Okta environments):
      SF_CLIENT_ID      — Connected App Consumer Key
      SF_CLIENT_SECRET  — Connected App Consumer Secret
      SF_USERNAME       — Salesforce login (SSO username)
      SF_PASSWORD       — Salesforce password  (no security token required)
      SF_DOMAIN         — optional, defaults to "login"
                          use your My Domain slug for SSO orgs
                          e.g. "roku.my" for https://roku.my.salesforce.com

  Legacy username / password / security token:
      SF_USERNAME
      SF_PASSWORD
      SF_SECURITY_TOKEN
      SF_DOMAIN         — optional, defaults to "login"

connect_from_env() detects which mode to use based on which vars are present.
"""

import datetime
import os


def _soql_escape(s: str) -> str:
    """Escape a string for use inside a SOQL single-quoted literal."""
    return s.replace("\\", "\\\\").replace("'", "\\'")


def _close_date_to_fy_quarter(close_date_str: str):
    """Return (calendar_year: int, quarter: str) e.g. (2026, 'Q1')."""
    d = datetime.date.fromisoformat(close_date_str)
    q = (d.month - 1) // 3 + 1
    return d.year, f"Q{q}"


# ── Connection helpers ────────────────────────────────────────────────────────

def connect_oauth(client_id: str, client_secret: str,
                  username: str, password: str,
                  domain: str = "login"):
    """
    Authenticate via OAuth 2.0 Resource Owner Password flow (Connected App).

    This is the correct method for SSO / Okta-federated Salesforce orgs:
      - No security token required
      - Works when direct username+password login is disabled in favour of SSO
      - Requires a Connected App configured in Salesforce with the
        'api' OAuth scope and password grant type enabled

    For My Domain orgs (e.g. roku.my.salesforce.com) set domain='roku.my'.
    """
    import requests
    from simple_salesforce import Salesforce

    token_url = f"https://{domain}.salesforce.com/services/oauth2/token"
    resp = requests.post(token_url, data={
        "grant_type":    "password",
        "client_id":     client_id,
        "client_secret": client_secret,
        "username":      username,
        "password":      password,
    })

    if not resp.ok:
        try:
            err = resp.json().get("error_description") or resp.json().get("error")
        except Exception:
            err = resp.text
        raise ConnectionError(f"OAuth token request failed ({resp.status_code}): {err}")

    token_data = resp.json()
    return Salesforce(
        session_id=token_data["access_token"],
        instance_url=token_data["instance_url"],
    )


def connect(username: str, password: str, security_token: str, domain: str = "login"):
    """Legacy username + password + security token auth (non-SSO orgs)."""
    from simple_salesforce import Salesforce
    return Salesforce(
        username=username,
        password=password,
        security_token=security_token,
        domain=domain,
    )


def test_connection(sf) -> tuple:
    """
    Verify a live Salesforce connection.
    Accepts an already-connected sf object.
    Returns (success: bool, message: str).
    """
    try:
        result = sf.query("SELECT Id, Name FROM User LIMIT 1")
        user = result["records"][0]["Name"] if result.get("records") else "unknown"
        return True, f"Connected as {user}"
    except Exception as exc:
        return False, str(exc)


def fetch_opportunities(sf, sf_account_name: str, fy: int,
                        activation_field: str = "Type",
                        activation_map: dict = None) -> tuple:
    """
    Query Closed Won opportunities for a given account name and fiscal year.

    Returns:
        (quarters_dict, record_count)

    quarters_dict structure:
        {
          "Q1": {"booked": 0.0, "act_dio": 0.0, "act_pmpg": 0.0,
                 "act_sponsorship": 0.0, "act_channel": 0.0, "act_ads": 0.0},
          ...
        }
    """
    ACT_KEYS = ["act_dio", "act_pmpg", "act_sponsorship", "act_channel", "act_ads"]
    if activation_map is None:
        activation_map = {}

    af = (activation_field or "Type").strip()
    safe_name = _soql_escape(sf_account_name)

    soql = (
        f"SELECT Amount, CloseDate, {af} "
        f"FROM Opportunity "
        f"WHERE Account.Name = '{safe_name}' "
        f"AND StageName = 'Closed Won' "
        f"AND CALENDAR_YEAR(CloseDate) = {int(fy)}"
    )

    result = sf.query_all(soql)
    records = result.get("records", [])

    quarters = {
        q: {"booked": 0.0, **{k: 0.0 for k in ACT_KEYS}}
        for q in ["Q1", "Q2", "Q3", "Q4"]
    }

    for opp in records:
        amount = float(opp.get("Amount") or 0)
        close_date = opp.get("CloseDate", "")
        if not close_date or amount == 0:
            continue
        year, q_str = _close_date_to_fy_quarter(close_date)
        if year != fy:
            continue

        quarters[q_str]["booked"] += amount

        act_val = str(opp.get(af) or "")
        act_key = activation_map.get(act_val, "")
        if act_key in ACT_KEYS:
            quarters[q_str][act_key] += amount

    return quarters, len(records)


def fetch_pipeline(sf, sf_account_name: str, fy: int) -> tuple:
    """
    Fetch open (not Closed Won / Closed Lost) opportunities.

    Returns:
        (quarterly_goals: dict, open_opps: list)

    quarterly_goals: {"Q1": 0.0, ...}  — pipeline total per quarter → used as Goal
    open_opps: [{"text": "...", "completed": False}, ...]  → short_term_opps
    """
    safe_name = _soql_escape(sf_account_name)
    soql = (
        f"SELECT Name, Amount, CloseDate, StageName "
        f"FROM Opportunity "
        f"WHERE Account.Name = '{safe_name}' "
        f"AND StageName NOT IN ('Closed Won', 'Closed Lost') "
        f"AND CALENDAR_YEAR(CloseDate) = {int(fy)} "
        f"ORDER BY CloseDate ASC"
    )

    result = sf.query_all(soql)
    records = result.get("records", [])

    quarterly_goals = {"Q1": 0.0, "Q2": 0.0, "Q3": 0.0, "Q4": 0.0}
    open_opps = []

    for opp in records:
        amount = float(opp.get("Amount") or 0)
        close_date = opp.get("CloseDate", "")
        name = str(opp.get("Name") or "Unnamed Opportunity")
        stage = str(opp.get("StageName") or "")

        if close_date:
            year, q_str = _close_date_to_fy_quarter(close_date)
            if year == fy:
                quarterly_goals[q_str] += amount

        parts = [name]
        if amount:
            if amount >= 1_000_000:
                parts.append(f"${amount / 1_000_000:.1f}M")
            elif amount >= 1_000:
                parts.append(f"${amount / 1_000:.0f}K")
            else:
                parts.append(f"${amount:,.0f}")
        if stage:
            parts.append(stage)
        if close_date:
            parts.append(f"Close: {close_date}")

        open_opps.append({"text": " · ".join(parts), "completed": False})

    return quarterly_goals, open_opps


def fetch_account_metadata(sf, sf_account_name: str,
                           vertical_field: str = "Industry",
                           sub_vertical_field: str = "") -> dict:
    """
    Query vertical and sub-vertical from the SF Account record.
    Returns dict with 'vertical' and optionally 'sub_vertical'.
    """
    safe_name = _soql_escape(sf_account_name)
    fields = ["Name"]
    if vertical_field:
        fields.append(vertical_field)
    if sub_vertical_field:
        fields.append(sub_vertical_field)

    soql = f"SELECT {', '.join(fields)} FROM Account WHERE Name = '{safe_name}' LIMIT 1"
    result = sf.query(soql)
    records = result.get("records", [])
    if not records:
        return {}

    rec = records[0]
    out = {}
    if vertical_field:
        out["vertical"] = rec.get(vertical_field, "") or ""
    if sub_vertical_field:
        out["sub_vertical"] = rec.get(sub_vertical_field, "") or ""
    return out


def fetch_brand_opportunities(sf, brand_name: str) -> list:
    """
    Fetch all non-Closed-Lost opportunities for a brand/advertiser name.
    Returns a list of dicts with id, name, amount, close_date, stage, type.
    """
    safe_name = _soql_escape(brand_name)
    soql = (
        f"SELECT Id, Name, Amount, CloseDate, StageName, Type "
        f"FROM Opportunity "
        f"WHERE Account.Name = '{safe_name}' "
        f"AND StageName != 'Closed Lost' "
        f"ORDER BY CloseDate ASC"
    )
    result = sf.query_all(soql)
    records = result.get("records", [])

    opps = []
    for rec in records:
        amount = float(rec.get("Amount") or 0)
        close_date = rec.get("CloseDate") or ""
        year, quarter = _close_date_to_fy_quarter(close_date) if close_date else (None, "")
        opps.append({
            "id":         rec.get("Id", ""),
            "name":       rec.get("Name", "") or "",
            "amount":     amount,
            "close_date": close_date,
            "stage":      rec.get("StageName", "") or "",
            "type":       rec.get("Type", "") or "",
            "quarter":    quarter,
            "year":       year,
        })
    return opps


# ── Environment-variable auth ─────────────────────────────────────────────────

def env_vars_configured() -> bool:
    """
    True if enough env vars are set to attempt a connection.
    Accepts either the OAuth set or the legacy set.
    """
    oauth_set  = ("SF_CLIENT_ID", "SF_CLIENT_SECRET", "SF_USERNAME", "SF_PASSWORD")
    legacy_set = ("SF_USERNAME", "SF_PASSWORD", "SF_SECURITY_TOKEN")
    return (
        all(os.environ.get(k) for k in oauth_set) or
        all(os.environ.get(k) for k in legacy_set)
    )


def auth_mode() -> str:
    """
    Returns 'oauth' if SF_CLIENT_ID is present, 'legacy' if SF_SECURITY_TOKEN
    is present, or 'none' if neither set is complete.
    """
    if all(os.environ.get(k) for k in ("SF_CLIENT_ID", "SF_CLIENT_SECRET",
                                        "SF_USERNAME", "SF_PASSWORD")):
        return "oauth"
    if all(os.environ.get(k) for k in ("SF_USERNAME", "SF_PASSWORD",
                                        "SF_SECURITY_TOKEN")):
        return "legacy"
    return "none"


def connect_from_env():
    """
    Connect to Salesforce using environment variables.

    Prefers OAuth (SSO) when SF_CLIENT_ID is present;
    falls back to username/password/token for non-SSO orgs.
    Raises EnvironmentError with a clear message if required vars are missing.
    """
    domain = os.environ.get("SF_DOMAIN", "login")
    mode   = auth_mode()

    if mode == "oauth":
        return connect_oauth(
            client_id     = os.environ["SF_CLIENT_ID"],
            client_secret = os.environ["SF_CLIENT_SECRET"],
            username      = os.environ["SF_USERNAME"],
            password      = os.environ["SF_PASSWORD"],
            domain        = domain,
        )

    if mode == "legacy":
        return connect(
            username       = os.environ["SF_USERNAME"],
            password       = os.environ["SF_PASSWORD"],
            security_token = os.environ["SF_SECURITY_TOKEN"],
            domain         = domain,
        )

    # Neither set is complete — report what's missing
    oauth_missing  = [k for k in ("SF_CLIENT_ID", "SF_CLIENT_SECRET",
                                   "SF_USERNAME", "SF_PASSWORD")
                      if not os.environ.get(k)]
    legacy_missing = [k for k in ("SF_USERNAME", "SF_PASSWORD", "SF_SECURITY_TOKEN")
                      if not os.environ.get(k)]
    raise EnvironmentError(
        "Salesforce environment variables not configured.\n"
        f"  For SSO / OAuth:   set {', '.join(oauth_missing)}\n"
        f"  For legacy auth:   set {', '.join(legacy_missing)}"
    )


# ── Date helpers ──────────────────────────────────────────────────────────────

def get_current_quarter_dates() -> tuple:
    """
    Returns (start_date_str, end_date_str) for the current calendar quarter.
    e.g. ('2026-04-01', '2026-06-30')
    """
    today = datetime.date.today()
    q = (today.month - 1) // 3 + 1
    start_month = (q - 1) * 3 + 1
    start = datetime.date(today.year, start_month, 1)

    end_month = start_month + 2
    # Last day of end_month
    if end_month == 12:
        end = datetime.date(today.year, 12, 31)
    else:
        end = datetime.date(today.year, end_month + 1, 1) - datetime.timedelta(days=1)

    return start.isoformat(), end.isoformat()


# ── Granular fetch helpers ────────────────────────────────────────────────────

def _fetch_quarter_booked(sf, account_name: str,
                          start_date: str, end_date: str) -> float:
    """Sum of Closed Won opportunity amounts with CloseDate in [start_date, end_date]."""
    safe_name = _soql_escape(account_name)
    soql = (
        f"SELECT SUM(Amount) booked "
        f"FROM Opportunity "
        f"WHERE Account.Name = '{safe_name}' "
        f"AND StageName = 'Closed Won' "
        f"AND CloseDate >= {start_date} "
        f"AND CloseDate <= {end_date}"
    )
    result  = sf.query(soql)
    records = result.get("records", [])
    if records:
        val = records[0].get("booked") or records[0].get("expr0")
        return float(val or 0)
    return 0.0


_LATE_STAGES = (
    "'Proposal/Price Quote'",
    "'Value Proposition'",
    "'Negotiation/Review'",
    "'Perception Analysis'",
    "'Id. Decision Makers'",
)


def _fetch_revenue_at_risk(sf, account_name: str,
                           start_date: str, end_date: str) -> float:
    """
    Total value of late-stage opportunities closing this quarter that are
    not yet Closed Won — i.e. revenue that could slip.
    """
    safe_name = _soql_escape(account_name)
    soql = (
        f"SELECT SUM(Amount) rar "
        f"FROM Opportunity "
        f"WHERE Account.Name = '{safe_name}' "
        f"AND StageName IN ({', '.join(_LATE_STAGES)}) "
        f"AND CloseDate >= {start_date} "
        f"AND CloseDate <= {end_date}"
    )
    result  = sf.query(soql)
    records = result.get("records", [])
    if records:
        val = records[0].get("rar") or records[0].get("expr0")
        return float(val or 0)
    return 0.0


def _fetch_active_opportunities(sf, account_name: str) -> list:
    """
    All open (not Closed Won / Closed Lost) opportunities for the advertiser.
    Returns [{"name": str, "stage": str, "amount": float}, ...]
    """
    safe_name = _soql_escape(account_name)
    soql = (
        f"SELECT Name, StageName, Amount, CloseDate "
        f"FROM Opportunity "
        f"WHERE Account.Name = '{safe_name}' "
        f"AND StageName NOT IN ('Closed Won', 'Closed Lost') "
        f"ORDER BY Amount DESC NULLS LAST "
        f"LIMIT 100"
    )
    result = sf.query_all(soql)
    return [
        {
            "name":       rec.get("Name", "") or "",
            "stage":      rec.get("StageName", "") or "",
            "amount":     float(rec.get("Amount") or 0),
            "close_date": rec.get("CloseDate", "") or "",
        }
        for rec in result.get("records", [])
    ]


def _fetch_fy_performance(sf, account_name: str, fy: int) -> tuple:
    """
    FY breakdown: quarterly Closed Won (booked) + open pipeline per quarter.

    Returns:
        quarterly  : {"Q1": {"booked": float, "goal": float}, "Q2": ..., ...}
        fy_booked  : float — sum of all Closed Won for the FY
        fy_goal    : float — booked + pipeline (total FY opp value)
        pipeline   : float — sum of all open opps for the FY
    """
    safe_name = _soql_escape(account_name)
    soql = (
        f"SELECT Name, Amount, CloseDate, StageName "
        f"FROM Opportunity "
        f"WHERE Account.Name = '{safe_name}' "
        f"AND StageName != 'Closed Lost' "
        f"AND CALENDAR_YEAR(CloseDate) = {int(fy)}"
    )
    result  = sf.query_all(soql)
    records = result.get("records", [])

    quarterly  = {q: {"booked": 0.0, "goal": 0.0} for q in ("Q1", "Q2", "Q3", "Q4")}
    fy_booked  = 0.0
    pipeline   = 0.0

    for rec in records:
        amount     = float(rec.get("Amount") or 0)
        close_date = rec.get("CloseDate", "")
        stage      = rec.get("StageName", "")
        if not close_date or amount == 0:
            continue

        year, q_str = _close_date_to_fy_quarter(close_date)
        if year != fy or q_str not in quarterly:
            continue

        if stage == "Closed Won":
            quarterly[q_str]["booked"] += amount
            fy_booked += amount
        else:
            quarterly[q_str]["goal"] += amount
            pipeline += amount

    fy_goal = fy_booked + pipeline
    return quarterly, fy_booked, fy_goal, pipeline


def _suggest_account_names(sf, partial_name: str, limit: int = 5) -> list:
    """
    LIKE search for Account names similar to partial_name.
    Used to surface alternatives when an exact match returns no results.
    """
    safe_partial = _soql_escape(partial_name)
    soql = (
        f"SELECT Name FROM Account "
        f"WHERE Name LIKE '%{safe_partial}%' "
        f"ORDER BY Name ASC "
        f"LIMIT {int(limit)}"
    )
    result = sf.query(soql)
    return [rec["Name"] for rec in result.get("records", [])]


# ── Master function ───────────────────────────────────────────────────────────

def get_salesforce_data(sf, account_name: str, fy: int) -> dict:
    """
    Fetch all dashboard-relevant data for a brand / advertiser in one call.

    Returns:
        {
            "brand":                str,
            "quarter_booked":       float,
            "revenue_at_risk":      float,
            "active_opportunities": [{"name", "stage", "amount", "close_date"}],
            "fy_booked":            float,
            "fy_goal":              float,
            "pipeline":             float,
            "quarterly": {
                "Q1": {"booked": float, "goal": float},
                ...
            },
            "suggestions":  [str],   # alternate SF account names (if no data found)
            "fetched_at":   str,     # ISO timestamp
        }
    """
    q_start, q_end = get_current_quarter_dates()

    quarter_booked = _fetch_quarter_booked(sf, account_name, q_start, q_end)
    revenue_at_risk = _fetch_revenue_at_risk(sf, account_name, q_start, q_end)
    active_opps = _fetch_active_opportunities(sf, account_name)
    quarterly, fy_booked, fy_goal, pipeline = _fetch_fy_performance(sf, account_name, fy)

    suggestions = []
    if fy_booked == 0 and pipeline == 0 and not active_opps:
        suggestions = _suggest_account_names(sf, account_name)

    return {
        "brand":                account_name,
        "quarter_booked":       quarter_booked,
        "revenue_at_risk":      revenue_at_risk,
        "active_opportunities": active_opps,
        "fy_booked":            fy_booked,
        "fy_goal":              fy_goal,
        "pipeline":             pipeline,
        "quarterly":            quarterly,
        "suggestions":          suggestions,
        "fetched_at":           datetime.datetime.now().isoformat(timespec="seconds"),
    }
