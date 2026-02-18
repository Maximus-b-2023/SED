import sqlite3
import logging

logger = logging.getLogger(__name__)


def _fetch_single_int(column: str, licence_id) -> int | None:
    """Fetch a single integer column for a licence by id using parameterized SQL.
    Returns None if the row or value doesn't exist.
    """
    try:
        lid = int(licence_id)
    except Exception:
        logger.warning("Invalid licence_id provided: %s", licence_id)
        return None

    try:
        conn = sqlite3.connect('./instance/db.sqlite3')
        cur = conn.cursor()
    except Exception:
        logger.exception("DB connection failed in _fetch_single_int")
        return None

    try:
        sql = f"SELECT {column} FROM licences WHERE id = ?"
        cur.execute(sql, (lid,))
        row = cur.fetchone()
        if not row or row[0] is None:
            return None
        return int(row[0])
    except Exception:
        logger.exception("Failed to fetch %s for licence id=%s", column, licence_id)
        return None


def getLicencePrice(licence_id):
    """Return the LICENCEPRICE for the licence (preserves original behaviour).
    Returns 0 if not found or invalid input.
    """
    val = _fetch_single_int("LICENCEPRICE", licence_id)
    return int(val) if val is not None else 0


def getLowestSellingPrice(licence_id):
    """Return the LOWESTSELLINGPRICE for the licence. Returns 0 if missing.
    """
    val = _fetch_single_int("LOWESTSELLINGPRICE", licence_id)
    return int(val) if val is not None else 0


def calcMinValue(licenceID, quantity):
    """Calculate the minimum value using the lowest selling price."""
    minValue = quantity * getLowestSellingPrice(licenceID)
    return minValue


def calcLicenceCost(licenceID, quantity):
    licencesCost = quantity * getLicencePrice(licenceID)
    return licencesCost
