from setuptools import setup, find_packages

# Read the README file for the long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pyttslib",
    version="0.1.0",
    author="Uday Giri",
    author_email="www.udaygiriaparnathi2004@gmail.com",  # Updated with your email including www
    description="A powerful and easy-to-use Python Text-to-Speech library with multiple engine support",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/udaygiri/PyTTSLib",  # Updated with correct GitHub URL
    project_urls={
        "Bug Tracker": "https://github.com/udaygiri/PyTTSLib/issues",
        "Documentation": "https://github.com/udaygiri/PyTTSLib#readme",
        "Source Code": "https://github.com/udaygiri/PyTTSLib",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Multimedia :: Sound/Audio :: Speech",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "pyttsx3>=2.90",
        "gtts>=2.2.4",
        "playsound>=1.3.0",
    ],
    keywords="text-to-speech, tts, speech synthesis, audio, google-tts, pyttsx3",
    include_package_data=True,
) 