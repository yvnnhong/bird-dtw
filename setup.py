from setuptools import setup, find_packages

setup(
    name="bird-dtw",
    version="0.1.0",
    description="Dynamic Time Warping for migratory bird path analysis",
    author="Yvonne Hong",
    author_email="yvonneh.nyc@gmail.com",
    url="https://github.com/yvnnhong/bird-dtw",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    install_requires=[
        #Add dependencies here later if needed. 
        #For now, I am just using math (built-in library)
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
    ],
)