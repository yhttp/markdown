from yhttp.markdown import toc


def test_toc_extractdir(mktmptree):
    root = mktmptree({
        'bar': {
            'index.md': '# bar index',
        },
        '0-index.md': '# index',
        '1-foo.md': '## foo',
        '2-baz': '## baz',
        '.qux.md': '## qux',
    })

    headings, subdirs = toc.extractdir(root)
    assert subdirs == ['bar']
    assert headings == [
        {
            'href': '0-index.md#index',
            'level': 1,
            'title': 'index',
            'children': [
                {
                    'children': [],
                    'href': '1-foo.md#foo',
                    'level': 2,
                    'title': 'foo',
                },
            ],
        },
    ]


def test_toc_extract():
    doc = '''
    # Foo
    ## Bar
    ### Baz
    ## Qux
    # Quux
    '''

    out = toc.extract('foobarbaz.md', doc.splitlines())
    assert out == [
        {
            'href': 'foobarbaz.md#foo',
            'level': 1,
            'title': 'Foo',
            'children': [
                {
                    'href': 'foobarbaz.md#bar',
                    'level': 2,
                    'title': 'Bar',
                    'children': [
                        {
                            'href': 'foobarbaz.md#baz',
                            'level': 3,
                            'title': 'Baz',
                            'children': [],
                        },
                    ],
                },
                {
                    'href': 'foobarbaz.md#qux',
                    'level': 2,
                    'title': 'Qux',
                    'children': [],
                },
            ],
        },
        {
            'href': 'foobarbaz.md#quux',
            'level': 1,
            'title': 'Quux',
            'children': [],
        },
    ]


def test_toc_extract_depth():
    doc = '''
    # Foo
    ## Bar
    ### Baz
    '''

    out = toc.extract('foobarbaz.md', doc.splitlines(), depth=2)
    assert out == [
        {
            'href': 'foobarbaz.md#foo',
            'level': 1,
            'title': 'Foo',
            'children': [
                {
                    'href': 'foobarbaz.md#bar',
                    'level': 2,
                    'title': 'Bar',
                    'children': [],
                },
            ],
        },
    ]


def test_toc_extract_levelgap():
    doc = '''
    # Foo
    ### Baz
    '''

    out = toc.extract('foobarbaz.md', doc.splitlines())
    assert out == [
        {
            'children': [],
            'href': 'foobarbaz.md#foo',
            'level': 1,
            'title': 'Foo',
        },
    ]


def test_toc_extract_backwardgap():
    doc = '''
    # Foo
    ## Bar
    ### Baz
    # Quux
    '''

    out = toc.extract('foobarbaz.md', doc.splitlines())
    assert out == [
        {
            'href': 'foobarbaz.md#foo',
            'level': 1,
            'title': 'Foo',
            'children': [
                {
                    'href': 'foobarbaz.md#bar',
                    'level': 2,
                    'title': 'Bar',
                    'children': [
                        {
                            'href': 'foobarbaz.md#baz',
                            'level': 3,
                            'title': 'Baz',
                            'children': [],
                        },
                    ],
                },
            ],
        },
        {
            'href': 'foobarbaz.md#quux',
            'level': 1,
            'title': 'Quux',
            'children': [],
        },
    ]


def test_toc_extract_codeblocks():
    doc = '''
    # Foo
    ```
    # qux
    foobar foobaz
    ```
    ## Bar
    ### Baz
    # Quux
    '''

    out = toc.extract('foobarbaz.md', doc.splitlines())
    assert out == [
        {
            'href': 'foobarbaz.md#foo',
            'level': 1,
            'title': 'Foo',
            'children': [
                {
                    'href': 'foobarbaz.md#bar',
                    'level': 2,
                    'title': 'Bar',
                    'children': [
                        {
                            'href': 'foobarbaz.md#baz',
                            'level': 3,
                            'title': 'Baz',
                            'children': [],
                        },
                    ],
                },
            ],
        },
        {
            'href': 'foobarbaz.md#quux',
            'level': 1,
            'title': 'Quux',
            'children': [],
        },
    ]
