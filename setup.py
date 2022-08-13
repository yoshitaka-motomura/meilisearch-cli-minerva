from setuptools import setup, find_packages
with open('requirements.txt') as requirements_file:
    install_requirements = requirements_file.read().splitlines()
setup(
    name='meilisearch-Minerva',
    version='0.1.0',
    description="meilisearch simple cli",
    author='yoshitaka-motomura',
    license='MIT',
    packages=find_packages(),
    install_requires=install_requirements,
    zip_safe=False,
    entry_points={
        "console_scripts": [
            "minerva=src.minerva:cli"
        ]
    },
    classifiers=[
        'Development Status :: 1 - Planning',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Environment :: Console',

    ]
)