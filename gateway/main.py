from fastapi import FastAPI, Request, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()


origins = [
    "http://localhost:3000",
    "http://localhost:8080"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH", "DELETE"],
    allow_headers=["*"],
)


SERVICE_URLS = {
    "user": "http://user_service:8000/api/users",
    "chat": "http://chat_service:8000/api/chat",
    "gpt": "http://custom_gpt_service:8000/api/custom_gpt"
}


@app.api_route("/api/{service_name}/{path:path}", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
async def proxy_request(service_name: str, path: str, request: Request):
    if service_name not in SERVICE_URLS:
        raise HTTPException(status_code=404, detail="Service not found")

    service_url = SERVICE_URLS[service_name]
    url = f"{service_url}/{path}"

    headers = dict(request.headers)

    # Handling data for POST/PUT/PATCH requests
    try:
        json_data = await request.json() if request.method in ["POST", "PUT", "PATCH"] else None
    except Exception:
        json_data = None

    try:
        response = requests.request(
            method=request.method,
            url=url,
            headers=headers,
            json=json_data
        )
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))

    # Remove 'Content-Length' if present, let FastAPI handle it
    headers = {k: v for k, v in response.headers.items() if k.lower() != 'content-length'}

    # Return the response as a FastAPI Response
    return Response(
        content=response.content,
        status_code=response.status_code,
        headers=headers,
        media_type=response.headers.get('content-type')
    )
