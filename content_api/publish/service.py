# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2014 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license

import logging

from eve.utils import config

from superdesk.services import BaseService


logger = logging.getLogger(__name__)


class PublishService(BaseService):
    """
    A service for publishing to the content api.

    Serves mainly as a proxy to the data layer.
    """
    def create(self, docs, **kwargs):
        ids = []
        for doc in docs:
            doc[config.ID_FIELD] = doc['guid']
            del doc['guid']
            _id = doc[config.ID_FIELD]
            original = self.find_one(req=None, _id=_id)
            if original:
                self.update(_id, doc, original)
                ids.append(_id)
            else:
                ids.extend(super().create([doc], **kwargs))
        return ids
