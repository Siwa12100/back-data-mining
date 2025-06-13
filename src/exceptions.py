class APIException(Exception):
    code = 500
    message = 'internal-error'
    description = 'Internal server error'
    pass

class BadRequestJSONException(APIException):
    code = 400
    message = 'bad-request'
    description = 'Bad request. JSON expected.'
    pass

class EmptyRequestException(APIException):
    code = 400
    message = 'empty-request'
    description = 'Empty request provided.'
    pass

class EmptyDataProvidedException(APIException):
    def __init__(self, field=None):
        if field is not None:
            description = f'Empty data provided. Field {field} expected.'
        else:
            description = 'Empty data provided.'
        super().__init__(code=400, message='empty-request', description=description)

class InvalidBase64DataException(APIException):
    code=400,
    message='invalid-base64',
    description='file_data is not a valid base64-encoded string.'
    pass

class InvalidCSVException(APIException):
    code=400,
    message='invalid-csv',
    description='Decoded file_data is not a valid CSV file.'
    pass