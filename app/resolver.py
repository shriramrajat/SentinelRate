from fastapi import Request

class IdentifierResolver:
    @staticmethod
    def resolve_identity(request: Request):
        """
        Returns a tuple: (identifier, is_authenticated)
        """
        # 1. Check for Authorization Header
        auth_header = request.headers.get("Authorization")
        
        if auth_header and auth_header.startswith("Bearer "):
            # In a real app, you would decode the JWT here.
            # For this demo, we assume the token IS the user_id.
            token = auth_header.split(" ")[1]
            return f"user:{token}", True
            
        # 2. Fallback to IP
        client_ip = request.client.host if request.client else "unknown"
        return f"ip:{client_ip}", False