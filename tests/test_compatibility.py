'''
@author: Rahul Tanwani

@summary: Test cases to check compatibility between individual requests
          and batch requests.
'''
import json

from tests.test_base import TestBase


class TestCompatibility(TestBase):

    '''
        Tests compatibility.
    '''

    def test_compatibility_of_get_request(self):
        '''
            Make a GET request without the batch and in the batch and assert
            that both gives the same results.
        '''
        # Get the response for an individual request.
        inv_req = self.client.get("/views/")
        inv_resp = self.prepare_response(inv_req.status_code, inv_req.content, inv_req._headers)

        # Get the response for a batch request.
        batch_request = self.make_a_batch_request("GET", "/views/", "")
        batch_resp = json.loads(batch_request.content)[0]
        del batch_resp["reason_phrase"]

        # Assert both individual request response and batch response are equal.
        self.assert_reponse_compatible(inv_resp, batch_resp)

    def test_compatibility_of_post_request(self):
        '''
            Make a POST request without the batch and in the batch and assert
            that both gives the same results.
        '''
        data = json.dumps({"text": "hello"})

        # Get the response for an individual request.
        inv_req = self.client.post("/views/", data, content_type="text/plain")
        inv_resp = self.prepare_response(inv_req.status_code, inv_req.content, inv_req._headers)

        # Get the response for a batch request.
        batch_request = self.make_a_batch_request("POST", "/views/", data, {"content_type": "text/plain"})
        batch_resp = json.loads(batch_request.content)[0]
        del batch_resp["reason_phrase"]

        # Assert both individual request response and batch response are equal.
        self.assert_reponse_compatible(inv_resp, batch_resp)

    def test_compatibility_of_put_request(self):
        '''
            Make a PUT request without the batch and in the batch and assert
            that both gives the same results.
        '''
        data = json.dumps({"text": "hello"})

        # Get the response for an individual request.
        inv_req = self.client.patch("/views/", data, content_type="text/plain")
        inv_resp = self.prepare_response(inv_req.status_code, inv_req.content, inv_req._headers)

        # Get the response for a batch request.
        batch_request = self.make_a_batch_request("patch", "/views/", data, {"content_type": "text/plain"})
        batch_resp = json.loads(batch_request.content)[0]
        del batch_resp["reason_phrase"]

        # Assert both individual request response and batch response are equal.
        self.assert_reponse_compatible(inv_resp, batch_resp)

    def test_compatibility_of_patch_request(self):
        '''
            Make a POST request without the batch and in the batch and assert
            that both gives the same results.
        '''
        data = json.dumps({"text": "hello"})

        # Get the response for an individual request.
        inv_req = self.client.post("/views/", data, content_type="text/plain")
        inv_resp = self.prepare_response(inv_req.status_code, inv_req.content, inv_req._headers)

        # Get the response for a batch request.
        batch_request = self.make_a_batch_request("POST", "/views/", data, {"CONTENT_TYPE": "text/plain"})
        batch_resp = json.loads(batch_request.content)[0]
        del batch_resp["reason_phrase"]

        # Assert both individual request response and batch response are equal.
        self.assert_reponse_compatible(inv_resp, batch_resp)

    def test_compatibility_of_delete_request(self):
        '''
            Make a DELETE request without the batch and in the batch and assert
            that both gives the same results.
        '''
        # Get the response for an individual request.
        inv_req = self.client.delete("/views/")
        inv_resp = self.prepare_response(inv_req.status_code, inv_req.content, inv_req._headers)

        # Get the response for a batch request.
        batch_request = self.make_a_batch_request("delete", "/views/", "")
        batch_resp = json.loads(batch_request.content)[0]
        del batch_resp["reason_phrase"]

        # Assert both individual request response and batch response are equal.
        self.assert_reponse_compatible(inv_resp, batch_resp)

    def test_compatibility_of_multiple_requests(self):
        '''
            Make multiple requests without the batch and in the batch and
            assert that both gives the same results.
        '''

        data = json.dumps({"text": "Batch"})
        # Make GET, POST and PUT requests individually.

        # Get the response for an individual GET request.
        inv_req = self.client.get("/views/")
        inv_get = self.prepare_response(inv_req.status_code, inv_req.content, inv_req._headers)

        # Get the response for an individual POST request.
        inv_req = self.client.post("/views/", data, content_type="text/plain")
        inv_post = self.prepare_response(inv_req.status_code, inv_req.content, inv_req._headers)

        # Get the response for an individual PUT request.
        inv_req = self.client.patch("/views/", data, content_type="text/plain")
        inv_put = self.prepare_response(inv_req.status_code, inv_req.content, inv_req._headers)

        # Consolidate all the responses.
        indv_responses = [inv_get, inv_post, inv_put]

        # Make a batch call for GET, POST and PUT request.
        get_req = ("get", "/views/", '', {})
        post_req = ("post", "/views/", data, {"content_type": "text/plain"})
        put_req = ("put", "/views/", data, {"content_type": "text/plain"})

        # Get the response for a batch request.
        batch_requests = self.make_multiple_batch_request([get_req, post_req, put_req])
        batch_responses = json.loads(batch_requests.content)

        # Assert all the responses are compatible.
        for indv_resp, batch_resp in zip(indv_responses, batch_responses):
            del batch_resp["reason_phrase"]
            self.assert_reponse_compatible(indv_resp, batch_resp)
