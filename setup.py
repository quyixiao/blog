from distutils.core import setup
import glob

setup(
    name="blog",
    version="0.1.1",
    author="quyixiao",
    author_email="2621048238@qq.com",
    description="测试",
    url="http://www.baidu.com",
    packages=['blog', 'user', 'post'],
    data_files=glob.glob('templates/*.html') + ['requirements', 'manage.py'],
)
