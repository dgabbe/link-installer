# link-installer
```usage: Link Installer [-h] [-s] source target files

Create symbolic links (ln -s) for a set of files using the same source and
target locations.

positional arguments:
  source        The directory of the source files.
  target        The directory of the target links.
  files         JSON file containing a list of files to be linked.

optional arguments:
  -h, --help    show this help message and exit
  -s, --script  Write a script file to STDOUT instead of executing commands.
                source and target directories must include trailing '/'. Use
                '${env-name}' if environment variables should be output.

The format for the JSON file is a list of a list of pairs. [["target-link-
name", "source-file-name"],...]
```
