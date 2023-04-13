from flask import Flask
from flask_restx import Api, Resource
from models import User
from config import ConnectionConfig
from connection import DbConnection
from flask_jwt_extended import JWTManager
from auth import auth_ns
from search import search_ns
from flask_cors import CORS

def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)

    CORS(app)

    DbConnection.start(ConnectionConfig)

    JWTManager(app)

    # blueprint = Blueprint('api', __name__, url_prefix='/api') # url prefix is for Base URL shown in docs
    # api = Api(app, version='1.0', title='Game Munchers API', doc="/docs")
    # api = Api(blueprint, version='1.0', title='Game Munchers API', doc="/docs")
    # app.register_blueprint(blueprint)
    # create api with prefix
    api = Api(app, version='1.0', title='Game Munchers API', doc="/api/docs", prefix='/api')

    api.add_namespace(auth_ns)
    api.add_namespace(search_ns)
    # api.add_namespace(auth_ns, path=prefix) # path is for Base URL shown in docs

    @app.route('/')
    def index():
        return {"message": "Hello World from the root route"}
    
    # @app.route('/')
    # def test1():
    #     return {"message": "actual root"}
    
    @app.route('/api/test2')
    def test2():
        return {"message": "getting crazy now"}
    
    # @app.route('/test')
    # def test():
    #     return {"message": "Hello World"}
    @api.route('/test') # since under api, it has the prefix /api
    class test(Resource):
        def get(self):
            return {"message": "Hello World"}
    
    @app.errorhandler(404)
    def page_not_found(e):
        return '404 (custom)Page Not Found', 404
    
    # model (serializer) for user
    @app.shell_context_processor
    def make_shell_context():
        return {'db': DbConnection.get_connection(), 'User': User}
    
    return app