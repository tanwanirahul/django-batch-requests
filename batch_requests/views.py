'''
@author: Rahul Tanwani

@summary: A module to perform batch request processing.
'''

import json

from django.core.urlresolvers import resolve
from django.http.response import HttpResponse, HttpResponseBadRequest,\
    HttpResponseServerError
from django.template.response import ContentNotRenderedError
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from batch_requests.exceptions import BadBatchRequest
from batch_requests.settings import br_settings as _settings
from batch_requests.utils import get_wsgi_request_object


def get_response(wsgi_request):
    '''
        Given a WSGI request, makes a call to a corresponding view
        function and returns the response.
    '''
    # Get the view / handler for this request
    view, args, kwargs = resolve(wsgi_request.path_info)

    kwargs.update({"request": wsgi_request})

    # Let the view do his task.
    try:
        resp = view(*args, **kwargs)
    except Exception as exc:
        resp = HttpResponseServerError(content=exc.message)

    headers = dict(resp._headers.values())
    # Convert HTTP response into simple dict type.
    d_resp = {"status_code": resp.status_code, "reason_phrase": resp.reason_phrase,
              "headers": headers}
    try:
        d_resp.update({"body": resp.content})
    except ContentNotRenderedError:
        resp.render()
        d_resp.update({"body": resp.content})

    return d_resp


def get_wsgi_requests(request):
    '''
        For the given batch request, extract the individual requests and create
        WSGIRequest object for each.
    '''
    valid_http_methods = ["get", "post", "put", "patch", "delete", "head", "options", "connect", "trace"]
    requests = json.loads(request.body)

    if type(requests) not in (list, tuple):
        raise BadBatchRequest("The body of batch request should always be list!")

    # Max limit check.
    no_requests = len(requests)

    if no_requests > _settings.MAX_LIMIT:
        raise BadBatchRequest("You can batch maximum of %d requests." % (_settings.MAX_LIMIT))

    # We could mutate the current request with the respective parameters, but mutation is ghost in the dark,
    # so lets avoid. Construct the new WSGI request object for each request.

    def construct_wsgi_from_data(data):
        '''
            Given the data in the format of url, method, body and headers, construct a new
            WSGIRequest object.
        '''
        url = data.get("url", None)
        method = data.get("method", None)

        if url is None or method is None:
            raise BadBatchRequest("Request definition should have url, method defined.")

        if method.lower() not in valid_http_methods:
            raise BadBatchRequest("Invalid request method.")

        body = data.get("body", "")
        headers = data.get("headers", {})
        return get_wsgi_request_object(request, method, url, headers, body)

    return [construct_wsgi_from_data(data) for data in requests]


@csrf_exempt
@require_http_methods(["POST"])
def handle_batch_requests(request, *args, **kwargs):
    '''
        A view function to handle the overall processing of batch requests.
    '''
    try:
        # Get the Individual WSGI requests.
        wsgi_requests = get_wsgi_requests(request)
    except BadBatchRequest as brx:
        return HttpResponseBadRequest(content=brx.message)

    # Fire these WSGI requests, and collect the response for the same.
    response = [get_response(wsgi_request) for wsgi_request in wsgi_requests]

    # Evrything's done, return the response.
    return HttpResponse(
        content=json.dumps(response), content_type="application/json")
