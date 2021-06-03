from flask_restful import reqparse
from models.widget import WidgetModel as WidgetDBModel
from flask_restful_swagger_3 import swagger, Resource, Schema


class WidgetModel(Schema):
    properties = {
        'name': {
            'type': 'string'
        },
        'parts': {
            'type': 'integer',
            'format': 'int64',
        },
    }

    required = ['name','parts']



class Widget(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'name',
        type=str,
        required=True,
        help='This field is required!'
    )
    parser.add_argument(
        'parts',
        type=int,
        required=True,
        help='This field is required!'
    )

    @swagger.tags('widget')
    @swagger.response(response_code=201, description='created widget')
    def post(self):
        data = self.parser.parse_args()

        # return 'bad request' if widget being added already exists
        if WidgetDBModel.find_widget_by_name(data['name']):
            return {'warning': f"An widget {data['name']} already exists"}, 400

        widget = WidgetDBModel(**data)

        widget.save_to_db()

        return widget.json(), 201

    @swagger.tags('widget')
    @swagger.response(response_code=200, description='updated widget')
    def put(self):
        data = Widget.parser.parse_args()

        widget = WidgetDBModel.find_widget_by_name(data['name'])

        if widget is None:
            widget = WidgetDBModel(**data)
        else:
            widget.name = data['name']
            widget.parts = data['parts']

        widget.save_to_db()

        return widget.json(), 200

    @swagger.tags('widget')
    @swagger.response(response_code=200, description='deleted widget')
    def delete(self):
        data = Widget.parser.parse_args()
        widget = WidgetDBModel.find_widget_by_name(data['name'])
        if widget:
            widget.delete_from_db()

        return {'message': 'widget Deleted!'}, 200


class WidgetItem(Resource):
    @swagger.tags('widget')
    @swagger.response(response_code=200, description='got widget')
    def get(self, name):
        widget = WidgetDBModel.find_widget_by_name(name)
        if widget:
            return widget.json()
        return {'warning': 'widget not found'}, 404


class WidgetList(Resource):
    def get(self):
        return {'widgets': [w.json() for w in WidgetDBModel.query.all()]}
