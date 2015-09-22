# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2014, 2015 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license

"""
A module that runs the Superdesk public API.
"""

import logging
from content_api.app import get_app


logger = logging.getLogger('superdesk')


if __name__ == '__main__':
    app = get_app()
    app.run(
        host='0.0.0.0',
        port=5050,   # XXX: have PUBAPI_PORT in config... and other things
        debug=True,  # TODO: remove before pushing to production (+ have in cfg)
        use_reloader=True
    )
