import hmac
import hashlib
import json
import yaml
from authlib.integrations.requests_client import OAuth2Session
from authlib.oauth2.rfc7523 import PrivateKeyJWT
from litestar import Litestar, post, Request
from litestar.exceptions import HTTPException

import logging

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

def read_file_content(file_path: str) -> str:
    """Read content from a file and return as a string."""
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            return content
    except Exception as e:
        logging.error(f"Error: {e}")
        return ""


def verify_signature(payload: bytes, signature: str, secret: str) -> bool:
    """Verify GitHub webhook signature."""
    mac = hmac.new(secret.encode(), msg=payload, digestmod=hashlib.sha256)
    expected_signature = f'sha256={mac.hexdigest()}'
    return hmac.compare_digest(expected_signature, signature)


def read_admission_conf(file_path: str) -> dict:
    """Read admission configuration."""
    try:
        with open(file_path, 'r') as file:
            yaml_content = yaml.safe_load(file)
            return yaml_content
    except Exception as e:
        logging.error(f"Error: {e}")
        return None


def check_adminssion(data: dict, admission_conf: dict) -> bool:
    admitted = False
    if data['action'] != 'queued':
        return False
    for i in admission_conf['repository']:
        if data['repository']['full_name'] != i['name']:
            continue
        elif data['workflow_job']['head_branch'] not in i['branch']:
            continue
        elif data['sender']['login'] not in i['user']:
            continue
        else:
            admitted = True    
            clusters = i['cluster']
    return admitted, clusters


def run_job(data_dict: dict, clusters: dict) -> None:
    """Run the job."""
    # Implement the job logic here
    logging.info("Running the job...")
    logging.info(f"Repository: {data_dict['repository']['full_name']}")
    logging.info(f"Branch: {data_dict['workflow_job']['head_branch']}")
    logging.info(f"Sender: {data_dict['sender']['login']}")
    logging.info(clusters)
    if "perlmutter" in clusters:
        logging.info("Running on Perlmutter")
        # call SF API to run the job
        logging.info(f"CLIENTID = {CLIENTID}")
        logging.info(f"PRIVATE_KEY = {PRIVATE_KEY}")
        logging.info(f"TOKEN_URL = {TOKEN_URL}")
        session = OAuth2Session( CLIENTID, PRIVATE_KEY, PrivateKeyJWT(TOKEN_URL), grant_type="client_credentials", token_endpoint=TOKEN_URL)
        logging.info(session.fetch_token())
        # will need to copy start_runner script first... 
        cmd=f"{START_RUNNER_SCRIPT} {data_dict['repository']['full_name']}"
        r = session.post("https://api.nersc.gov/api/v1.2/utilities/command/perlmutter", data = {"executable": cmd})
        logging.info(f"Superfacility API status: r.json()")
    logging.info("Job completed.")
    return None


# Define your GitHub webhook secret
SECRETS_DIR='/secrets'
GITHUB_SECRET = read_file_content(f'{SECRETS_DIR}/github_secret.txt')
CLIENTID = read_file_content(f'{SECRETS_DIR}/clientid.txt')
PRIVATE_KEY = read_file_content(f'{SECRETS_DIR}/priv_key.pem')
TOKEN_URL = "https://oidc.nersc.gov/c2id/token"
ADMISSION_CONF = '/ciapi/configs/admission.yaml'
START_RUNNER_SCRIPT = '/ciapi/scripts/start_runner.sh'


admission_conf = read_admission_conf(ADMISSION_CONF)

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
        # parse data and decide what to do with it
        
        logging.info("Received payload.")
        #print(json.dumps(data, indent=4))
        admitted, clusters = check_adminssion(data, admission_conf)
        if admitted:
            logging.info("Admission success")
            logging.info(f"data['action'] = {data['action']}")
            logging.info(f"data['repository']['full_name'] = {data['repository']['full_name']}")
            logging.info(f"data['workflow_job']['head_branch'] = {data['workflow_job']['head_branch']}")
            logging.info(f"data['sender']['login'] = {data['sender']['login']}")
            run_job(data, clusters)
            return {"status": "job admitted"}
        return {"status": "success, job not admitted"}
    except Exception as e:
        #print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# Create the Litestar app
app = Litestar(route_handlers=[github_webhook])

# Run the app
if __name__ == "__main__":
    app.run()
