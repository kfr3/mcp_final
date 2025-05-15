from setuptools import setup, find_packages

setup(
    name="mcp_final",
    version="0.1.0",
    packages=find_packages(),
    package_dir={"": "src"},
    install_requires=[
        "fastapi",
        "uvicorn",
        "sqlalchemy",
        "pydantic",
        "httpx",
        # Add other dependencies as needed
    ],
) 