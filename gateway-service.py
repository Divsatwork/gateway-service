"""
Gateway Service.
Brought to you by DC.

Just give the port for this service to start and you are ready to go.
Handles automatic registration of services and health checks periodically.
"""
import json
import web
import yaml
import sys
import requests

DEFAULT_PORT = 9900

urls = (
    '/(.*)', 'Index'
)

print("Initializing Gateway-service....")
args = sys.argv
if len(args) == 0 or len(args) > 2:
    raise Exception("Please provide correct arguments."
                    "\nFormat: python3 gateway-service [yaml-file-name: required] [port: optional]"
                    "\nExpected format: python3 gateway-service example.yaml 8081")

"""
YAML Structure:
{SERVICE_NAME: {"apis": [], "host": "", "port": "", "name": ""}}
"""
print(f"Reading the yaml file: [{args[1]}]")
with open(args[1]) as f:
    yaml_config = yaml.load(f, Loader=yaml.FullLoader)

API_MAP = {}
# Initializing API map from yaml_config
for k, v in yaml_config.items():
    # k = service name
    # v = {apis, host, port}
    for api in v["apis"]:
        API_MAP[api] = "http://" + v["host"] + ":" + str(v["port"]) + api


class Index:

    def GET(self, api_to_hit):
        uri = API_MAP.get("/" + api_to_hit)
        if uri is None:
            return json.dumps({"Error": "No service registered for this call"})
        response = requests.get(uri, web.input())
        web.ctx.status = str(response.status_code)
        for k, v in response.headers.items():
            web.header(k, v)
        return response.content

    def POST(self, api_to_hit):
        uri = API_MAP.get("/" + api_to_hit)
        if uri is None:
            return json.dumps({"Error": "No service registered for this call"})
        response = requests.post(uri, web.data())
        web.ctx.status = str(response.status_code)
        for k, v in response.headers.items():
            web.header(k, v)
        return response.content

    def PUT(self, api_to_hit):
        uri = API_MAP.get("/" + api_to_hit)
        if uri is None:
            return json.dumps({"Error": "No service registered for this call"})
        response = requests.put(uri, web.data())
        web.ctx.status = str(response.status_code)
        for k, v in response.headers.items():
            web.header(k, v)
        return response.content

    def DELETE(self, api_to_hit):
        uri = API_MAP.get("/" + api_to_hit)
        if uri is None:
            return json.dumps({"Error": "No service registered for this call"})
        response = requests.delete(uri, web.input())
        web.ctx.status = str(response.status_code)
        for k, v in response.headers.items():
            web.header(k, v)
        return response.content


if __name__ == "__main__":
    port = DEFAULT_PORT if len(args) < 3 else args[2]
    app = web.application(urls, globals())
    print(f"Starting Gateway-service on port: [{port}]")
    web.httpserver.runsimple(app.wsgifunc(), ("0.0.0.0", port))
