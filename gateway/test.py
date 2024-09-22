import httpx

# Define the URL of your login endpoint
LOGIN_URL = "http://localhost:8000/api/users/login/"

# Define the login payload (adjust fields as needed)
login_payload = {
    "username": "your_username",
    "password": "your_password"
}

async def login():
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(LOGIN_URL, json=None)
            response.raise_for_status()  # Raises an error for 4xx/5xx responses
            
            print("Login successful!")
            print("Response:", response.json())
        except httpx.HTTPStatusError as http_err:
            print(f"HTTP error occurred: {http_err}")
            print("Response:", http_err.response.text)
        except Exception as e:
            print(f"An error occurred: {e}")

# To run the login function
if __name__ == "__main__":
    import asyncio
    asyncio.run(login())
