#!/usr/bin/python
import os
import datetime
import PyRSS2Gen

kInDir = "raw_post"
kTmplDir = "template"
kBlogDir  = "site/blog"
kPostsDir  = "site/blog/posts"

def main():
    postlist = posts()
    archive(postlist)

def posts():
    postlist = []

    # Create the output directory if it doesn't already exist
    os.makedirs(kPostsDir, exist_ok=True)

    postHeader = getTemplate("posthead.htm")
    postFooter = getTemplate("postfoot.htm")
    postTitle = getTemplate("postitle.htm")

    for fInName in os.listdir(kInDir):
        fInPath = os.path.join(kInDir, fInName)
        fOutName = os.path.splitext(fInName)[0] + ".htm"
        fOutPath = os.path.join(kPostsDir, fOutName)
        fIn = open(fInPath, "r")
        fOut = open(fOutPath, "w")

        # emit post header
        fOut.write(postHeader)

        # parse & consume 1st input line -> title
        title = fIn.readline()
        # parse & consume 2nd input line -> date
        date = fIn.readline()
        # store (title, date, filename)
        postlist.append((title, date, fOutName))

        # emit post titlebox
        fOut.write(postTitle % (len(title) + 4, title, date))

        # write remaining lines
        # wrapping with <pre></pre> unless input was a .htm file
        if not fInName.endswith(".htm"):
            fOut.write("<pre>\n")
        while 1:
            line = fIn.readline()
            if not line:
                break
            fOut.write(line)
        if not fInName.endswith(".htm"):
            fOut.write("</pre>\n")

        # emit post footer
        fOut.write(postFooter)

        fIn.close()
        # close post htm file
        fOut.close()

    return postlist

def archive(postlist):
    archiveHeader = getTemplate("archhead.htm")
    archiveFooter = getTemplate("archfoot.htm")
    archiveDiv = getTemplate("archdiv.htm")
    redirectHtml = getTemplate("redirect.htm")
    
    # sort the (title, date, filename) data structure by date
    # (ASCIIbetical descending)
    postlist.sort(key=lambda t: t[1], reverse=True)

    # create redirect htm file
    fRdOutPath = os.path.join(kBlogDir, "index.htm")
    with open(fRdOutPath, "w") as f:
        # emit filename of newest post
        f.write(redirectHtml % postlist[0][2])

    # create archive htm file
    fOutPath = os.path.join(kPostsDir, "index.htm")
    fOut = open(fOutPath, "w")

    # create archive rss feed
    rss = PyRSS2Gen.RSS2(
        title = "VGA Blog",
        link = "http://example.com/blog",
        description = "",
        lastBuildDate = datetime.datetime.now())

    # emit archive header
    fOut.write(archiveHeader)

    # for each datum
    for tup in postlist:
        (title, date, filename) = tup
        date = date.strip()
        # emit div
        s = archiveDiv % (date.strip(), filename, title.strip())
        fOut.write(s)
        # emit rss entry
        rss.items.append(
            PyRSS2Gen.RSSItem(
                title = title,
                link =
                    "https://example.com/blog/posts/%s" % filename,
                description = "",
                pubDate = datetime.datetime.strptime(date, "%Y-%m-%d")))

    # emit archive footer
    fOut.write(archiveFooter)
    # close archive htm file
    fOut.close()
    # write rss feed
    with open(os.path.join(kBlogDir, "rss.xml"), "w") as rssFile:
        rss.write_xml(rssFile)

def getTemplate(name):
    path = os.path.join(kTmplDir, name)
    with open(path, "r") as f: contents = "".join(f.readlines())
    return contents

if __name__ == "__main__":
    main()
