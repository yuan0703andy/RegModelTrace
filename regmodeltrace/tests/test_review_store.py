import sqlite3

import pytest

from regmodeltrace.review_store import ReviewConflict, ReviewStore
from regmodeltrace.workbench import WorkbenchError


@pytest.fixture
def store(tmp_path):
    from regmodeltrace.workbench_server import WORKBENCH
    return ReviewStore(tmp_path / 'reviews.sqlite3', WORKBENCH)


def test_restart_revisions_retries_and_bindings(store):
    session = store.create_session('QA only')
    cid = next(iter(store.workbench.candidates))
    args = dict(event_id='first', decision='ACCEPTED', reason_code='RELEVANT_SUPPORT',
                rationale='Synthetic QA decision')
    event = store.append(session['session_id'], cid, **args)
    assert store.append(session['session_id'], cid, **args) == event
    for key, value in store.binding().items():
        assert event[key] == value
    assert event['passage_id'] == store.workbench.candidates[cid]['passage_id']
    with pytest.raises(ReviewConflict):
        store.append(session['session_id'], cid, **{**args, 'rationale': 'Different'})
    with pytest.raises(ReviewConflict):
        store.append(session['session_id'], cid, **{**args, 'event_id': 'stale'})
    store.append(session['session_id'], cid, event_id='second', decision='UNRESOLVED',
                 reason_code='NEED_BROADER_SEARCH', rationale='QA revision',
                 previous_event_id='first')
    reopened = ReviewStore(store.path, store.workbench)
    assert [r['event_id'] for r in reopened.history(session['session_id'], cid)] == ['first', 'second']
    with store.connect() as db, pytest.raises(sqlite3.IntegrityError):
        db.execute('DELETE FROM events')


def test_validation_and_navigation_do_not_write(store, monkeypatch):
    with pytest.raises(ValueError):
        store.create_session(' ')
    session = store.create_session('QA')
    cid = next(iter(store.workbench.candidates))
    store.workbench.candidate_payload(cid)
    assert store.history(session['session_id'], cid) == []
    args = dict(event_id='x', decision='ACCEPTED', reason_code='RELEVANT_SUPPORT',
                rationale='QA')
    with pytest.raises(KeyError):
        store.append('unknown', cid, **args)
    with pytest.raises(KeyError):
        store.append(session['session_id'], 'unknown', **args)
    with pytest.raises(ValueError):
        store.append(session['session_id'], cid, **{**args, 'rationale': ''})
    with pytest.raises(ValueError):
        store.append(session['session_id'], cid, **{**args, 'reason_code': 'NOT_A_REASON'})
    def fail(_):
        raise WorkbenchError('Source failure')
    monkeypatch.setattr(store.workbench, 'candidate_payload', fail)
    with pytest.raises(WorkbenchError):
        store.append(session['session_id'], cid, **args)
    assert store.history(session['session_id'], cid) == []


def test_http_history_and_host_owned_provenance(store, monkeypatch):
    from fastapi.testclient import TestClient
    from regmodeltrace import workbench_server as server
    monkeypatch.setattr(server, 'REVIEW_STORE', store)
    client = TestClient(server.app)
    sid = client.post('/api/review-sessions', json={'reviewer': 'QA'}).json()['session_id']
    cid = next(iter(store.workbench.candidates))
    url = f'/api/review-sessions/{sid}/candidates/{cid}'
    body = dict(event_id='http', decision='REJECTED', reason_code='WRONG_SOURCE',
                rationale='QA only')
    assert client.post(url, json={**body, 'corpus_snapshot_id': 'fake'}).status_code == 422
    assert client.post(url, json=body).status_code == 200
    assert client.post(url, json=body).status_code == 200
    history = client.get(url).json()
    assert len(history) == 1
    assert history[0]['decision'] == 'REJECTED'
    assert history[0]['reason_code'] == 'WRONG_SOURCE'
    exported = client.get(f'/api/review-sessions/{sid}/exports/evidence_packet.json')
    assert exported.status_code == 200
    assert exported.headers['content-disposition'] == (
        'attachment; filename="evidence_packet.json"'
    )
    assert exported.json()['review_event_count'] == 1
    assert client.get(f'/api/review-sessions/{sid}/exports/unknown').status_code == 404
    assert client.get('/api/review-sessions/unknown').status_code == 404
