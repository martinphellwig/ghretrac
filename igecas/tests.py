#from django.test import TestCase

# Create your tests here.


from igecas.libs import jsonrpc

api = jsonrpc.DjangoProxy(port='8000', path='igecas/api/')

print(api.django.login('admin', 'admin'))
