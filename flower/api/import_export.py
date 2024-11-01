import json
from tornado import web
from ..utils.import_export import export_tasks_and_workers, import_tasks_and_workers
from . import BaseApiHandler

class ExportHandler(BaseApiHandler):
    @web.authenticated
    def get(self):
        """
        Export tasks and workers data

        **Example request**:

        .. sourcecode:: http

          GET /api/export HTTP/1.1
          Host: localhost:5555

        **Example response**:

        .. sourcecode:: http

          HTTP/1.1 200 OK
          Content-Length: 1234
          Content-Type: application/json; charset=UTF-8

          {
              "tasks": [...],
              "workers": [...]
          }

        :reqheader Authorization: optional OAuth token to authenticate
        :statuscode 200: no error
        :statuscode 401: unauthorized request
        """
        data = export_tasks_and_workers(self.application.events.state)
        self.write(data)
        self.set_header('Content-Type', 'application/json')

class ImportHandler(BaseApiHandler):
    @web.authenticated
    def post(self):
        """
        Import tasks and workers data

        **Example request**:

        .. sourcecode:: http

          POST /api/import HTTP/1.1
          Content-Length: 1234
          Content-Type: application/json; charset=UTF-8
          Host: localhost:5555

          {
              "tasks": [...],
              "workers": [...]
          }

        **Example response**:

        .. sourcecode:: http

          HTTP/1.1 200 OK
          Content-Length: 17
          Content-Type: application/json; charset=UTF-8

          {
              "message": "Import successful"
          }

        :reqheader Authorization: optional OAuth token to authenticate
        :statuscode 200: no error
        :statuscode 400: invalid data
        :statuscode 401: unauthorized request
        """
        try:
            data = json.loads(self.request.body)
            import_tasks_and_workers(self.application.events.state, data)
            self.write({"message": "Import successful"})
            self.set_header('Content-Type', 'application/json')
        except json.JSONDecodeError as e:
            raise web.HTTPError(400, f"Invalid data: {e}")
