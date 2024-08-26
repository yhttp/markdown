import types
import functools

import markdown2


extras = [
    'header-ids',
]


markdowner = markdown2.Markdown(extras=extras)


def markdown2html(if_contenttype='text/markdown', cssfiles=None):
    def decorator(handler):
        @functools.wraps(handler)
        def wrapper(req, *args, **kwargs):
            resp = req.response
            chunks = []
            firstchunk = None

            # execute the inner handler
            body = handler(req, *args, **kwargs)

            if isinstance(body, types.GeneratorType):
                # Get the first chunk to for execute the handler
                firstchunk = next(body)

            if if_contenttype and resp.type != if_contenttype:
                # ignore converting to html
                if firstchunk is not None:
                    yield firstchunk
                    yield from body
                else:
                    yield body

            else:
                # Convert and serve the html
                resp.type = 'text/html'
                if firstchunk is not None:
                    chunks.append(markdowner.convert(firstchunk).encode())
                    for chunk in body:
                        chunks.append(markdowner.convert(chunk).encode())
                else:
                    chunks.append(markdowner.convert(body).encode())

                resp.length = sum(len(c) for c in chunks)
                for chunk in chunks:
                    yield chunk

        return wrapper

    return decorator
