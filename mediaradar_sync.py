"""
MediaRadar integration for Roku Intelligence Center.

Current status: placeholder implementation.
The public interface (get_mediaradar_data) is stable — swap in the real API
call inside _call_mediaradar_api() when credentials are available.

Authentication (when live):
    MEDIARADAR_API_KEY  — set as an environment variable

Brand normalization:
    MediaRadar indexes by brand, not by agency. normalize_brand_name() strips
    common agency parentheticals (e.g. "Nike (OMD)" → "Nike") before lookup.
"""

import os
import re


# ── Brand name normalization ──────────────────────────────────────────────────

_AGENCY_PARENTHETICALS = re.compile(r"\s*\([^)]*\)")

_AGENCY_SUFFIXES = [
    " - OMD", " - Mindshare", " - Wavemaker", " - MediaCom",
    " - Zenith", " - Starcom", " - Spark Foundry", " - Assembly",
    " / ",
]


def normalize_brand_name(brand_name: str) -> str:
    """
    Strip agency parentheticals and suffixes, return clean brand name.

    Examples:
        "Nike (OMD)"            → "Nike"
        "Nike - OMD"            → "Nike"
        "P&G / Tide"            → "P&G"
        "Samsung Electronics"   → "Samsung Electronics"  (unchanged)
    """
    cleaned = _AGENCY_PARENTHETICALS.sub("", brand_name).strip()
    for suffix in _AGENCY_SUFFIXES:
        if suffix in cleaned:
            cleaned = cleaned[: cleaned.index(suffix)].strip()
    return cleaned


# ── Public interface ──────────────────────────────────────────────────────────

def get_mediaradar_data(brand_name: str) -> dict:
    """
    Return competitive intelligence for brand_name.

    Tries the real MediaRadar API first; falls back to an empty placeholder
    if the API key is not configured or a network error occurs.

    Return shape:
        {
            "brand": str,
            "source": "api" | "placeholder",
            "competitors": [
                {
                    "name":            str,
                    "ctv_investment":  str,
                    "buying_approach": str,
                    "targeting":       [str],
                    "creative":        [str],
                    "measurement":     [str],
                }
            ],
            "error": str | None,   # set on API failure, not raised
        }
    """
    normalized = normalize_brand_name(brand_name)

    try:
        data = _call_mediaradar_api(normalized)
        data["source"] = "api"
        data["error"] = None
        return data
    except NotImplementedError:
        return {**_placeholder_data(normalized), "source": "placeholder", "error": None}
    except Exception as exc:
        return {**_placeholder_data(normalized), "source": "placeholder", "error": str(exc)}


# ── API implementation (plug in here) ────────────────────────────────────────

def _call_mediaradar_api(brand_name: str) -> dict:
    """
    Replace the body of this function with the real MediaRadar API call.

    Expected env var:  MEDIARADAR_API_KEY

    Raises:
        NotImplementedError  — when MEDIARADAR_API_KEY is not set
        requests.HTTPError   — on API-level errors (once implemented)

    Skeleton for when the API is available:

        import requests

        base_url = "https://api.mediaradar.com/v1"   # confirm with vendor
        headers  = {"Authorization": f"Bearer {api_key}", "Accept": "application/json"}

        # Step 1 — resolve brand to MediaRadar brand_id
        r = requests.get(f"{base_url}/brands/search",
                         headers=headers, params={"q": brand_name, "limit": 1})
        r.raise_for_status()
        brand_id = r.json()["results"][0]["brand_id"]

        # Step 2 — fetch top 3 competitors
        r = requests.get(f"{base_url}/brands/{brand_id}/competitors",
                         headers=headers, params={"limit": 3, "channel": "ctv"})
        r.raise_for_status()

        return _parse_api_response(r.json())
    """
    api_key = os.environ.get("MEDIARADAR_API_KEY")
    if not api_key:
        raise NotImplementedError(
            "MEDIARADAR_API_KEY is not set — using placeholder data."
        )

    # TODO: implement real API call (see docstring skeleton above)
    raise NotImplementedError("MediaRadar API call not yet implemented.")


def _parse_api_response(raw: dict) -> dict:
    """
    Transform the raw MediaRadar API payload into the RIC competitor shape.
    Update this once the real response schema is known.
    """
    competitors = []
    for item in raw.get("competitors", [])[:3]:
        competitors.append({
            "name":            item.get("brand_name", ""),
            "ctv_investment":  item.get("ctv_spend_display", ""),
            "buying_approach": item.get("buying_approach", ""),
            "targeting":       item.get("targeting_tactics", []),
            "creative":        item.get("creative_formats", []),
            "measurement":     item.get("measurement_partners", []),
        })
    return {"brand": raw.get("brand_name", ""), "competitors": competitors}


def _placeholder_data(brand_name: str) -> dict:
    """Empty competitor slots — renders cleanly with '—' values in the dashboard."""
    return {
        "brand": brand_name,
        "competitors": [
            {
                "name":            "",
                "ctv_investment":  "",
                "buying_approach": "",
                "targeting":       [],
                "creative":        [],
                "measurement":     [],
            }
            for _ in range(3)
        ],
    }


# ── Utility ───────────────────────────────────────────────────────────────────

def api_configured() -> bool:
    """True if MEDIARADAR_API_KEY is present in the environment."""
    return bool(os.environ.get("MEDIARADAR_API_KEY"))
