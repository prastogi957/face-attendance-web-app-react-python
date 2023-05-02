from fastapi import FastAPI
from fastapi import Request, Response

app = FastAPI()

# Define a list of allowed IP addresses
ALLOWED_IPS = ['192.168.1.1', '192.168.1.2', '192.168.1.3']

@app.middleware("http")
async def restrict_access_to_allowed_ips(request: Request, call_next):
    # Get the client's IP address from the request
    client_ip = request.client.host

    # Check if the client's IP address is in the allowed list
    if client_ip not in ALLOWED_IPS:
        # Return a forbidden response with a custom message
        return Response(content="Forbidden", status_code=403)

    # Pass the request to the next middleware or route handler
    response = await call_next(request)

    return response

@app.get("/restricted")
async def restricted_route():
    # This route can only be accessed by clients with IP addresses in the allowed list
    return {"message": "Access granted"}

