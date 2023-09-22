"""
Environment-based config example

Running with default values:

    $ python3 example_env_simple.py
    Dump configuration keys => values:
      app_modules : ['base', 'auth', 'upload']
      app_name : TestApplication

Overriding default values with env vars

    $ APP_NAME="MyApp" APP_MODULES="base,auth" python3 example_env_simple.py
    Dump configuration keys => values:
      app_modules : ['base', 'auth']
      app_name : MyApp
"""


from rick.resource.config import EnvironmentConfig

class MyConfig(EnvironmentConfig):
    APP_NAME = "TestApplication"
    APP_MODULES = ['base', 'auth', 'upload']


cfg = MyConfig().build()
print("Dump configuration keys => values:")
for name in cfg.keys():
    print(f"  {name} : {str(cfg.get(name))}")

