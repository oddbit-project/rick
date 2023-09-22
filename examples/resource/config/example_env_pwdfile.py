"""
Environment-based config example with support for optional password files (such as docker secrets)

String values are considered files if they start with '/' or './'

Running with default values:

    $ python3 example_env_pwdfile.py
    Dump configuration keys => values:
      db_name : my_db
      db_password : password

Specifying a password directly:
    $ DB_PASSWORD="mysuperduperpassword" python3 example_env_pwdfile.py
    Dump configuration keys => values:
      db_name : my_db
      db_password : mysuperduperpassword

Using db_password.txt as a password file:
    $ DB_PASSWORD="./db_password.txt" python3 example_env_pwdfile.py
    Dump configuration keys => values:
      db_name : my_db
      db_password : drwtwtgdfgew52efvzsdc
"""


from rick.resource.config import EnvironmentConfig, StrOrFile

class MyConfig(EnvironmentConfig):
    DB_NAME = "my_db"
    DB_PASSWORD = StrOrFile("password")


cfg = MyConfig().build()
print("Dump configuration keys => values:")
for name in cfg.keys():
    print(f"  {name} : {str(cfg.get(name))}")

