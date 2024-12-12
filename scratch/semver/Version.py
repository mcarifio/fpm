#!/usr/bin/env python
import re


class Version:
    # https://regex101.com/r/vkijKf/1/
    version_re = r"^(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)(-((?P<prerelease>0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(\+(?P<build>([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*)))?$"

    def __init__(self, data):
        for key, value in data.items():
            setattr(self, key, value)

    @staticmethod
    def parse(version):
        if match := re.match(Version.version_re, version):
            return Version(match.groupdict())

    def __str__(self):
        return str(self.__dict__)


if "__main__" == __name__:
    print(Version.parse("1.0.0"))
    print(Version.parse("1.0.0-alpha.1"))
    print(Version.parse("1.0.0-alpha.1+build.it.good"))
    print(Version.parse("1.0"))

    version = Version.parse("1.0.0")
    print(version and version.major)
    version = Version.parse("1.0")
    print(version and version.major)
