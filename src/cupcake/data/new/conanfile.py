from conan import ConanFile
from conan.tools.cmake import CMake

class {{ NameTitle }}(ConanFile):
    name = '{{ name }}'
    version = '0.1.0'
    {% if github %}
    user = 'github'
    channel = '{{ github }}'
    {% endif %}

    license = '{{ license }}'
    {% if author %}
    author = '{{ author }}'
    {% endif %}
    {% if github %}
    url = 'https://github.com/{{ github }}/{{ name }}'
    {% endif %}

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False], 'fPIC': [True, False]}
    default_options = {'shared': False, 'fPIC': True}

    requires = ['cupcake/0.5.0@github/thejohnfreeman']
    test_requires = ['doctest/2.4.8']
    generators = ['CMakeDeps', 'CMakeToolchain']

    exports_sources = [
        'CMakeLists.txt',
        'cmake/*',
        'external/*',
        'include/*',
        'src/*',
    ]

    # For out-of-source build.
    # https://docs.conan.io/en/latest/reference/build_helpers/cmake.html#configure
    no_copy_source = True

    def requirements(self):
        for requirement in self.test_requires:
            self.requires(requirement)

    def config_options(self):
        if self.settings.os == 'Windows':
            del self.options.fPIC

    def build(self):
        cmake = CMake(self)
        cmake.configure(variables={'BUILD_TESTING': 'NO'})
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        path = f'{self.package_folder}/share/{self.name}/cpp_info.py'
        with open(path, 'r') as file:
            exec(file.read(), {}, {'self': self.cpp_info})
