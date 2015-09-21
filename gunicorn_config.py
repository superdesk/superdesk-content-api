# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2014, 2015 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license

import os
import multiprocessing

bind = '0.0.0.0:%s' % os.environ.get('PORT', '5050')
bind = '0.0.0.0:5050'
workers = multiprocessing.cpu_count()

accesslog = '-'
access_log_format = '%(r)s\nstatus=%(s)s time=%(T)ss bytes=%(b)s pid=%(p)s remote=%(h)s referer=%(f)s'

reload = 'SUPERDESK_CONTENT_API_RELOAD' in os.environ
