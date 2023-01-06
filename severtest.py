import xmlrpc.client

proxy = xmlrpc.client.ServerProxy('http://localhost:8002')
for method_name in proxy.system.listMethods():
    print('=' * 60)
    print(method_name)
    print('-' * 60)
    print(proxy.system.methodHelp(method_name))
    print()