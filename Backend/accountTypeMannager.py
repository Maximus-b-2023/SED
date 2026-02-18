import sqlite3
import logging

logger = logging.getLogger(__name__)


def authAdmin(UID):
    try:
        conn = sqlite3.connect('./instance/db.sqlite3')
        cur = conn.cursor()
    except Exception:
        logger.error("DB connection failed in authAdmin")
        return False
    try:
        sql = 'SELECT ACCOUNTTYPE FROM users WHERE ROWID = ?'
        cur.execute(sql, (UID,))
        accountType = cur.fetchone()
    except Exception:
        logger.exception("Failed to retrieve account type for UID=%s", UID)
        return False
    if not accountType:
        logger.info("No accountType found for UID=%s", UID)
        return False
    try:
        is_admin = str(accountType[0]) == "Admin"
    except Exception:
        logger.exception("Unexpected accountType format for UID=%s: %s", UID, accountType)
        return False
    logger.debug("authAdmin for UID=%s -> %s", UID, is_admin)
    return is_admin


def fetchUsers(UID):
    try:
        conn = sqlite3.connect('./instance/db.sqlite3')
        cur = conn.cursor()
    except:
        return "connection failed"
    if authAdmin(UID) == True:
        try:
            sql = '''SELECT ROWID, USERNAME, ACCOUNTTYPE FROM users'''
            cur.execute(sql)
            userList = cur.fetchall()
            print(userList)
            return userList
        except:
            print("Fetch failed")
            return "Fetch failed"
    else:
        print("User not verified for this action")
        return "User not verified for this action"
    

def updateAccountType(UID,targetUID, newAccountType):
    try:
        conn = sqlite3.connect('./instance/db.sqlite3')
        cur = conn.cursor()
    except:
        logger.error("DB connection failed in updateAccountType")
        return "connection failed"
    # ensure UIDs are integers
    try:
        uid_int = int(UID)
        target_uid_int = int(targetUID)
    except Exception:
        logger.warning("Invalid UID or targetUID: UID=%s targetUID=%s", UID, targetUID)
        return "invalid UID"

    # allowlist account types
    allowed = ("User", "Admin")
    if newAccountType not in allowed:
        logger.warning("Rejected updateAccountType with invalid account type: %s", newAccountType)
        return "invalid account type"

    if authAdmin(uid_int) == True:
        try:
            sql = 'UPDATE users SET accounttype = ? WHERE ROWID = ?'
            cur.execute(sql, (newAccountType, target_uid_int))
            conn.commit()
            msg = f"User {target_uid_int} updated to account type {newAccountType}"
            logger.info(msg)
            return msg
        except Exception:
            logger.exception("Update failed for targetUID=%s", target_uid_int)
            return "Update failed"
    else:
        logger.warning("User %s not verified for updateAccountType", UID)
        return "User not verified for this action"

