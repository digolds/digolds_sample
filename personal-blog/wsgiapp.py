#!/usr/bin/env python

__author__ = 'SLZ'

'''
digwebs framework demo.
'''

import logging
logging.basicConfig(level=logging.INFO)

from digwebs.web import get_app
import os
dir_path = os.path.dirname(os.path.realpath(__file__))
digwebs_app = get_app({'root_path':dir_path})
digwebs_app.init_all()
if __name__ == '__main__':
    import os
    os.environ['TABLE_NAME'] = 'personal-articles-table'
    os.environ['INDEX_NAME'] = 'ContentGlobalIndex'

    os.environ['USER_NAME'] = 'slz'
    os.environ['PASSWORD'] = 'abc'
    digwebs_app.run(9999, host='0.0.0.0')
else:
    wsgi_app = digwebs_app.get_wsgi_application()
