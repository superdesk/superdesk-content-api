# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2015 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license

from flask import url_for, current_app as app


def url_for_media(media_id):
    try:
        url = app.media.url_for_media(media_id)
        if url:
            return url
        return url_for('assets_raw.get_media_streamed', media_id=media_id, _external=True)
    except AttributeError:
        return url_for('assets_raw.get_media_streamed', media_id=media_id, _external=True)
