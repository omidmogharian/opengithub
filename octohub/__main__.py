#!/usr/bin/env python
# Copyright (c) 2013 Alon Swartz <alon@turnkeylinux.org>
#
# This file is part of OctoHub.
#
# OctoHub is free software; you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation; either version 3 of the License, or (at your option) any later
# version.
from __future__ import print_function

"""
OctoHub: GitHub API CLI

Arguments:
    method              Request HTTP method (e.g., GET, POST, DELETE, ...)
    uri                 Request URI (e.g., /user/issues)
    key=val             Request params key=value pairs (e.g., filter=assigned)

Options:
    --input <file>      Path to json encoded file for data (- for stdin)
    --max-pages <int>   Maximum pagination calls (only GET method supported)
                        For all pages, specify 0

Environment:
    OCTOHUB_TOKEN       GitHub personal access token
    OCTOHUB_LOGLEVEL    Log level debugging sent to stderr

Example usage:
    octohub GET /users/:user
    octohub GET /user/issues filter=assigned labels=bug
    octohub GET /repos/:owner/:repo/issues
    octohub GET /repos/:owner/:repo/issues sort=updated --max-pages=3
    octohub POST /repos/:owner/:repo/issues --input=issue.json
    octohub POST /user/repos --input=repo.json
    cat repo.json | octohub POST /orgs/:org/repos --input=-

http://developer.github.com/v3/
"""

import os
import sys
import getopt
try:
    import simplejson as json
except ImportError:
    import json

from octohub.connection import Connection, Pager
from octohub.exceptions import ResponseError

def fatal(e):
    print('Error: ' + str(e), file=sys.stderr)
    sys.exit(1)

def usage(e=None):
    if e:
        print('Error: ' + str(e), file=sys.stderr)

    cmd = os.path.basename(sys.argv[0])
    print('Syntax: %s method uri [arg=val...]' % cmd, file=sys.stderr)
    print(__doc__.strip(), file=sys.stderr)

    sys.exit(1)

def main():
    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], 'h',
                                       ['help', 'input=', 'max-pages='])
    except getopt.GetoptError as e:
        usage(e)

    data = None
    max_pages = None
    for opt, val in opts:
        if opt in ('-h', '--help'):
            usage()

        elif opt == '--input':
            if val == '-':
                data = sys.stdin
            else:
                data = file(val, 'r')

        elif opt == '--max-pages':
            max_pages = int(val)

    if len(args) == 0:
        usage()

    if len(args) < 2:
        usage('incorrect number of arguments')

    method = args[0]
    uri = args[1]

    if max_pages is not None and method != 'GET':
        fatal('--max-pages is only supported with method GET')

    params = {}
    for arg in args[2:]:
        key, val = arg.split('=')
        params[key] = val

    token = os.environ.get('OCTOHUB_TOKEN', None)
    conn = Connection(token)

    try:
        if max_pages is None:
            response = conn.send(method, uri, params, data)
            print(json.dumps(response.parsed, indent=1))
        else:
            parsed = []
            pager = Pager(conn, uri, params, max_pages=max_pages)
            for response in pager:
                parsed.extend(response.parsed)
            print(json.dumps(parsed, indent=1), end=' ')
    except ResponseError as e:
        fatal(e)

if __name__ == '__main__':
   main()
