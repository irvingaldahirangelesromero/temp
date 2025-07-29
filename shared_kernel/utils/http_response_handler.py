import json
from typing import Any, Dict

class HTTPResponseHandler:
    @staticmethod
    def create_response(data: Any = None, status_code: int = 200, message: str = "Success", content_type: str = "application/json") -> Dict:
        body = json.dumps({"message": message, "data": data}) if content_type == "application/json" else data
        return {
            "statusCode": status_code,
            "headers": {
                "Content-Type": content_type
            },
            "body": body
        }

    @staticmethod
    def create_error_response(message: str, status_code: int = 400, content_type: str = "application/json") -> Dict:
        body = json.dumps({"message": message}) if content_type == "application/json" else message
        return {
            "statusCode": status_code,
            "headers": {
                "Content-Type": content_type
            },
            "body": body
        }

class JsonResponse(HTTPResponseHandler):
    @staticmethod
    def success(data: Any = None, status_code: int = 200, message: str = "Success") -> Dict:
        return HTTPResponseHandler.create_response(data, status_code, message, content_type="application/json")

    @staticmethod
    def error(message: str, status_code: int = 400) -> Dict:
        return HTTPResponseHandler.create_error_response(message, status_code, content_type="application/json")

class SoapResponse(HTTPResponseHandler):
    @staticmethod
    def success(data: str, status_code: int = 200, message: str = "Success") -> Dict:
        return HTTPResponseHandler.create_response(data, status_code, message, content_type="application/soap+xml")

    @staticmethod
    def error(message: str, status_code: int = 400) -> Dict:
        return HTTPResponseHandler.create_error_response(message, status_code, content_type="application/soap+xml")

class ExcelResponse(HTTPResponseHandler):
    @staticmethod
    def success(data: bytes, status_code: int = 200, message: str = "Success") -> Dict:
        return HTTPResponseHandler.create_response(data, status_code, message, content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    @staticmethod
    def error(message: str, status_code: int = 400) -> Dict:
        return HTTPResponseHandler.create_error_response(message, status_code, content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

class CsvResponse(HTTPResponseHandler):
    @staticmethod
    def success(data: str, status_code: int = 200, message: str = "Success") -> Dict:
        return HTTPResponseHandler.create_response(data, status_code, message, content_type="text/csv")

    @staticmethod
    def error(message: str, status_code: int = 400) -> Dict:
        return HTTPResponseHandler.create_error_response(message, status_code, content_type="text/csv")
