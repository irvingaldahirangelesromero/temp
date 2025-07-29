class CustomException(Exception):
    """Base class for other exceptions"""
    pass

class ValidationError(CustomException):
    """Raised when there is a validation error"""
    def __init__(self, errors):
        self.errors = errors
        super().__init__(self._format_errors())

    def _format_errors(self):
        return f"Validation Error: {self.errors}"

class DatabaseConnectionError(CustomException):
    """Raised when there is a database connection error"""
    def __init__(self, db_type, message="Failed to connect to the database"):
        self.db_type = db_type
        self.message = message
        super().__init__(self._format_message())

    def _format_message(self):
        return f"{self.message} ({self.db_type})"

class AWSSecretsManagerError(CustomException):
    """Raised when there is an error with AWS Secrets Manager"""
    def __init__(self, secret_name, message="Failed to retrieve secret"):
        self.secret_name = secret_name
        self.message = message
        super().__init__(self._format_message())

    def _format_message(self):
        return f"{self.message}: {self.secret_name}"

class PayloadValidationError(CustomException):
    """Raised when there is a payload validation error"""
    def __init__(self, errors):
        self.errors = errors
        super().__init__(self._format_errors())

    def _format_errors(self):
        return f"Payload Validation Error: {self.errors}"

class NotFoundError(CustomException):
    """Raised when a requested resource is not found"""
    def __init__(self, resource, message="Resource not found"):
        self.resource = resource
        self.message = message
        super().__init__(self._format_message())

    def _format_message(self):
        return f"{self.message}: {self.resource}"

class UnauthorizedError(CustomException):
    """Raised when a user is not authorized to perform an action"""
    def __init__(self, action, message="Unauthorized action"):
        self.action = action
        self.message = message
        super().__init__(self._format_message())

    def _format_message(self):
        return f"{self.message}: {self.action}"

class ConflictError(CustomException):
    """Raised when there is a conflict in the request"""
    def __init__(self, conflict, message="Conflict error"):
        self.conflict = conflict
        self.message = message
        super().__init__(self._format_message())

    def _format_message(self):
        return f"{self.message}: {self.conflict}"

class InternalServerError(CustomException):
    """Raised when there is an internal server error"""
    def __init__(self, message="Internal server error"):
        self.message = message
        super().__init__(self.message)
