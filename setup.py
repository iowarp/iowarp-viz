import setuptools
import os
import shutil

setuptools.setup(
    name="py_hermes_mdm",
    packages=setuptools.find_packages(),
    scripts=['bin/hermes_viz_server'],
    version="0.0.1",
    author="Luke Logan",
    author_email="lukemartinlogan@gmail.com",
    description="Vizualizer for an I/O buffering library",
    url="https://github.com/HDFGroup/hermes.git",
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Development Status :: 1.1",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "License :: None",
        "Operating System :: Linux",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: I/O",
    ],
    long_description="",
    install_requires=[
        "pybind11",
        "pytest",
        "flask"
    ]
)

home = os.path.expanduser("~")
dashboard_src = os.path.join(os.path.dirname(__file__), "dashboard")
dashboard_dst = os.path.join(home, ".hermes_viz")

if os.path.exists(dashboard_dst):
    shutil.rmtree(dashboard_dst)
shutil.copytree(dashboard_src, dashboard_dst)