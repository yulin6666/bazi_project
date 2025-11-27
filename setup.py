from setuptools import find_packages, setup

setup(
    name="bazi-api",
    version="1.0.0",
    description="基于FastAPI的八字计算API服务",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(),
    install_requires=[
        "fastapi==0.104.1",
        "uvicorn[standard]==0.24.0",
        "langchain==0.1.0",
        "langchain-openai==0.1.0",
        "lunar-python==1.2.0",
        "pydantic==2.5.0",
    ],
    python_requires=">=3.11",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)