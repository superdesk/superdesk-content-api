# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2014, 2015 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license

from re import findall
from os.path import basename
from urllib.parse import urlparse
from flask import json
from eve.methods.common import parse
from behave import given, when, then  # @UnresolvedImport
from wooper.expect import expect_status, expect_status_in, expect_json_contains
from wooper.general import fail_and_print_body
from wooper.assertions import assert_equal

from superdesk.tests import get_prefixed_url
from superdesk import get_resource_service
from content_api.behave_setup import get_fixture_path


def get_resource_name(url):
    parsed_url = urlparse(url)
    return basename(parsed_url.path)


def store_placeholder(context, url):
    if context.response.status_code in (200, 201):
        item = json.loads(context.response.get_data())
        if item['_status'] == 'OK' and item.get('_id'):
            setattr(context, get_resource_name(url), item)


def apply_placeholders(context, text):
    placeholders = getattr(context, 'placeholders', {})
    for placeholder in findall('#([^#"]+)#', text):
        if placeholder not in placeholders:
            try:
                resource_name, field_name = placeholder.lower().split('.', maxsplit=1)
            except:
                continue
            resource = getattr(context, resource_name, None)
            if resource and field_name in resource:
                value = str(resource[field_name])
            else:
                continue
        else:
            value = placeholders[placeholder]
        text = text.replace('#%s#' % placeholder, value)
    return text


def test_json(context):
    try:
        response_data = json.loads(context.response.get_data())
    except Exception:
        fail_and_print_body(context.response, 'response is not valid json')
    context_data = json.loads(apply_placeholders(context, context.text))
    assert_equal(json_match(context_data, response_data), True,
                 msg=str(context_data) + '\n != \n' + str(response_data))
    return response_data


def test_key_is_present(key, context, response):
    """Test if given key is present in response.

    In case the context value is empty - "", {}, [] - it checks if it's non empty in response.

    If it's set in context to false, it will check that it's falsy/empty in response too.

    :param key
    :param context
    :param response
    """
    assert not isinstance(context[key], bool) or not response[key], \
        '"%s" should be empty or false, but it was "%s" in (%s)' % (key, response[key], response)


def get_json_data(response):
    return json.loads(response.get_data())


def json_match(context_data, response_data):
    if isinstance(context_data, dict):
        assert isinstance(response_data, dict), 'response data is not dict, but %s' % type(response_data)
        for key in context_data:
            if key not in response_data:
                print(key, ' not in ', response_data)
                return False
            if context_data[key] == "__any_value__":
                test_key_is_present(key, context_data, response_data)
                continue
            if not json_match(context_data[key], response_data[key]):
                return False
        return True
    elif isinstance(context_data, list):
        for item_context in context_data:
            found = False
            for item_response in response_data:
                if json_match(item_context, item_response):
                    found = True
                    break
            if not found:
                print(item_context, ' not in ', response_data)
                return False
        return True
    elif not isinstance(context_data, dict):
        if context_data != response_data:
            print(context_data, ' != ', response_data)
        return context_data == response_data


def unique_headers(headers_to_add, old_headers):
    headers = dict(old_headers)
    for item in headers_to_add:
        headers.update({item[0]: item[1]})
    unique_headers = [(k, v) for k, v in headers.items()]
    return unique_headers


def post_data(context, url, success=False):
    with context.app.mail.record_messages() as outbox:
        data = apply_placeholders(context, context.text)
        url = apply_placeholders(context, url)
        context.response = context.client.post(get_prefixed_url(context.app, url),
                                               data=data, headers=context.headers)
        if success:
            assert_ok(context.response)

        item = json.loads(context.response.get_data())
        context.outbox = outbox
        store_placeholder(context, url)
        return item


def assert_ok(response):
    """Assert we get ok status within api response."""
    expect_status_in(response, (200, 201))
    expect_json_contains(response, {'_status': 'OK'})


def assert_200(response):
    """Assert we get status code 200."""
    expect_status_in(response, (200, 201, 204))


def is_user_resource(resource):
    return resource in ('users', '/users')


@given('empty "{resource}"')
def step_impl_given_empty(context, resource):
    if not is_user_resource(resource):
        with context.app.test_request_context(context.app.config['URL_PREFIX']):
            get_resource_service(resource).delete_action()


@given('"{resource}"')
def step_impl_given_(context, resource):
    data = apply_placeholders(context, context.text)
    with context.app.test_request_context(context.app.config['URL_PREFIX']):
        if not is_user_resource(resource):
            get_resource_service(resource).delete_action()

        items = [parse(item, resource) for item in json.loads(data)]
        if is_user_resource(resource):
            for item in items:
                item.setdefault('needs_activation', False)

        get_resource_service(resource).post(items)
        context.data = items
        context.resource = resource
        setattr(context, resource, items[-1])


@given('the "{resource}"')
def step_impl_given_the(context, resource):
    with context.app.test_request_context(context.app.config['URL_PREFIX']):
        if not is_user_resource(resource):
            get_resource_service(resource).delete_action()

        orig_items = {}
        items = [parse(item, resource) for item in json.loads(context.text)]
        get_resource_service(resource).post(items)
        context.data = orig_items or items
        context.resource = resource


@when('we get "{url}"')
def when_we_get_url(context, url):
    url = apply_placeholders(context, url).encode('ascii').decode('unicode-escape')
    headers = []
    if context.text:
        for line in context.text.split('\n'):
            key, val = line.split(': ')
            headers.append((key, val))
    headers = unique_headers(headers, context.headers)
    url = apply_placeholders(context, url)
    context.response = context.client.get(get_prefixed_url(context.app, url), headers=headers)


@when('we post to "{url}"')
def step_impl_when_post_url(context, url):
    post_data(context, url)


@then('we get existing resource')
def step_impl_then_get_existing(context):
    assert_200(context.response)
    test_json(context)


@then('we get list with {total_count} items')
def step_impl_then_get_list(context, total_count):
    assert_200(context.response)
    data = get_json_data(context.response)
    int_count = int(total_count.replace('+', ''))

    if '+' in total_count:
        assert int_count <= len(data['_items']), '%d items is not enough' % data['_meta']['total']
    else:
        assert int_count == len(data['_items']), 'got %d' % (data['_meta']['total'])
    if context.text:
        test_json(context)


@then('we get error {code}')
def step_impl_then_get_error(context, code):
    expect_status(context.response, int(code))
    if context.text:
        test_json(context)


@then('we get response code {code}')
def step_impl_then_get_code(context, code):
    assert context.response.status_code == int(code), \
        'got %d %s' % (context.response.status_code, context.response.get_data())
    expect_status(context.response, int(code))


@when('we upload a file "{file_name}" to "{destination}" with "{media_id}"')
def step_impl_when_upload_image_with_guid(context, file_name, destination, media_id):
    upload_file(context, destination, file_name, 'media', {'media_id': media_id})


def upload_file(context, dest, filename, file_field, extra_data=None, method='post', user_headers=[]):
    with open(get_fixture_path(filename), 'rb') as f:
        data = {file_field: f}
        if extra_data:
            data.update(extra_data)
        headers = [('Content-Type', 'multipart/form-data')]
        headers.extend(user_headers)
        headers = unique_headers(headers, context.headers)
        url = get_prefixed_url(context.app, dest)
        context.response = getattr(context.client, method)(url, data=data, headers=headers)
        assert_ok(context.response)
        store_placeholder(context, url)
