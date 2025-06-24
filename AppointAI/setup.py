from setuptools import find_packages, setup
from typing import List

def get_requirements() -> List[str]:
    try:
        with open("requirements.txt", "r") as file:
            requirement_list = [
                line.strip() for line in file.readlines()
                if line.strip() and line.strip() != "-e ."
            ]
        return requirement_list
    except FileNotFoundError:
        print("requirements.txt file not found. Returning an empty list.")
        return []
    
setup(
    name="appointai",
    version="0.1.0",
    author="Yogesh Nikam",
    author_email="yogeshk04@gmail.com",
    description="Appointment scheduling AI using LangGraph",
    long_description="This package provides an AI solution for scheduling appointments using LangGraph.",
    long_description_content_type="text/markdown",
    install_requires=get_requirements(),
    python_requires=">=3.10"
)