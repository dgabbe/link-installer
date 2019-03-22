#! /usr/bin/env python3
#
# link-installer --help for usage
#
# Build as an exe:
#   python3 -m nuitka --follow-imports --show-progress --python-flag=no_site --remove-output link-installer.py --standalone
#
# May need to use  --file-reference-choice=FILE_REFERENCE_MODE
#

from argparse import ArgumentParser, FileType
from json import load
from os import rename, symlink
from os.path import exists, isdir, isfile, islink, join, realpath
from sys import exit


def main():

    parser = ArgumentParser(
        prog="Link Installer",
        description="""Create symbolic links (ln -s) for a set of files using the same source and target locations.""",
        epilog="""The format for the JSON file is a list of a list of pairs.
    [["target-link-name", "source-file-name"],...]""",
    )
    parser.add_argument("source", help="The directory of the source files.")
    parser.add_argument("target", help="The directory of the target links.")
    parser.add_argument(
        "files",
        type=FileType(mode="r"),
        help="JSON file containing a list of files to be linked.",
    )
    args = parser.parse_args()

    #
    # Setup
    #
    source_dir = args.source
    target_dir = args.target
    link_list = load(args.files)
    args.files.close()

    #
    # Check source & target dirs
    #
    if not isdir(source_dir):
        exit("{} is not a directory.".format(source_dir))
    if not isdir(target_dir):
        exit("{} is not a directory.".format(target_dir))

    #
    # Start install
    #
    if len(link_list) == 0:
        exit("Oops: no files to link")

    for fp in link_list:
        if len(fp) != 2:
            print(
                "Skipping "
                + str(fp)
                + ". Expected list like ['source-file', 'target-file']."
            )
            continue

        source_f = join(source_dir, fp[0])
        target_f = join(target_dir, fp[1])

        if not exists(source_f):
            print("\nOops: {} does not exist. Check for typo in files arg.\n".format(source_f))
            continue

        if isfile(target_f) and not islink(target_f):
            rename(target_f, target_f + ".org")
            print("Moved " + target_f + " to " + target_f + ".org")

        if islink(target_f):
            print(target_f + " is a sym link. No change to make.")
        else:
            symlink(source_f, target_f)
            print(target_f + " -> " + realpath(source_f))


if __name__ == "__main__":
    main()
else:
    print("** Did not plan on being imported **")
