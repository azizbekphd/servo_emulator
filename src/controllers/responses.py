from openpyxl import load_workbook, Workbook
import os


class ResponsesControllerState:

    def __init__(self, config, workbook=None, request_response_pairs={}):
        self.workbook = workbook
        self.request_response_pairs = request_response_pairs
        self.config = config


class ResponsesController:

    def __init__(self, state):
        self.state = state

    def load_pairs(self):
        config = self.state.config
        filename = config["FILENAME"]

        if (os.path.isfile(filename)):
            self.state.workbook = load_workbook(filename)
            sheet = self.state.workbook.active
            index = 2
            while True:
                req = sheet[config["REQUESTS"]["COLUMN"] + str(index)].value
                res = sheet[config["RESPONSES"]["COLUMN"] + str(index)].value
                if (not (req and res)):
                    break
                self.state.request_response_pairs[req] = res
                index += 1
        return True

    def set_pair(self, req, res):
        self.state.request_response_pairs[req] = res
        return True

    def get_response(self, req):
        return self.state.request_response_pairs[req]

    def save_pairs(self):
        config = self.state.config
        filename = config["FILENAME"]

        self.state.workbook = Workbook()
        sheet = self.state.workbook.create_sheet(
                title=config["WORKSHEET_TITLE"])
        req_column = config["REQUESTS"]["COLUMN"]
        res_column = config["RESPONSES"]["COLUMN"]
        sheet[req_column + "1"] = config["REQUESTS"]["TITLE"]
        sheet[res_column + "1"] = config["RESPONSES"]["TITLE"]

        index = config["START_ROW"]
        for req, res in self.state.request_response_pairs.items():
            sheet[req_column + str(index)] = req
            sheet[res_column + str(index)] = res
            index += 1

        self.state.workbook.save(filename)
