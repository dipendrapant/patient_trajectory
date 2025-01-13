import os

from setuptools import find_packages, setup

# Read the contents of your README file
long_description = ""
if os.path.isfile("README.md"):
    with open("README.md", encoding="utf-8") as f:
        long_description = f.read()

setup(
    name="patient_trajectory",            
    version="0.1.0",                      
    author="Dipendra Pant",
    author_email="dipendrapant778@gmail.com",
    description="A package to visualize patient trajectories for any number of patients",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dipendrapant/patient_trajectory",  # Update as needed
    packages=find_packages(),
    install_requires=[
        "pandas>=1.0.0",
        "matplotlib>=3.0.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
