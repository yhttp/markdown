import time

import pytest
import requests

from .conftest import GITHUBACTIONS


@pytest.mark.skipif(
    GITHUBACTIONS,
    reason='no way of testing this by GH currently, due the Github actions bug'
)
def test_cli_serve(cliapp, freetcpport, mktmptree):
    root = mktmptree({
        'bar': {
            'index.md': '# bar index',
        },
        'index.md': '# index',
        'index.html': '<h1>index</h1>',
    })

    with cliapp(f'-C {root} serve --bind {freetcpport}', nowait=True) as s:
        url = f'http://localhost:{freetcpport}'
        time.sleep(2)
        r = requests.get(url)
        assert r.text.startswith('<!DOCTYPE html>')

        r = requests.get(f'{url}/index.html')
        assert r.text.startswith('<!DOCTYPE html>')

        s.kill()


if __name__ == '__main__':
    from yhttp.markdown.main import Main
    Main.quickstart(['serve'])
