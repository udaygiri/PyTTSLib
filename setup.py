from setuptools import setup, find_packages

setup(
    name="pyttslib",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pyttsx3>=2.90",
        "gtts>=2.2.4",
        "playsound>=1.3.0",
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="A comprehensive text-to-speech library with multiple engine support",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/pyttslib",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
) 