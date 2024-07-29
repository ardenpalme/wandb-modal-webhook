from fastapi import Depends, HTTPException, status, FastAPI
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel

auth_scheme = HTTPBearer()
app = FastAPI()

class Event(BaseModel):
    "Defines the payload your webhook will send."
    event_type: str
    event_author: str
    alias: str
    artifact_version: str
    artifact_version_string: str
    artifact_collection_name: str
    project_name: str
    entity_name: str

    def __str__(self):
        msg = 'Payload:\n========\n'
        for k,v in self.model_dump().items():
            msg += f'{k}={v}\n'
        return msg

@app.post("/")
def webhook(event: Event, 
            token: HTTPAuthorizationCredentials = Depends(auth_scheme)):
    "Receive the webhook and print the payload.  Uses a token to authenticate."
    print(event)
    if token.credentials != 'secret-random-token':
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect bearer token",
            headers={"WWW-Authenticate": "Bearer"},
            )
    return {"message": "Event processed successfully"}


def verify_HTTPS_token(credentials: HTTPSAuthorizationCredentials = Depends(https_bearer)):
	token = credentials.credentials
	with open("/home/ubuntu/wandb-modal-webhook/SSL/public_key.pem") as in_key:
		public_key = in_key.read()
	try:
		# Decode the JWT token using the public key
		payload = jwt.decode(token, public_key, algorithms=["RS256"])

	except jwt.ExpiredSignatureError:
		raise HTTPException(
			status_code=status.HTTP_403_FORBIDDEN,
			detail="Token has expired"
		)
	except jwt.InvalidTokenError:
		raise HTTPException(
			status_code=status.HTTP_403_FORBIDDEN,
			detail="Invalid token"
		)
