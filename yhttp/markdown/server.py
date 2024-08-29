import os
from wsgiref.simple_server import make_server

import easycli
import sass as libsass
from mako.lookup import TemplateLookup
import yhttp.core as y

from . import __version__, toc
from .settings import settings
from .markdown import markdowner


here = os.path.dirname(__file__)
app = y.Application(version=__version__)


app.staticdirectory(
    '/static/',
    os.path.join(here, 'static/'),
    default=False,
    autoindex=False,
)


@app.when
def ready(app):
    if 'yhttp' in settings:
        app.settings.merge(settings.server)

    app.loopkup = TemplateLookup(
        directories=[here],
        cache_enabled=not settings.yhttp.debug,
    )


def sasscompile(s):
    return libsass.compile(
        indented=True,
        string=s,
        include_paths=[os.path.join(here, 'styles')],
        source_comments=False,
    )


sass = y.utf8('text/css', dump=sasscompile)


# TODO: cache
@app.route('/index.css')
@sass
def get(req, path=None):
    with open(os.path.join(here, 'styles/index.sass')) as f:
        return f.read()


@app.route('/(.*)')
@y.html
def get(req, path=None):
    # FIXME: (security) prevent to get parent directories
    targetpath = os.path.join(settings.server.root, path or '')
    targetfile = None

    # Default document
    default = settings.server.default_document
    if os.path.isdir(targetpath):
        if default:
            default = os.path.join(targetpath, default)
            if os.path.isfile(default):
                targetfile = default

    else:
        targetfile = targetpath
        targetpath = os.path.dirname(targetpath)

    # Fallback
    if not targetfile or not os.path.isfile(targetfile):
        fallback = settings.server.fallback_document
        if fallback:
            fallback = os.path.join(settings.server.root, fallback)
            if os.path.exists(fallback):
                targetfile = fallback

    # 404 not found
    if not targetfile or not os.path.isfile(targetfile):
        if not os.path.isdir(targetpath):
            raise y.statuses.notfound()

        targetfile = None

    # Generate TOC
    toc_ = toc.extractdir(targetpath, '', settings.toc.depth)
    t = app.loopkup.get_template('master.mako')

    if not targetfile:
        return t.render(
            title=settings.server.title,
            toc=toc_,
            content='',
        )
        return

    with open(targetfile) as f:
        return t.render(
            title=settings.server.title,
            toc=toc,
            content=markdowner.convert(f.read()),
        )


# app.route('/(.*)')(
#     markdown2html(cssfiles=['main.css'])(
#         y.static.directory(
#             rootpath=os.curdir,
#             default='index.md',
#             autoindex=True,
#             fallback=False
#         )
#     )
# )


DEFAULT_ADDRESS = '8080'


class Serve(easycli.SubCommand):
    __command__ = 'serve'
    __aliases__ = ['s']
    __arguments__ = [
        easycli.Argument(
            '-b', '--bind',
            default=DEFAULT_ADDRESS,
            metavar='{HOST:}PORT',
            help='Bind Address. default: %s' % DEFAULT_ADDRESS
        ),
    ]

    def __call__(self, args):  # pragma: no cover
        """the no cover pragma was set, because the coverae meassurement in
        subprocess is so complicated, but this function is covered by
        test_builtincli.py.
        """
        host, port = args.bind.split(':')\
            if ':' in args.bind else ('localhost', args.bind)

        app.ready()
        httpd = make_server(host, int(port), app)
        print(f'Markdown server started at http://{host}:{port}')
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("CTRL+C pressed.")
            app.shutdown()
