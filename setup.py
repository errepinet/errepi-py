from distutils.core import setup

setup(
    name="errepi-py",
    version="0.0.1",
    description="Python bindings for Errepi Net microservices",
    packages=["errepi"],
    author="Valerio Faiuolo",
    author_email="valerio.faiuolo@errepinet.it",
    python_requires=">=3.10,<4",
    keywords=["errepinet", "microservices", "bindings"],
    url="https://github.com/errepinet/errepi-py",
    install_requires=["pydantic>=2.0.0,<3.0.0", "requests>=2.0.0,<3.0.0"],
)
