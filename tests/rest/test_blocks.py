import requests


def test_get_block_latest(get_rest):
    r = get_rest('blocks')
    assert r.status_code == 200


# def test_get_block_latest():
#     url = settings.SERVER_HOST + "blocks"
#     response = requests.get(url)
#     assert response.status_code == 200


# def test_get_block_by_height(get_rest):
#     r = get_rest('blocks/height/30000001')
#     assert r.status_code == 200


# def test_get_block_by_height():
#     url = settings.SERVER_HOST + "blocks/height/10000000"
#     response = requests.get(url)
#     assert response.status_code == 200


# def test_get_block_by_hash(get_rest):
#     r = get_rest('blocks/hash/ee0077a8bb433897ca7e00b52e0bdb461cf4c356ec817cd47a6570aa172b37dc')
#     assert r.status_code == 200


# def test_get_block_by_hash():
#     url = (
#             settings.SERVER_HOST
#             + "blocks/hash/ee0077a8bb433897ca7e00b52e0bdb461cf4c356ec817cd47a6570aa172b37dc"
#     )
#     response = requests.get(url)
#     assert response.status_code == 200


# def test_get_events_by_tx(get_rest):
#     r = get_rest('events/tx_hash/0xd007cf25e28a98066f27a6ea113e41c34a3deaf91a1e17456949714997f9e642')
#     assert r.status_code == 200


# def test_get_events_by_tx():
#     url = (
#             settings.SERVER_HOST
#             + "events/tx_hash/0xd007cf25e28a98066f27a6ea113e41c34a3deaf91a1e17456949714997f9e642"
#     )
#     response = requests.get(url)
#     assert response.status_code == 200


def test_get_events_latest_block(get_rest):
    r = get_rest('events/block')
    assert r.status_code == 200


# def test_get_events_latest_block():
#     url = settings.SERVER_HOST + "events/block"
#     response = requests.get(url)
#     assert response.status_code == 200


# def test_get_events_by_height(get_rest):
#     r = get_rest('tx/block/10000000')
#     assert r.status_code == 200


# def test_get_events_by_height():
#     url = settings.SERVER_HOST + "tx/block/10000000"
#     response = requests.get(url)
#     assert response.status_code == 200


# def test_get_tx_by_hash(get_rest):
#     r = get_rest('tx/hash/0xd007cf25e28a98066f27a6ea113e41c34a3deaf91a1e17456949714997f9e642')
#     assert r.status_code == 200


# def test_get_tx_by_hash():
#     url = (
#             settings.SERVER_HOST
#             + "tx/hash/0xd007cf25e28a98066f27a6ea113e41c34a3deaf91a1e17456949714997f9e642"
#     )
#     response = requests.get(url)
#     assert response.status_code == 200


def test_get_txs_latest_block(get_rest):
    r = get_rest('tx/block')
    assert r.status_code == 200


# def test_get_txs_latest_block():
#     url = settings.SERVER_HOST + "tx/block"
#     response = requests.get(url)
#     assert response.status_code == 200


# def test_get_txs_by_height(get_rest):
#     r = get_rest('tx/block/10000000')
#     assert r.status_code == 200


# def test_get_txs_by_height():
#     url = settings.SERVER_HOST + "tx/block/10000000"
#     response = requests.get(url)
#     assert response.status_code == 200

