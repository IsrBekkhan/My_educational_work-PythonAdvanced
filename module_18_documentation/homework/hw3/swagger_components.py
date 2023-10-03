calc_request = {
        "type": "object",
        "required": ["jsonrpc", "method", "params", "id"],
        "properties": {
            "jsonrpc": {
                "type": "string",
                "default": "2.0",
                "pattern": "2.0"
            },
            "method": {
                "type": "string",
                "enum": ["calc.add", "calc.sub", "calc.mul", "calc.div"]
            },
            "params": {
                "type": "object",
                "required": ["a", "b"],
                "properties": {
                    "a": {"type": "number"},
                    "b": {"type": "number"}
                }
            },
            "id": {"type": "string"}
        }
    }

calc_response = {
        "type": "object",
        "required": ["jsonrpc", "id"],
        "properties": {
            "jsonrpc": {
                "type": "string",
                "default": "2.0",
                "pattern": "2.0"
            },
            "result": {"type": "number"},
            "error": {
                "type": "object",
                "required": ["code", "message", "data"],
                "properties": {
                    "code": {"type": "integer"},
                    "message": {"type": "string"},
                    "data": {"type": "object"}
                }
            },
            "id": {"type": "string"}
        }
    }

base_method_doc = {
    "summary": "Calculate",
    "parameters":
        [
            {
                "name": "request",
                "in": "body",
                "required": True,
                "schema": {
                    "$ref": "#/definitions/CalcRequest"
                }
            }
        ],
    "responses": {
        "200": {
            "description": "Success",
            "schema": {
                "$ref": "#/definitions/CalcResponse"
            }
        },
        "400": {
            "description": "Bad Request",
            "schema": {
                "$ref": "#/definitions/CalcResponse"
            }
        },
        "500": {
            "description": "Internal Server Error",
            "schema": {
                "$ref": "#/definitions/CalcResponse"
            }
        }
    }
}