from setuptools import setup, find_packages


setup(
    name='selenium-recaptcha-solver',
    version='1.0.6',
    license='MIT',
    author='Tomás Perestrelo',
    author_email='tomasperestrelo21@gmail.com',
    packages=find_packages(exclude=('tests*', 'testing*')),
    url='https://github.com/thicccat688/selenium-recaptcha-solver',
    download_url='https://pypi.org/project/selenium-recaptcha-solver',
    keywords='python, captcha, speech recognition, selenium, web automation',
    long_description=open('README.md', 'r').read(),
    long_description_content_type='text/markdown',
)
