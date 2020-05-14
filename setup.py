from setuptools import setup

setup(
    name="asx_technical_analysis",
    version="1.9.2",
    description="Analyse ASX stocks using basic technique",
    url="https://github.com/liverpool1026/asx_technical_analysis",
    author="Kevin Hwa",
    author_email="web.hawkvine@gmail.com",
    packages=["asx_analysis"],
    include_package_data=True,
    install_requires=["attrs", "numpy", "pandas", "requests"],
)
