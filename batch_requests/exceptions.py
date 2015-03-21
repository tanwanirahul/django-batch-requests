'''
Created on Dec 30, 2014

@author: Rahul Tanwani

@summary: Holds exception required for batch_requests app.
'''


class BadBatchRequest(Exception):
    '''
        Raised when client sends an invalid batch request.
    '''
    def __init__(self, *args, **kwargs):
        '''
            Initialize.
        '''
        Exception.__init__(self, *args, **kwargs)
