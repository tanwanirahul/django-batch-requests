'''
@author: rahul
'''
import json

from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View


class SimpleView(View):

    '''
        A simple view with dummy implementation for all the methods.
        The view is only intended to be used for testing.
    '''

    def get(self, request):
        '''
            Handles GET requests.
        '''
        return HttpResponse("Success!")

    def post(self, request):
        '''
            Handles POST requests.
            This implementation just echos back the data coming in.
        '''
        return HttpResponse(status=201, content=request.body)

    def put(self, request):
        '''
            Handles PUT requests
        '''
        # Imaginary current view of data.
        data = {"method": "PUT", "status": 202, "text": "Updated"}
        data.update(json.loads(request.body))
        return HttpResponse(status=202, content=json.dumps(data))

    def patch(self, request):
        '''
            Handles PATCH requests
        '''
        # Imaginary current view of data.
        data = {"method": "PUT", "status": 202, "text": "Updated"}
        data.update(json.loads(request.body))
        return HttpResponse(status=202, content=json.dumps(data))

    def delete(self, request):
        '''
            Handles delete requests
        '''
        return HttpResponse(status=202, content="No Content!")

    def head(self, request):
        '''
            Handles head requests.
        '''
        return HttpResponse()

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        '''
            Overiding to exempt csrf.
        '''
        return super(SimpleView, self).dispatch(*args, **kwargs)


class EchoHeaderView(View):

    '''
        Echos back the header value.
    '''

    def get(self, request, *args, **kwargs):
        '''
            Handles the get request.
        '''
        # Lookup for the header client is requesting for.
        header = request.GET.get("header", None)

        # Get the value for the associated header.
        value = getattr(request, header, None)

        # If header is not an attribute of request, look into request.META
        if value is None:
            value = request.META.get(header, None)

        return HttpResponse(value)

    def post(self, request, *args, **kwargs):
        '''
            Delegates to the get request.
        '''
        return self.get(request, *args, **kwargs)


class ExceptionView(View):

    '''
        Views that raises exception for testing purpose.
    '''

    def get(self, request, *args, **kwargs):
        '''
            Handles the get request.
        '''
        raise Exception("exception")
