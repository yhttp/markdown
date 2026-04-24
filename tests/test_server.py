from bddrest import status, response, when

from yhttp.markdown import __version__


def test_server_info(ymdapp, ymdserver):
    ymdapp.ready()
    with ymdserver(verb='info'):
        assert status == 200
        assert response.json == dict(
            version=__version__,
            debug=True,
        )


# def test_server_index(ymdapp, ymdserver, mktmptree):
#     root = mktmptree({
#         'index.md': '# bar index',
#     })
#
#     ymdapp.settings.root = root
#     ymdapp.ready()
#     with ymdserver(path='/index.md'):
#         assert status == 200
#         assert response.text.startswith('<!DOCTYPE html>')
#
#
# def test_server_css(ymdapp, ymdserver):
#     ymdapp.ready()
#     with ymdserver(path='/index.css'):
#         assert status == 200
#         assert response.text.startswith('/* yhttp-markdown css */')
#
#
# def test_server_exclude(ymdapp, ymdserver, mktmptree):
#     root = mktmptree({
#         'index.md': '# index',
#         'foo.md': '# foo',
#         'bar': {
#             'index.md': '# bar index'
#         }
#     })
#
#     ymdapp.settings.merge(f'''
#     root: {root}
#     exclude:
#       - foo\\.md
#       - bar/?.*
#     ''')
#
#     ymdapp.ready()
#     with ymdserver():
#         assert status == 200
#         assert response.text.startswith('<!DOCTYPE html>')
#
#         when(path='/index.md')
#         assert status == 200
#
#         when(path='/foo.md')
#         assert status == 404
#
#         when(path='/bar')
#         assert status == 404
#
#         when(path='/bar/index.md')
#         assert status == 404
#
#     ymdapp.settings.merge('''
#     root: .
#     exclude: []
#     ''')
#
#
# def test_server_webmanifest(ymdapp, ymdserver):
#     ymdapp.ready()
#     with ymdserver('/webmanifest.json'):
#         assert status == 200
#         assert response.json == {
#             'icons': [
#                 {
#                     'sizes': '192x192',
#                     'src': '/.ymdmetadata/android-chrome-192x192.png',
#                     'type': 'image/png',
#                 },
#                 {
#                     'sizes': '512x512',
#                     'src': '/.ymdmetadata/android-chrome-512x512.png',
#                     'type': 'image/png',
#                 },
#             ],
#         }
#
#
# def test_server_notfound(ymdapp, ymdserver, mktmptree):
#     root = mktmptree({
#         'index.md': '# index',
#     })
#     ymdapp.settings.root = root
#     ymdapp.ready()
#     with ymdserver():
#         assert status == 200
#
#         when(path='/bar.md')
#         assert status == 404
#
#
# def test_server_unauthorized(ymdapp, ymdserver, mktmptree):
#     root = mktmptree({
#         'index.md': '# index',
#     })
#     ymdapp.settings.root = root
#     ymdapp.ready()
#     with ymdserver('/../foo'):
#         assert status == 403
