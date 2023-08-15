import re

from functools import total_ordering

__all__ = ['SemanticVersion']

# regular expressions for checking semantic version guidelines
IDENTIFIER = '[a-zA-Z0-9-]'
DOTSEP_ID = rf'{IDENTIFIER}+(\.{IDENTIFIER}+)*'
PRE_RELEASE = rf'(?P<pre_release>{DOTSEP_ID})'
BUILD = rf'(?P<build>{DOTSEP_ID})'
VERSION = r'(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)'
SEMVAR = re.compile(rf'[Vv]?(?P<version>{VERSION})(-{PRE_RELEASE})?(\+{BUILD})?$')


class InvalidSemanticVersion(Exception):
    def __init__(self, *args):
        super().__init__(*args)


@total_ordering
class SemanticVersion:
    __slots__ = '_major', '_minor', '_patch', '_preRelease', '_build'

    def __init__(self, version: str):
        if not isinstance(version, str):
            raise TypeError('version must be a str type')

        match = SEMVAR.fullmatch(version)
        if match is None:
            raise InvalidSemanticVersion('version string does not contain a valid sematic version')

        results = match.groupdict(default='')
        self._major = int(results['major'])
        self._minor = int(results['minor'])
        self._patch = int(results['patch'])
        self._preRelease = results['pre_release']
        self._build = results['build']
        for p in self._preRelease.split('.'):
            if p != '0' and p[0] == '0':
                raise InvalidSemanticVersion('pre-release dot separated identifiers must not include leading zeros')

    def __str__(self) -> str:
        rtn = f'{self._major}.{self._minor}.{self._patch}'
        if self._preRelease:
            rtn += f'-{self._preRelease}'
        if self._build:
            rtn += f'+{self._build}'

        return rtn

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}("{self.__str__()}")'

    @property
    def version(self):
        return f'{self._major}.{self._minor}.{self._patch}'

    @property
    def major(self):
        return self._major

    @property
    def minor(self):
        return self._minor

    @property
    def patch(self):
        return self._patch

    @property
    def preRelease(self):
        return self._preRelease

    @property
    def buildMetadata(self):
        return self._build

    def __eq__(self, other: 'SemanticVersion') -> bool:
        if isinstance(other, SemanticVersion):
            return (self._major == other._major and self._minor == other._minor and self._patch == other._patch
                    and self._preRelease == other._preRelease)

        return NotImplemented

    def __lt__(self, other: 'SemanticVersion') -> bool:
        if isinstance(other, SemanticVersion):
            pass

        return NotImplemented

    def toDict(self):
        return {'major': self._major, 'minor': self._minor, 'patch': self._patch,
                'pre_release': self._preRelease, 'build_metadata': self._build}
