# -*- coding: utf-8 -*-
#
#
# Project name: OpenVAS Reporting: A tool to convert OpenVAS XML reports into Excel files.
# Project URL: https://github.com/groupecnpp/OpenvasReporting

from .openvasreporting import main

__author__ = 'CNPP (https://github.com/TheGroundZero)'
__maintainer__ = 'LaCapitainerie'

if __name__ == '__main__':
    if __package__ is None:
        from os import path
        from sys import path as spath

        spath.append(path.dirname(path.dirname(path.abspath(__file__))))
        del spath, path

    main()
