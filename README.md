# errepi-py
Python bindings for Errepi Net microservices

## Install with pip

```bash
# Install latest version
pip install git+ssh://git@github.com:errepinet/errepi-py.git

# Install specific version
pip install git+ssh://git@github.com:errepinet/errepi-py.git@version
```

In requirements.txt add, for latest version:
`git+ssh://git@github-SindacalistaErrepinet/errepinet/errepi-py.git`

for specific version:
`git+ssh://git@github-SindacalistaErrepinet/errepinet/errepi-py.git@version`


## Simple example
```python
from errepi.cron import CronConfigurator
cron = CronConfigurator.from_env()
info = cron.app_info()
print("App info:", info)
```

more detailed example founds in \examples directory