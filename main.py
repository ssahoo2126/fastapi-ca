from fastapi import FastAPI
from user.interface.controllers.user_controller import router as user_routers
import user.interface.controllers.user_controller as user_controller_module
from fastapi.exceptions import RequestValidationError
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from containers import Container

app = FastAPI()
app.container = Container()
app.container.wire(modules=[user_controller_module])
app.include_router(user_routers)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(status_code=400, content=exc.errors())
    

@app.get("/")
def hello():
    return {"Hello": "FastAPI"}