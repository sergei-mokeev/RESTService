from aiohttp.web import json_response, RouteTableDef
from restservice import RESTError, RESTService, RESTConfig, RESTHandler


routes = RouteTableDef()


# Create class Config with params as annotation
# config gets env variable ENVIRONMENT and find params in yaml file
# if config not found param with current env config gets param from DEFAULT or return None
class Config(RESTConfig):
    DB: str


# make func handler
async def func_handler(request):
    return json_response(await request.json())


# make class handler with config
@routes.view(r'/test/{user_id}')
class TestHandler(RESTHandler):
    # GET handler
    async def get(self):
        user_id = self.request.match_info.get('user_id')
        db_path = self.config.DB
        if user_id == 'exc':
            raise RESTError('USER_ID_ERROR', 'User id error.')

        return json_response({'user_id': user_id, 'db_path': db_path})


if __name__ == '__main__':
    app = RESTService()  # create aiohttp app with middleware
    app.config = Config('config.yaml')  # add config
    app.add_routes(routes)  # add route table
    app.router.add_get('/example', func_handler)  # add handler
    app.start()  # run app
