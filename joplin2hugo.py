import os
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
import logging
from os import path as path
from glob import glob
import re

def get_agruments():
    parser = ArgumentParser(description="This is a simple python converter script to convert Joplin Markdown exports to Hugo site generator as content.",
                            formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("joplin_in", help="Directory where joplin markdown is saved")
    parser.add_argument("content_path", help="Hugo content base path used in `hugo new content` command, content will be named by the script")
    parser.add_argument("--hugo_base_dir", help="Hugo site base directory", default="..")
    parser.add_argument("--debug", help="debug_flag", action='store_true')
    args = parser.parse_args()
    logging.basicConfig(level=logging.DEBUG if args.debug else logging.INFO,
                        format='%(levelname)s: %(message)s')

    logging.debug(f"Received args={args}")
    return args.joplin_in, args.content_path, args.hugo_base_dir

def title_2_file_name(title):
    ret = title
    ret = ret.replace(" - ", "-")
    ret = ret.replace(".", "-")
    ret = ret.replace(" ","-")
    return ret

def re_replace_and_write(input_re, replace_with, data, to_file):
    sed = re.compile(input_re, re.MULTILINE)
    to_file.write(sed.sub(replace_with, data) + "\n")

def main():
    joplin_in, content_path, hugo_base_dir = get_agruments()

    # get all md files from joplin_in/Blog dir
    src_md_file = glob(path.join(joplin_in, "Blog", "*.md"))
    assert len(src_md_file) == 1, f"There should be only one md file inside {joplin_in}/Blog"
    src_md_file = src_md_file[0]
    logging.info(f"Found {src_md_file}")

    # get resources dir
    resources_dir = path.join(joplin_in, "_resources")
    assert path.isdir(resources_dir), f"Resources dir f{resources_dir} doesnt exists"

    # content page name
    title = path.basename(path.splitext(src_md_file)[0])
    target_md_file = title_2_file_name(title)
    logging.debug(f"title = {title}")
    logging.debug(f"content_md_title = {target_md_file}")

    # create new content page in hugo
    target_md_file = f"{content_path}/{target_md_file}/index.md"
    cmd = f"hugo new content {target_md_file} -s '{hugo_base_dir}'"
    logging.info(f"Executing '{cmd}'")
    assert os.system(cmd) == 0, "Command execution failed"
    target_md_file = path.join(hugo_base_dir, "content", target_md_file)
    assert path.isfile(target_md_file), f"{target_md_file} doesnt exists"

    # Add title string to target_md_file
    with open(target_md_file, "r") as f:
        data = f.read()
    with open(target_md_file, "w") as f:
        re_replace_and_write("^title.=.*", f"title = \"{title}\"", data, f)
    logging.info(f"Added \"{title}\" to content page")

    # append src_md_file to target_md_file with url changed
    with open(src_md_file, "r") as f:
        data = f.read()
    with open(target_md_file, "a") as f:
        img_re = "\.\.\/_resources/"
        re_replace_and_write(img_re, "", data, f)
    logging.info(f"Updated {target_md_file} with {src_md_file}'s data")
    logging.info("Replaced img urls")

    # Copy images if any from resources_dir to content dir
    _from = path.join(resources_dir, "*")
    to = path.dirname(target_md_file)
    cmd = f"cp -v {_from} {to}"
    logging.info(f"Copying images from {_from} to {to}")
    assert os.system(cmd) == 0, "Moving failed"

    # suggest removing the src dir
    logging.info("Recommending to remove 'Blog' and '_resources' dirs")
    cmd = "rm -rIv {path.dirname(src_md_file)} {resources_dir}"
    assert os.system(cmd) == 0, "Removal failed"

    return

if __name__ == "__main__":
    main()
