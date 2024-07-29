from fastapi import Depends, HTTPException, status, FastAPI, WebSocket
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import os

'''
sudo uvicorn main:app --host 0.0.0.0 --port 443 
--ssl-certfile /home/ubuntu/wandb-modal-webhook/SSL/certificate.crt 
--ssl-keyfile /home/ubuntu/wandb-modal-webhook/SSL/private.key
'''

project_dir = "/home/ubuntu/wandb-modal-webhook/"

http_bearer = HTTPBearer()
app = FastAPI()

# Mount the static directory to serve CSS files
app.mount("/static", StaticFiles(directory= os.path.join(project_dir, "static")), name="static")

class Event(BaseModel):
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

@app.get("/", response_class=HTMLResponse)
def read_root():
	with open(os.path.join(project_dir, "index.html"), "r", encoding="utf-8") as file:
		html_content = file.read()
	return HTMLResponse(content=html_content)

@app.post("/")
def webhook(event: Event, token: HTTPAuthorizationCredentials = Depends(http_bearer)):
	print(event)
	if token.credentials != "secret-random-token": #os.environ["AUTH_TOKEN"]:
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Incorrect bearer token",
			headers={"WWW-Authenticate": "Bearer"},
			)
	return {"message": "Event processed successfully"}