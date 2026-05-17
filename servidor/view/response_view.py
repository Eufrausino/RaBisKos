class ResponseView:
    @staticmethod
    def success(response_type: str, data: dict = None) -> dict:
        if data is None:
            data = {}
        return {
            "type": response_type,
            "status": "ok",
            "data": data
        }

    @staticmethod
    def error(code: str, message: str = "") -> dict:
        return {
            "type": "ERROR",
            "status": "error",
            "code": code,
            "message": message
        }

    @staticmethod
    def event(event_type: str, data: dict) -> dict:
        return {
            "type": event_type,
            "data": data
        }