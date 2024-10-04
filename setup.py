from setuptools import setup

setup(
    name="dk",
    version="0.1",
    py_modules=["dk"],
    # install_requires=["gitpython"],
    entry_points={
        "console_scripts": [
            "dk = dk:main",
        ],
    },
)
