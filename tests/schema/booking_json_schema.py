BOOKING_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": [
        "bookingid",
        "booking"
    ],
    "properties": {
        "bookingid": {
            "type": "integer",
            "minimum": 1
        },
        "booking": {
            "type": "object",
            "additionalProperties": False,
            "required": [
                "firstname",
                "lastname",
                "totalprice",
                "depositpaid",
                "bookingdates",
                "additionalneeds"
            ],
            "properties": {
                "firstname": {
                    "type": "string"
                },
                "lastname": {
                    "type": "string"
                },
                "totalprice": {
                    "type": "number"
                },
                "depositpaid": {
                    "type": "boolean"
                },
                "bookingdates": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": [
                        "checkin",
                        "checkout"
                    ],
                    "properties": {
                        "checkin": {
                            "type": "string",
                            "format": "string"
                        },
                        "checkout": {
                            "type": "string",
                            "format": "string"
                        }
                    }
                },
                "additionalneeds": {
                    "type": "string"
                }
            }
        }
    }
}
