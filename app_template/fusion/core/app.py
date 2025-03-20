import typing

from fastapi import FastAPI

from fusion.core.config import FusionAppConfig
from fusion.core.sheet import Sheet


class FusionApp:
    def __init__(self, config: FusionAppConfig):
        self.config = config
        self.sheets: typing.List[Sheet] = []

    def get_sheet_list(self):
        return [{"id": sheet.id, "name": sheet.name} for sheet in self.sheets]

    def get_sheet(self, sheet_id):
        return next(
            (sheet.to_dict() for sheet in self.sheets if sheet.id == sheet_id), None
        )

    def serve(self):
        # create fastapi app
        api_app = FastAPI()
        api_app.add_api_route("/sheets", self.get_sheet_list, methods=["GET"])
        api_app.add_api_route("/sheet/{sheet_id}", self.get_sheet, methods=["GET"])
        # api_app.(host=self.config.host, port=self.config.port)
        # return the app
        return api_app
