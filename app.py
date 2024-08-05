import hmac
import hashlib
import json
import yaml
from litestar import Litestar, post, Request
from litestar.exceptions import HTTPException

# Define your GitHub webhook secret
# Read the secret from a file
#with open('/secret/gh_wh_dingp_acme', 'r') as file:
#    GITHUB_SECRET = file.read().strip()

def verify_signature(payload: bytes, signature: str, secret: str) -> bool:
    """Verify GitHub webhook signature."""
    mac = hmac.new(secret.encode(), msg=payload, digestmod=hashlib.sha256)
    expected_signature = f'sha256={mac.hexdigest()}'
    return hmac.compare_digest(expected_signature, signature)


def parse_admission_file(file_path: str) -> dict:
    """Parse the admission.yaml file and convert it into a Python dictionary."""
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)
    return data


class APIEndpoint:
    def __init__(self, config: dict):
        self.config = config

    @post("/api/endpoint")
    async def handle_endpoint(self, request: Request) -> dict:
        """Handle API endpoint."""
        try:
            payload = await request.body()
            # Decode payload and parse JSON
            data = json.loads(payload.decode('utf-8'))
            print("Received payload:")
            print(json.dumps(data, indent=4))
            
            # Add your custom logic to handle the API endpoint payload
            # You can access the configuration parameters from self.config
            
            return {"status": "success"}
        except Exception as e:
            print(f"Error: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")

# Load the admission.yaml file
admission_data = parse_admission_file("/path/to/admission.yaml")

# Create an instance of the APIEndpoint class with the admission data
api_endpoint = APIEndpoint(admission_data)

# Add the API endpoint to the Litestar app
app.add_route(api_endpoint.handle_endpoint)


@post("/webhook")
async def github_webhook(request: Request) -> dict:
    """Handle GitHub webhook."""
    try:
        payload = await request.body()
        #signature = request.headers.get("X-Hub-Signature-256")
        
        #if not signature:
        #    raise HTTPException(status_code=400, detail="Missing signature header")
        
        #if not verify_signature(payload, signature, GITHUB_SECRET):
        #    raise HTTPException(status_code=400, detail="Invalid signature")

        # Decode payload and parse JSON
        data = json.loads(payload.decode('utf-8'))
        print("Received payload:")
        print(json.dumps(data, indent=4))

        if "action" in data and data["action"] == "queued":
            # Custom logic for handling the webhook payload when action is "queued"
            # Add your code here
            pass
        # Process the payload
        # Here you can add your custom logic to handle the webhook payload
        
        return {"status": "success"}
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# Create the Litestar app
app = Litestar(route_handlers=[github_webhook])

# Run the app
if __name__ == "__main__":
    app.run()
