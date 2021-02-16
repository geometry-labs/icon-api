
def test_get_events_by_tx(get_rest):
    r = get_rest('events/tx_hash/0xd007cf25e28a98066f27a6ea113e41c34a3deaf91a1e17456949714997f9e642')
    assert r.status_code == 200

# def test_get_events_by_tx():
#     url = (
#         settings.SERVER_HOST
#         + "events/tx_hash/0xd007cf25e28a98066f27a6ea113e41c34a3deaf91a1e17456949714997f9e642"
#     )
#
#     response = requests.get(url)
#     assert response.status_code == 200


def test_get_events_latest_block(get_rest):
    r = get_rest('events/block')
    assert r.status_code == 200


# def test_get_events_latest_block():
#     url = settings.SERVER_HOST + "events/block"
#
#     response = requests.get(url)
#     assert response.status_code == 200


def test_get_events_by_height(get_rest):
    r = get_rest('tx/block/10000000')
    assert r.status_code == 200


# def test_get_events_by_height():
#     url = settings.SERVER_HOST + "tx/block/10000000"
#
#     response = requests.get(url)
#     assert response.status_code == 200
