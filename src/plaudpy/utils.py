"""PlaudPy utilities — reusable helper functions.

Functions here are added on-demand as needed during sessions.
Each function should be self-contained and well-documented.
"""

import sqlite3
from datetime import datetime, timezone, tzinfo
from pathlib import Path

from .client import PlaudClient
from .models import FileSimple

DEFAULT_DB_PATH = Path(__file__).parent.parent.parent / "plaud_data.db"

_SCHEMA = """
CREATE TABLE IF NOT EXISTS recordings (
    id              TEXT PRIMARY KEY,
    filename        TEXT NOT NULL DEFAULT '',
    duration        INTEGER NOT NULL DEFAULT 0,
    start_time_ms   INTEGER NOT NULL DEFAULT 0,
    local_datetime  TEXT,
    hour            INTEGER,
    weekday         INTEGER,       -- 0=Mon … 6=Sun
    weekday_name    TEXT,
    is_working_hours INTEGER DEFAULT 0,
    directory       TEXT,
    synced_at       TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS sync_log (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    synced_at   TEXT NOT NULL,
    total_files INTEGER NOT NULL
);
"""

_MIGRATIONS = [
    "ALTER TABLE recordings ADD COLUMN directory TEXT",
]

WEEKDAY_NAMES = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


def _get_all_files() -> list[FileSimple]:
    """Fetch all files from the account."""
    with PlaudClient() as client:
        return client.files.list_simple()


def get_db(db_path: str | Path | None = None) -> sqlite3.Connection:
    """Open (and initialize if needed) the PlaudPy SQLite database.

    Args:
        db_path: Path to the database file. Defaults to <project>/plaud_data.db.

    Returns:
        sqlite3.Connection with row_factory set to sqlite3.Row.
    """
    path = Path(db_path) if db_path else DEFAULT_DB_PATH
    conn = sqlite3.connect(str(path))
    conn.row_factory = sqlite3.Row
    conn.executescript(_SCHEMA)
    # Run migrations for existing DBs that lack newer columns
    for migration in _MIGRATIONS:
        try:
            conn.execute(migration)
            conn.commit()
        except sqlite3.OperationalError:
            pass  # column already exists
    return conn


def sync_recordings(
    db_path: str | Path | None = None,
    tz: tzinfo | None = None,
    work_start: int = 9,
    work_end: int = 18,
) -> int:
    """Fetch all recordings from Plaud and upsert them into the local database.

    Args:
        db_path: Path to the database file.
        tz: Timezone for computing local time fields. Defaults to system local tz.
        work_start: Start of working hours (inclusive, 24h). Default 9.
        work_end: End of working hours (exclusive, 24h). Default 18.

    Returns:
        Number of recordings synced.
    """
    if tz is None:
        tz = datetime.now().astimezone().tzinfo

    files = _get_all_files()
    now_iso = datetime.now(timezone.utc).isoformat()

    conn = get_db(db_path)
    try:
        for f in files:
            if f.start_time:
                dt = datetime.fromtimestamp(f.start_time / 1000.0, tz=timezone.utc).astimezone(tz)
                local_dt = dt.isoformat()
                hour = dt.hour
                weekday = dt.weekday()
                weekday_name = WEEKDAY_NAMES[weekday]
                is_working = 1 if (weekday < 5 and work_start <= hour < work_end) else 0
            else:
                local_dt = None
                hour = None
                weekday = None
                weekday_name = None
                is_working = 0

            conn.execute(
                """INSERT INTO recordings
                       (id, filename, duration, start_time_ms,
                        local_datetime, hour, weekday, weekday_name,
                        is_working_hours, synced_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                   ON CONFLICT(id) DO UPDATE SET
                       filename=excluded.filename,
                       duration=excluded.duration,
                       start_time_ms=excluded.start_time_ms,
                       local_datetime=excluded.local_datetime,
                       hour=excluded.hour,
                       weekday=excluded.weekday,
                       weekday_name=excluded.weekday_name,
                       is_working_hours=excluded.is_working_hours,
                       synced_at=excluded.synced_at
                """,
                (f.id, f.filename, f.duration, f.start_time,
                 local_dt, hour, weekday, weekday_name,
                 is_working, now_iso),
            )

        conn.execute(
            "INSERT INTO sync_log (synced_at, total_files) VALUES (?, ?)",
            (now_iso, len(files)),
        )
        conn.commit()
    finally:
        conn.close()

    return len(files)


# --- Query helpers (work against the local DB, no API calls) ---


def count_recordings(db_path: str | Path | None = None) -> int:
    """Return the total number of recordings in the local database."""
    conn = get_db(db_path)
    try:
        row = conn.execute("SELECT COUNT(*) AS n FROM recordings").fetchone()
        return row["n"]
    finally:
        conn.close()


def count_recordings_during_hours(
    start_hour: int = 9,
    end_hour: int = 18,
    weekdays_only: bool = True,
    db_path: str | Path | None = None,
) -> int:
    """Count recordings within specified hours from the local database.

    Args:
        start_hour: Start of window (inclusive), 24h format. Default 9.
        end_hour: End of window (exclusive), 24h format. Default 18.
        weekdays_only: If True, only count Mon-Fri. Default True.
        db_path: Path to the database file.
    """
    conn = get_db(db_path)
    try:
        sql = "SELECT COUNT(*) AS n FROM recordings WHERE hour >= ? AND hour < ?"
        params: list = [start_hour, end_hour]
        if weekdays_only:
            sql += " AND weekday < 5"
        row = conn.execute(sql, params).fetchone()
        return row["n"]
    finally:
        conn.close()


def recordings_by_weekday(db_path: str | Path | None = None) -> list[dict]:
    """Get recording counts grouped by weekday.

    Returns:
        List of dicts with 'weekday_name' and 'count', ordered Mon-Sun.
    """
    conn = get_db(db_path)
    try:
        rows = conn.execute(
            """SELECT weekday, weekday_name, COUNT(*) AS count
               FROM recordings
               WHERE weekday IS NOT NULL
               GROUP BY weekday
               ORDER BY weekday"""
        ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def recordings_by_hour(db_path: str | Path | None = None) -> list[dict]:
    """Get recording counts grouped by hour of day.

    Returns:
        List of dicts with 'hour' and 'count', ordered 0-23.
    """
    conn = get_db(db_path)
    try:
        rows = conn.execute(
            """SELECT hour, COUNT(*) AS count
               FROM recordings
               WHERE hour IS NOT NULL
               GROUP BY hour
               ORDER BY hour"""
        ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def assign_directory(
    directory: str,
    before: str | None = None,
    after: str | None = None,
    working_hours_only: bool = False,
    weekdays_only: bool = False,
    db_path: str | Path | None = None,
) -> int:
    """Assign a directory label to recordings matching the given criteria.

    Args:
        directory: Directory name to assign.
        before: ISO date string (exclusive upper bound on local_datetime).
        after: ISO date string (inclusive lower bound on local_datetime).
        working_hours_only: Only match recordings during working hours (9-18 M-F).
        weekdays_only: Only match Mon-Fri recordings.
        db_path: Path to the database file.

    Returns:
        Number of recordings updated.
    """
    conn = get_db(db_path)
    try:
        clauses = []
        params: list = []

        if before:
            clauses.append("local_datetime < ?")
            params.append(before)
        if after:
            clauses.append("local_datetime >= ?")
            params.append(after)
        if working_hours_only:
            clauses.append("is_working_hours = 1")
        elif weekdays_only:
            clauses.append("weekday < 5")

        where = " AND ".join(clauses) if clauses else "1=1"
        params.append(directory)

        cur = conn.execute(
            f"UPDATE recordings SET directory = ? WHERE {where}",
            [directory] + params[:-1],
        )
        conn.commit()
        return cur.rowcount
    finally:
        conn.close()


def assign_directory_and_tag(
    directory: str,
    before: str | None = None,
    after: str | None = None,
    working_hours_only: bool = False,
    weekdays_only: bool = False,
    db_path: str | Path | None = None,
) -> dict:
    """Assign a directory locally AND apply a matching Plaud tag via the API.

    Creates the tag on Plaud if it doesn't exist, then applies it to every
    matching recording in one batch call.

    Args:
        directory: Directory / tag name.
        before: ISO date (exclusive upper bound).
        after: ISO date (inclusive lower bound).
        working_hours_only: Only 9-18 M-F recordings.
        weekdays_only: Only Mon-Fri recordings.
        db_path: Path to the database file.

    Returns:
        Dict with 'db_updated' and 'api_tagged' counts.
    """
    # 1. Update local DB
    db_count = assign_directory(
        directory,
        before=before,
        after=after,
        working_hours_only=working_hours_only,
        weekdays_only=weekdays_only,
        db_path=db_path,
    )

    # 2. Get the IDs that were just assigned
    conn = get_db(db_path)
    try:
        rows = conn.execute(
            "SELECT id FROM recordings WHERE directory = ?", (directory,)
        ).fetchall()
        file_ids = [r["id"] for r in rows]
    finally:
        conn.close()

    if not file_ids:
        return {"db_updated": db_count, "api_tagged": 0}

    # 3. Find or create the tag on Plaud
    with PlaudClient() as client:
        existing_tags = client.tags.list_tags()
        tag = next((t for t in existing_tags if t.name == directory), None)
        if tag is None:
            tag = client.tags.create_tag(directory)

        # 4. Apply the tag to all matching recordings in one call
        client.files.update_tags(file_ids, tag.id)

    return {"db_updated": db_count, "api_tagged": len(file_ids)}


def recordings_by_directory(db_path: str | Path | None = None) -> list[dict]:
    """Get recording counts grouped by directory.

    Returns:
        List of dicts with 'directory' and 'count'.
    """
    conn = get_db(db_path)
    try:
        rows = conn.execute(
            """SELECT COALESCE(directory, '(unassigned)') AS directory, COUNT(*) AS count
               FROM recordings
               GROUP BY directory
               ORDER BY count DESC"""
        ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()
