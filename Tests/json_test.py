from io import StringIO
import json

io = StringIO('{"success":false}')
ob = json.load(io)

print(ob["success"])