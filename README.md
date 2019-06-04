# vga-blog
This is a retro-styled static site generator inspired by <a href="https://github.com/jmpavlick/hypertextual">Hypertextual</a>. Posts may be written as .txt or .htm files. A chronological list of posts and an RSS feed are automatically maintained.

## How to use:
- Put your blog posts in the `raw_post/` directory.
  - The format of the input blog posts is raw `.txt` or `.htm` files.
  - The first line must be the post's title, and the second line must be the post's date written as ISO 8601.
- Put the static part of your site in the `site/` directory.
- Run `vgablog.py`.
- Your blog will be generated into a freshly created `site/blog/` directory.  Navigation is generated too:
    - a link to the most recent post
    - a chronological list of posts
    - a RSS feed

## Example:
https://edlinfan.neocities.org/
