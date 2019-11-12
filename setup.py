import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
try:
    with open(os.path.join(here, "README.rst")) as f:
        README = f.read()
    with open(os.path.join(here, "CHANGES.txt")) as f:
        CHANGES = f.read()
except IOError:
    README = CHANGES = ""

install_requires = []

dev_extras = ["black"]
tests_require = []

testing_extras = tests_require + []

setup(
    name="pycomment",
    version=open(os.path.join(here, "VERSION")).read().strip(),
    description="with repr value as comment",
    long_description=README + "\n\n" + CHANGES,
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
    keywords="",
    author="podhmo",
    author_email="ababjam61+github@gmail.com",
    url="https://github.com/podhmo/pycomment",
    packages=find_packages(exclude=["pycomment.tests"]),
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    extras_require={"testing": testing_extras, "dev": dev_extras},
    tests_require=tests_require,
    test_suite="pycomment.tests",
    entry_points="""
[console_scripts]
pycomment = pycomment.__main__:main
""",
)
