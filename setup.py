from setuptools import setup


setup(
    name='ioeval',
    version='1.0',
    description='musicologically-informed tools for symbolic music generation evaluation',
    author='RoseQSun',
    packages=['ioeval'],
    install_requires=['matplotlib==3.7.1', 'music21==8.1.0', 'numpy'],
    scripts=['scripts/utils.py'],
    include_package_data=True,
    python_requires='>=3.7'
)