# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2014 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license

import json
import os

from content_api.auth import get_auth_url
from content_api.behave_setup import setup, set_placeholder
from superdesk import get_resource_service


def before_all(context):
    setup(context)
    os.environ['BEHAVE_TESTING'] = '1'


def before_feature(context, feature):
    pass


def before_scenario(context, scenario):
    config = {}
    if scenario.status != 'skipped' and 'notesting' in scenario.tags:
        config['SUPERDESK_TESTING'] = False

    setup(context, config)
    context.headers = [
        ('Content-Type', 'application/json'),
        ('Origin', 'localhost')
    ]

    if scenario.status != 'skipped' and 'auth' in scenario.tags:
        setup_auth_user(context)


def after_scenario(context, scenario):
    pass


test_user = {
    'username': 'test_user',
    'password': 'test_password'
}


test_client = {
    'name': 'test client',
    'client_type': 'subscriber'
}


def setup_auth_user(context, user=None, client=None):
    """
    Setup the user for the DB authentication.
    :param context: test context
    :param dict user: user
    """
    user = user or test_user
    client = client or test_client
    with context.app.test_request_context(context.app.config['URL_PREFIX']):
        original_password = user['password']

        if not get_resource_service('users').find_one(username=user['username'], req=None):
            get_resource_service('users').post([user])
        user['password'] = original_password

        db_client = get_resource_service('clients').find_one(name=client['name'], req=None)
        if not db_client:
            get_resource_service('clients').post([client])
            db_client = get_resource_service('clients').find_one(name=client['name'], req=None)

        auth_data = {'username': user['username'], 'password': user['password'],
                     'grant_type': 'password', 'client_id': str(db_client['_id'])}
        headers = [('Content-Type', 'application/x-www-form-urlencoded')]
        auth_response = context.client.post(get_auth_url(context.app),
                                            data=auth_data, headers=headers)

        auth_response_str = auth_response.get_data().decode('utf-8')
        token = json.loads(auth_response_str).get('access_token').encode('utf-8')
        context.headers.append(('Authorization', b'basic ' + token))
        context.user = user
        set_placeholder(context, 'CONTEXT_USER_ID', str(user.get('_id')))
