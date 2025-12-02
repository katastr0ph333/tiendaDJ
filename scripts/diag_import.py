import sys, os, importlib
print('cwd=', os.getcwd())
print('sys.path[0]=', sys.path[0])
if os.getcwd() not in sys.path:
    sys.path.insert(0, os.getcwd())
try:
    import mainApp
    print('mainApp file->', getattr(mainApp, '__file__', None))
except Exception as e:
    print('ERROR importing mainApp:', type(e).__name__, e)
try:
    m = importlib.import_module('mainApp.models')
    print('mainApp.models file->', getattr(m, '__file__', None))
except Exception as e:
    print('ERROR importing mainApp.models:', type(e).__name__, e)
print('listing mainApp dir:')
print(os.listdir(os.path.join(os.getcwd(), 'mainApp')))
print('--- end ---')
