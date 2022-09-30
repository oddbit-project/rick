"""
Environment-based config example with environment var prefixing



Running with default values:

    $ python3 example_env_prefix.py
    Dump configuration keys => values:
      modules : ['base', 'auth', 'upload']
      name : TestApplication

Overriding default values with env vars

    $ APP_NAME="MyApp" APP_MODULES="base,auth" python3 example_env_prefix.py
    Dump configuration keys => values:
      modules : ['base', 'auth']
      name : MyApp
"""

from rick.resource.config import EnvironmentConfig

class MyConfig(EnvironmentConfig):
    NAME = "TestApplication"
    MODULES = ['base', 'auth', 'upload']

# Environment variable prefix is APP_
cfg = MyConfig().build('APP_')
print("Dump configuration keys => values:")
for name in cfg.keys():
    print("  {} : {}".format(name, str(cfg.get(name))))

