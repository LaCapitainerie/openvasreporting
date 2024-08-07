# -*- coding: utf-8 -*-
#
"""

This file parse the XML report from OpenVAS and return the data in a structured way

"""
#
# Project name: OpenVAS Reporting: A tool to convert OpenVAS XML reports into Excel files.
# Project URL: https://github.com/groupecnpp/OpenvasReporting

from typing import Callable
from .config import Config
from .parsed_data import ResultTree, Host, Port, Vulnerability, ParseVulnerability

from defusedxml import ElementTree as Et

def parsers() -> dict[str, Callable]:
        """
        Enum-like instance containing references to correct parser function
    
        > parsers()[key] (param[s])
    
        :return: Pointer to parser function
        """
        return {
            'vulnerability': openvas_parser_by_vuln,
            'host': openvas_parser_by_host,
            'summary': openvas_parser_by_vuln
        }

def openvas_parser_by_vuln(config: Config) -> list[Vulnerability]:
    """
    This function takes an OpenVAS XML report and returns Vulnerability info

    :param config: config options as by the command line or defaults
    :type config: Config

    :return: list

    :raises: TypeError, InvalidFormat
    """
    
    if not isinstance(config, Config):
        raise TypeError("Expected Config, got '{}' instead".format(type(config)))
    for file in config.input_files:
        if not isinstance(file, str):
            raise TypeError(
                "Expected basestring, got '{}' instead".format(type(file)))
        with open(file, "r", newline=None) as f:
            first_line = f.readline()
            if not first_line.startswith("<report") or \
                    not all(True for x in ("extension", "format_id", "content_type") if x in first_line):
                raise IOError("Invalid report format")

    vulnerabilities:dict[str, Vulnerability] = {}

    for f_file in config.input_files:
        root = Et.parse(f_file).getroot()

        for vuln in root.findall(".//results/result"):

            parsed_vuln = ParseVulnerability.check_and_parse_result(vuln, config)
            if parsed_vuln is None:
                continue

            if Config.cvss_level(parsed_vuln.vuln_cvss) not in config.threat_included:
                continue

            # --------------------
            #
            # STORE VULN_HOSTS PER VULN
            host = Host(parsed_vuln.vuln_host, host_name=parsed_vuln.vuln_host_name)
            try:
                # added results to port function as will ne unique per port on each host.
                port = Port.string2port(parsed_vuln.vuln_port, parsed_vuln.vuln_result) 
            except ValueError:
                port = Port(0, "", "")

            vuln_store = Vulnerability(
                parsed_vuln.vuln_id, 
                name=parsed_vuln.vuln_name,
                threat=parsed_vuln.vuln_threat,
                tags=parsed_vuln.vuln_tags,
                cvss=parsed_vuln.vuln_cvss,
                cves=parsed_vuln.vuln_cves,
                references=parsed_vuln.vuln_references,
                family=parsed_vuln.vuln_family,
                level=parsed_vuln.vuln_level
            )

            vuln_store.add_vuln_host(host, port)
            vulnerabilities[parsed_vuln.vuln_id] = vuln_store 

    return list(vulnerabilities.values())

def openvas_parser_by_host(config: Config) -> ResultTree:
    """
    This function takes an OpenVAS XML report and returns Vulnerability info

    :param config: config options as by the command line or defaults
    :type config: Config

    :return: list

    :raises: TypeError, InvalidFormat
    """
    
    if not isinstance(config, Config):
        raise TypeError("Expected Config, got '{}' instead".format(type(config)))
    for file in config.input_files:
        if not isinstance(file, str):
            raise TypeError(
                "Expected basestring, got '{}' instead".format(type(file)))
        with open(file, "r", newline=None) as f:
            first_line = f.readline()
            if not first_line.startswith("<report") or \
                    not all(True for x in ("extension", "format_id", "content_type") if x in first_line):
                raise IOError("Invalid report format")

    resulttree = ResultTree()

    for f_file in config.input_files:
        root = Et.parse(f_file).getroot()

        for vuln in root.findall(".//results/result"):

            parsed_vuln = ParseVulnerability.check_and_parse_result(vuln, config)
            if parsed_vuln is None:
                continue

            if Config.cvss_level(parsed_vuln.vuln_cvss) not in config.threat_included:
                continue

            resulttree.addresult(parsed_vuln)

    if len(resulttree) == 0:
        raise ImportError('No valid <results> found. Check exclusions and/or scope listings. I\'ve got nothing to do')
    
    return resulttree

