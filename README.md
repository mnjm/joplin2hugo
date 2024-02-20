# Joplin to Hugo

This is a simple python converter script to convert Joplin Markdown exports to Hugo site generator as content.

Works with Joplin's Markdown save.

## How to

```
usage: python3 joplin2hugo.py [-h] [--hugo_base_dir HUGO_BASE_DIR] [--debug] joplin_in content_path

This is a simple python converter script to convert Joplin Markdown exports to Hugo site generator as content.

positional arguments:
  joplin_in             Directory where joplin markdown is saved
  content_path          Hugo content base path used in `hugo new content` command, content will be named by the script

options:
  -h, --help            show this help message and exit
  --hugo_base_dir HUGO_BASE_DIR
                        Hugo site base directory (default: ..)
  --debug               debug_flag (default: False)
```

### Intended use
This repo is intended to be used as submodule to your hugo git repo but straight cloning/download should also work.
You can add it as submodule using `git submodule add https://github.com/mnjm/joplin2hugo.git`

### Example

`python3 joplin2hugo.py ~/joplin-save-dir posts/ --hugo_base_dir ~/hugo_site`

Assuming there is a Joplin markdown file named `An Another Blog.md` saved in `~/joplin-save-dir/Blog` and its associated images in `~/joplin-save-dir/_resources`. Upon executing the above command, the content will be saved in `~/hugo_site/content/posts/An-Another-Blog/index.md` with images in the same directory, and URLs adjusted.
