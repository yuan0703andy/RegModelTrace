"""Local append-only reviewer assertions; never changes frozen evidence."""
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4


class ReviewConflict(ValueError):
    pass


DECISIONS = {"ACCEPTED", "REJECTED", "UNRESOLVED"}
REASON_CODES = {
    "RELEVANT_SUPPORT",
    "IRRELEVANT",
    "INSUFFICIENT_EVIDENCE",
    "MISSING_QUALIFICATION",
    "WRONG_SOURCE",
    "WRONG_VERSION",
    "NEED_BROADER_SEARCH",
    "OTHER",
}


class ReviewStore:
    def __init__(self, path, workbench):
        self.path = Path(path)
        self.workbench = workbench
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.connect() as db:
            db.executescript('''
                CREATE TABLE IF NOT EXISTS sessions (id TEXT PRIMARY KEY, payload TEXT NOT NULL);
                CREATE TABLE IF NOT EXISTS events (seq INTEGER PRIMARY KEY AUTOINCREMENT,
                    id TEXT UNIQUE NOT NULL, session TEXT NOT NULL, candidate TEXT NOT NULL,
                    payload TEXT NOT NULL);
                CREATE TRIGGER IF NOT EXISTS no_event_update BEFORE UPDATE ON events
                    BEGIN SELECT RAISE(ABORT, 'append only'); END;
                CREATE TRIGGER IF NOT EXISTS no_event_delete BEFORE DELETE ON events
                    BEGIN SELECT RAISE(ABORT, 'append only'); END;
            ''')

    def connect(self):
        return sqlite3.connect(self.path, timeout=10)

    def binding(self):
        case = self.workbench.case_payload()
        return {key: case[key] for key in
                ('retrieval_run_id', 'corpus_snapshot_id', 'index_build_id')}

    def create_session(self, reviewer):
        if not reviewer.strip() or len(reviewer) > 200:
            raise ValueError('Reviewer name required (maximum 200 characters)')
        session = dict(session_id=str(uuid4()), reviewer=reviewer.strip(),
                       created_at=datetime.now(timezone.utc).isoformat(), **self.binding())
        with self.connect() as db:
            db.execute('INSERT INTO sessions VALUES (?, ?)',
                       (session['session_id'], json.dumps(session)))
        return session

    def session(self, session_id):
        with self.connect() as db:
            row = db.execute('SELECT payload FROM sessions WHERE id=?', (session_id,)).fetchone()
        if row is None:
            raise KeyError('Unknown review session')
        session = json.loads(row[0])
        if any(session[k] != v for k, v in self.binding().items()):
            raise ReviewConflict('Session belongs to a different frozen case')
        return session

    def snapshot(self, session_id):
        """Read one session and all events from a consistent SQLite snapshot."""

        with self.connect() as db:
            db.execute('BEGIN')
            row = db.execute('SELECT payload FROM sessions WHERE id=?', (session_id,)).fetchone()
            if row is None:
                raise KeyError('Unknown review session')
            session = json.loads(row[0])
            rows = db.execute(
                'SELECT payload FROM events WHERE session=? ORDER BY seq', (session_id,)
            ).fetchall()
        binding = self.binding()
        if any(session[k] != v for k, v in binding.items()):
            raise ReviewConflict('Session belongs to a different frozen case')
        events = [json.loads(row[0]) for row in rows]
        for event in events:
            if event['session_id'] != session_id:
                raise ReviewConflict('Event belongs to a different review session')
            if event['candidate_id'] not in self.workbench.candidates:
                raise ReviewConflict('Event references an unknown frozen candidate')
            if any(event[k] != v for k, v in binding.items()):
                raise ReviewConflict('Event belongs to a different frozen case')
        return session, events

    def history(self, session_id, candidate_id):
        if candidate_id not in self.workbench.candidates:
            raise KeyError('Unknown candidate')
        _, events = self.snapshot(session_id)
        return [event for event in events if event['candidate_id'] == candidate_id]

    def append(self, session_id, candidate_id, *, event_id, decision, reason_code, rationale,
               previous_event_id=None):
        session = self.session(session_id)
        detail = self.workbench.candidate_payload(candidate_id)
        if not event_id.strip() or len(event_id) > 200:
            raise ValueError('Event identity required')
        if decision not in DECISIONS:
            raise ValueError('Invalid decision')
        if reason_code not in REASON_CODES:
            raise ValueError('Invalid reason code')
        if not rationale.strip() or len(rationale) > 10000:
            raise ValueError('Rationale required (maximum 10000 characters)')
        if detail['source_status'] != 'RESOLVED':
            raise ReviewConflict('Source is not resolved')
        event = dict(event_id=event_id, session_id=session_id, candidate_id=candidate_id,
                     reviewer=session['reviewer'], decision=decision,
                     reason_code=reason_code,
                     rationale=rationale.strip(), previous_event_id=previous_event_id,
                     passage_id=detail['passage_id'], document_id=detail['document_id'],
                     **self.binding())
        with self.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            old = db.execute('SELECT payload FROM events WHERE id=?', (event_id,)).fetchone()
            if old:
                saved = json.loads(old[0])
                if any(saved[k] != v for k, v in event.items()):
                    raise ReviewConflict('Event identity reused with different content')
                return saved
            last = db.execute('SELECT id FROM events WHERE session=? AND candidate=? ORDER BY seq DESC LIMIT 1',
                              (session_id, candidate_id)).fetchone()
            if (last[0] if last else None) != previous_event_id:
                raise ReviewConflict('Stale decision; reload history before revising')
            event['created_at'] = datetime.now(timezone.utc).isoformat()
            db.execute('INSERT INTO events(id,session,candidate,payload) VALUES (?,?,?,?)',
                       (event_id, session_id, candidate_id, json.dumps(event)))
        return event
