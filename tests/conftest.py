import os
import functools

import bddcli
import bddrest
import pytest
import yhttp.core as y


GITHUBACTIONS = 'CI' in os.environ and os.environ['CI'] \
    and 'GITHUB_RUN_ID' in os.environ


@pytest.fixture
def cliapp():
    cliapp = bddcli.Application(
        'yhttp-markdown',
        'yhttp.markdown.server:app.climain'
    )
    return functools.partial(bddcli.Given, cliapp)


@pytest.fixture
def yapp():
    from yhttp.markdown import __version__

    return y.Application(__version__, 'yhttp-markdown')


@pytest.fixture
def yserver(yapp):
    yield functools.partial(bddrest.Given, yapp)


@pytest.fixture
def ymdapp():
    from yhttp.markdown.server import app

    app.settings.debug = True
    yield app
    app.shutdown()


@pytest.fixture
def ymdserver(ymdapp):
    yield functools.partial(bddrest.Given, ymdapp)
