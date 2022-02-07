from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='fastgame',
    author_email='13513519246@139.com',
    author='stripe-python',
    maintainer='stripe-python',
    maintainer_email='13513519246@139.com',
    py_modules=find_packages(),
    version='1.1.0',
    description='Fastgame是一个帮助你快速构建游戏或简单的GUI界面的python第三方库。',
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=['pygame>=2.1.0', 'arrow', 'opencv-python', 'tqdm', 'pillow'],
    python_requires='>=3.6',
)
