#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import jsonify

__version__ = "0.0.1.0"


class ResponseInterface(object):
    success = True

    def __init__(self, message, status):
        self.message = message
        self.status = status

    def return_response(self, message=None, status=None):

        if status:
            self.status = status
        if message:
            self.message = message

        obj = {
            "success": self.success,
            "message": self.message
        }

        reponse = jsonify(obj)
        reponse.status_code = self.status

        return reponse


class SuccessResponse(ResponseInterface):
    success = True


class ErrorResponse(ResponseInterface):
    success = False


class ResultResponse(ResponseInterface):

    def return_response(self, message={}, status=200):
        self.status = status
        self.message = message
        response = jsonify(self.message)
        response.status_code = self.status
        return response


class CustomResponse():

    def response(self, response_type):

        return response_type


if __name__ == "__main__":
    pass
