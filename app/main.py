from fastapi import FastAPI, Depends
from .router.users import users_router
from .router.login import login_router,oauth2_scheme
from .router.parking import parking_router

app = FastAPI()
app.include_router(users_router)
app.include_router(login_router)
app.include_router(parking_router)

@app.get("/")
def home(token: str = Depends(oauth2_scheme)):
    return {"Info": "Just for Fun = " + token}
#
# @app.post("/token")
# async def token(form_data: OAuth2PasswordRequestForm = Depends()):
#     return {'access_token': form_data.username + "_token"}