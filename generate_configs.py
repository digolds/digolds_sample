import os
from config import digolds_service_path, unix_sock, user

gunicorn_bin_name = os.popen('which gunicorn').read().strip()

gunicorn_config = f"""
[supervisorctl]

[program:gunicorn]
command={gunicorn_bin_name} -b {unix_sock} wsgiapp:wsgi_app
directory={digolds_service_path}
user={user}
autostart=true
autorestart=true
redirect_stderr=true
"""

with open('gunicorn.conf', 'w') as file:
    file.write(gunicorn_config.strip())