import json

with open('./config/development.json', 'r', encoding='utf-8') as fp:
    mongo_development = json.load(fp)

with open('./config/integration.json', 'r', encoding='utf-8') as fp:
    mongo_integration = json.load(fp)

with open('./config/local.json', 'r', encoding='utf-8') as fp:
    mongo_local = json.load(fp)

with open('./config/local_backup.json', 'r', encoding='utf-8') as fp:
    mongo_local_backup = json.load(fp)
