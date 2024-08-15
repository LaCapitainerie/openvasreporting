# Table of content
| Topics | Location |
| -------- | ------- |
| Packaging | <a href="#packaging">here</a> |
| Input command | <a href="#input-command">here</a> |
| External Support | <a href="#external-support">here</a> |
| Data parsing | |
| Main Algorithm | |

## Packaging
To ensure the application can be published on Pypi to be distributed as a package, all folder need to have a **\_\_init_\_.py**,
in there you will find the licence of the application, information on the author, the package and the subpackage used in there.

Theses files won't change in the future as most feature a likealy already developed so adding one would normally be in an existing file.


**\_\_main__.py** files are processed in the same way, as they are usefull for exporting all files in the packages but nothing else, you can be sure you won't have to touch them.

## Input Command

> [!IMPORTANT]
> This section is mostly about the main file named **openvasreporting.py** at the root of the project.

First thing first, every function in this program is commented and has a description in it header.

As there is a lot of arguments, (and there will probably be new as new feature involve new parameters), you can choose to pass them in the command line you type or not as there are default values for most of them, but the command can be pretty long to write and to remember exactly, so you have an option to use a .yml file with a already done config, that let you run the script by just passing the yml file as an argument.

Theses two functions are loaded as a **Config** type, note that there is a slightly difference between theses two class, but a change should upcome to improve that.

When it's done, XML files will be convert following the Config.

## External Support

There are 6 ways to export data :

- Excel
    - By Vuln
    - By Host
- Word
    - By Vuln
- Csv
    - By Vuln
    - By Host
    - As a Summary

Each type of files doesn't have the same way to export as some were forgot to be done and some are not possible due to missconfiguration, another issue that will be patched.

#### Excel

> [!NOTE]
> Excel one contains graph and table, each Vuln/Host are listed in a different page to ensure readability.

#### Word

> [!TIP]
> You can actually customise your word output file by making a template of it, the one currently used can be found there : **/openvasreporting/src/openvas-template.docx**

#### CSV

Csv output are most tables that you can found on excel and word output, as their main goal is to pass data.