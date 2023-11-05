import json

import requests
from eolymp.asset.asset_service_http import AssetServiceClient
from eolymp.asset.asset_service_pb2 import UploadFileInput
from eolymp.atlas import statement_service_pb2, library_service_pb2, statement_pb2
from eolymp.atlas.atlas_http import AtlasClient
from eolymp.core.http_client import HttpClient
from eolymp.ecm import content_pb2
from eolymp.universe.universe_http import UniverseClient
from eolymp.universe.universe_pb2 import LookupSpaceInput, DescribeSpaceInput


class API:
    def __init__(self, space_id, username, password):
        resp = requests.post(url='https://api.eolymp.com/oauth/token',
                             data={'username': username, 'password': password,
                                   'grant_type': 'password'})
        token = json.loads(resp.text)['access_token']
        client = HttpClient(token=token)
        u = UniverseClient(client)
        space = u.DescribeSpace(DescribeSpaceInput(space_id=space_id)).space
        self.client = AtlasClient(client, url=space.url)
        self.asset = AssetServiceClient(client, url=space.url)
        pass

    def get_statements(self, prob_id):
        return self.client.ListStatements(statement_service_pb2.ListStatementsInput(problem_id=prob_id)).items

    def get_problems(self):
        def __get_problems(offset, size):
            return self.client.ListProblems(request=library_service_pb2.ListProblemsInput(offset=offset, size=size))

        return get_many(__get_problems)

    def create_statement(self, prob_id, locale, title, link, source=""):
        s = statement_pb2.Statement(problem_id=prob_id, locale=locale, title=title,
                                    content=content_pb2.Content(latex=" "), download_link=link, source=source)
        return self.client.CreateStatement(statement_service_pb2.CreateStatementInput(problem_id=prob_id,
                                                                                      statement=s)).statement_id

    def update_statement(self, problem_id, statement):
        return self.client.UpdateStatement(
            statement_service_pb2.UpdateStatementInput(problem_id=problem_id, statement_id=statement.id,
                                                       statement=statement))

    def upload_pdf(self, filename, data):
        return self.asset.UploadFile(UploadFileInput(name=filename, type="application/pdf", data=data)).file_url



def get_many(f, item_filter=None):
    items = []
    offset = 0
    size = 100
    while True:
        m = f(offset=offset, size=size)
        for item in m.items:
            if item_filter is None or item_filter(item):
                items += [item]
        if len(m.items) != size:
            break
        offset += size
        print(offset)
    return items

