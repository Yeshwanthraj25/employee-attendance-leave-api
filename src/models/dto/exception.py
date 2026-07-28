class AppException(Exception):
    def __init__(self, file_name: str, function_name: str, status_code: int, 
                 error_details: str, log_data: str):
        self.file_name = file_name
        self.function_name = function_name
        self.status_code = status_code
        self.error_details = error_details
        self.log_data = log_data