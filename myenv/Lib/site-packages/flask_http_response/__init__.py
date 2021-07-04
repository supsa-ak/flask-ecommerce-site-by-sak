#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .main import CustomResponse, SuccessResponse, ErrorResponse, ResultResponse


success = CustomResponse().response(SuccessResponse('Successfully Completed', 200))
error = CustomResponse().response(ErrorResponse('Operation Faild', 400))
result = CustomResponse().response(ResultResponse({}, 200))