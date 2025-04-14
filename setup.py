from setuptools import setup, find_packages

setup(
    name="bohri_calendar",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "playwright",
        "Pillow",
        "reportlab",
        "asyncio",
    ],
    entry_points={
        'console_scripts': [
            'bohri-calendar=bohri_calendar.cli:main',
        ],
    },
)