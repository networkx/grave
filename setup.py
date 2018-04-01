from setuptools import setup
from setuptools import find_packages

setup(name = "Grave",
      version = "0.0.1",
      description = "Dead simple graph visualization",
      long_description = "Grave is a Graph Visualization Package "\
                         "combining ideas from Matplotlib and NetworkX",
      url = "http://github.com/networkx/grave",
      author = "Grave Developers",
      author_email = "networkx-discuss@googlegroups.com",
      license = "BSD",
      packages = find_packages(),
      tests_require = ['pytest', 'pytest-runner'],
      setup_requires = ['pytest-runner'],
      zip_safe = False)
