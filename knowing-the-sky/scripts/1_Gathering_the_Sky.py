# ---
# jupyter:
#   jupytext:
#     cell_markers: '"""'
#     comment_magics: false
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.16.4
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %% [markdown]
"""
## Lesson 1: Gathering the Sky
#### Learning Objectives:
After completing this lesson, users will be able to:
1. Implement multiple methods for obtaining data from online NASA resources using Python
2. Describe positive file management practices
3. Utilize Python packages to manipulate file compression and placement

_Python libraries introduced in this lesson:_ [`os`](https://docs.python.org/3/library/os.html), [`pathlib`](https://docs.python.org/3/library/pathlib.html), [`astroquery`](https://astroquery.readthedocs.io/en/latest/index.html), [`requests`](https://docs.python-requests.org/en/latest/index.html), [`gzip`](https://docs.python.org/3/library/gzip.html), [`io`](https://docs.python.org/3/library/io.html), [`tarfile`](https://docs.python.org/3/library/tarfile.html)
"""

# %% [markdown] jp-MarkdownHeadingCollapsed=true
"""
### Introduction
Prior to the invention and widespread adoption of personal clocks, many cultures looked to celestial movements as a way to navigate and track time, including Native American tribes. Some tribes, such as the Shinnecock, traditionally look to the moon as their main timekeeper, incorporating additional information from observations of specific plant species blooming or fruiting, or the behavior of animals such as the geese migrating south. Similarly, the Salish would observe the appearance and behavior of various bird species as well as use the changing positions of stars to track the passage of time. During his anthropological research of the Salish people, Claude Schaffer conducted interviews and made observations of how time and the seasons were recorded. In his notes, Schaffer refers to a constellation known as Čspéʔl̓č̓s Kʷkʷusm̓ which translates to _seven stars_. From the perspective in the Salish territory (which mainly covers Western Montana), this constellation moves across the sky and ends the night directly overhead when day breaks. As the seasons progress, the constellation starts the night at different areas of the sky. These changes in position mark the passing of the seasons as Čspéʔl̓č̓s Kʷkʷusm̓ made it's journey to the zenith (and therefore the night) longer during the winter. Schaffer interpreted that the _seven stars_ constellation is the same set of stars referred to as the _Big Dipper_ by Western astronomy.
However, along with this well described account of the movement of the Čspéʔl̓č̓s Kʷkʷusm̓, there is a shorter, more vague, but equally as interesting note:

> There was a group of three stars that rose from the place that was between the sun and the moon and it never changed its positon of rising.

It is here that we will begin our investigation. Which three stars are being referred to? How can we use available datasets to determine this? We'll begin by learning the basics of acquiring data using Python.
"""

# %% [markdown]
"""
### Acquiring Data

Unless you're doing pure simulations --- and sometimes even then --- you'll usually need source data for scientific programming. Often the seemingly simple steps of finding, acquiring, and figuring out how to 'open' data can take as much time as analyzing it. Many of us have been spoiled by modern search engines and data standardization; but digital astronomical data predates the even the existence of modern computers! Fortunately, and by the collective effort of tens of thousands of computer programmers and scientists, many excellent open source libraries and tools exist to make these tasks easier.

The technology that underlies the following examples is called the Hypertext Transfer Protocol, or, more commonly, just HTTP -- an abbreviation that's probably familiar to you from your browser URL bar. HTTP is the primary "application layer" protocol used to access content on the Internet and to interact with online services, including cloud services. Applications use HTTP by issuing "requests" of various types, most commonly `GET` (retrieve data), `PUT`, and `POST` (which both send data). Servers respond to HTTP requests by sending HTTP "responses", which can contain both data and metadata about the response. HTTP metadata are called "headers".

Most popular programming languages offer ways to make HTTP requests and interpret HTTP responses, and Python is no exception. One of the best Python libraries for doing this is unsurprisingly called `requests`.
"""

# %% [markdown]
"""
#### Web Data: `requests`

Sometimes you'll find that the files you need are accessible via plain web links (URLs). If it's just a handful of files, a web browser may do the job just fine. If there are more --- especially if the URLs are regularly constructed, in a list you can load into memory, or subject to change based on other parts of your program --- it's often better to do it with code.

`requests` is a popular library for making HTTP requests in Python. This first example is *very* easy.  We'll look at some more complex uses of `requests` in later modules.

**todo: i'd like a more complex example --- something where we can use a for loop --- maybe in an exercise? hard to make it relevant for the first section, is the issue...but we could get other data they need.**

We'll need information on stars people can see without optical equipment in order to identify the three stars in Schaffer's notes, so let's grab a copy of the Bright Star Catalog (BSC), a popular catalog of stars visible from Earth with the naked eye.
"""

# %%
import requests

# url for the bright star catalog
bright_star_url = "http://cdsarc.u-strasbg.fr/viz-bin/nph-Cat/tar.gz?V/50"

# %% [markdown]
"""
`requests.get` downloads data from a URL into a `requests.Response` object, which contains both the file's contents and any headers sent by the server. This won't write a file to disk, we'll talk more about that in the **File Management** section below.
"""

# %%
bright_star_response = requests.get(bright_star_url)

# %% [markdown]
"""
It's good to check whether you actually got the file before moving on. `Response.raise_for_status`
will raise an exception if the server returned a 404 (missing) or other error code. Otherwise, it won't return anything.
"""

# %%
bright_star_response.raise_for_status()

# %% [markdown]
"""
`Response.content` contains the body of the response -- in this case, the catalog file.
Sometimes you can easily work with it in memory, especially if it can be decoded
as plain text. That isn't the case here, because it's a compressed `.tar.gz` file.
We'll look at how to decompress it later.

Note that you don't want to print the whole response out in the Notebook, because it's 740 kilobytes -- hundreds of pages of binary gibberish!
There are nevertheless some good ways to get some important information about it without getting too complicated:
"""

# %%
print(f"The response content is {len(bright_star_response.content)} bytes long.")
print(f"It is a Python {type(bright_star_response.content)} object.")
print(f"Here are the first 20 bytes of the response: {bright_star_response.content[:20]}.")
print(f"The server says it is a {bright_star_response.headers['Content-Type']} file.")

# %% [markdown]
"""
#### Catalog Data: astroquery

Before we move on with our exploration of the bright star catalog, we should first discuss astronomical catalog data. Many data aren't so easy to grab from plain URLs like we did above. Let's say we wanted to get some detailed images of a 
region of the sky from the Herschel mission. The Herschel image dataset is extremely large, and 
impractical to download in whole for most purposes. Fortunately, Herschel's images, like many data sets, 
are accessible via an Application Programming  Interface (API); unfortunately, APIs can be complicated to 
use, and every API is different. `astroquery`, an `astropy` affiliate package, is a grab-bag of high-level interfaces to astronomy APIs that attempt to solve this problem. To practice, let's get an image of Orion with the help of `astroquery`'s 
`esasky` module.

**note: consider this a placeholder**
"""

# %%
from astroquery.esasky import ESASky
maps = ESASky.query_object_maps('Alnitak', missions=['Herschel'])
maps

# %%
# get the URLs
maps[0]['product_url']

# %%
# TODO: download a URL

# %%
# TODO, maybe, if we wanted to show more cataloging...

# import astropy.coordinates as coord
# from astroquery.simbad import Simbad
# result_table = Simbad.query_region(coord.SkyCoord("05h35m17.3s -05h23m28s", frame='icrs'), radius='1d0m0s')

# %% [markdown]
"""
### File Management

When working with scientific data, you'll often find yourself working with a large number of files, or with very large files. Both of these can present difficulties! Large numbers of files are difficult to organize. Individually, large files can take a long time to download and open, and use up a lot of local storage space. Processing them without great care can use up a lot of your computer's working memory (RAM), leading to sluggish performance or even crashes. 

These problems are made worse by the fact that scientific files often have long, complicated filenames. Although they can contain a lot of useful information, they are hard to read until you are very used to a specific data set. 

It's also likely you'll find yourself writing a lot of files containing data you've processed with your own code.

This all means that good file management is very important. It helps you avoid spending lots of time poking around and opening random files to find what you're looking for -- or, worse, losing your work.

So, what is good file management? A lot of it comes down to personal preference or specific project needs, and there are many tools for it that you may find useful, but the most straightforward thing to do is to leverage the built-in capabilities of your filesystem, and that's what we'll do on this project. Filesystems are great! Every computer and every programming language knows how to work with them, and it is easy to click through folders in a file manager application and explore them with code. Here are some guidelines that work for most people:
* Keep files for a specific project in a single folder 'tree'.
* Name and organize folders in a way that makes sense to you -- keep similar files together and give folders names you will remember.
* Similarly, choose a clear, expressive naming convention for any files you write yourself.
* Don't put too many files in a single folder -- this makes it hard to browse and can also reduce performance. 100 is about the limit.
* Keep code and data files in separate folders.
* Make sure you know where new files are going. For example, when you download a file from the Internet using your browser, it often goes into a Downloads folder. It's good to know where that is in your filesystem so that you can actually use those files.
* Keep new files that you write (output data) separate from files you've acquired from other sources (input data).

The Python ecosystem, including just the Standard Library, has many tools to work with local filesystems. Let's look at a couple of common patterns.
"""

# %% [markdown]
"""
#### Dealing With Compression

We have the Bright Star Catalog (BSC) as an in-memory object -- not a file on disk. If you were to shut down this notebook right now, then the catalog information that was downloaded would be lost. To use it in other scripts, we need to save it to disk.
The BSC file is also compressed using `gzip`, a common compression algorithm; it is _also_ 'wrapped' using `tar`, a common utility for compacting multiple files into a single file. These will make it hard to use straightforwardly, so let's "ungzip" and "untar" the file save it to disk. This will also show you a number of useful patterns for working with compressed files and directories in Python! (Uncompressed astronomical data and catalogs are often quite large. But they also often compress quite efficiently for reasons that are beyond the scope of this tutorial to explain. For this reason, astronomical data are routinely stored and transmitted in a lossless compression format like `gzip`.)
"""

# %%
# Python's built-in package for handling gzip compression
from gzip import GzipFile

# BytesIO is an object that allows you to interact with an object
# in memory as if it were a file
from io import BytesIO

# Python's built-in package for handling tar files
from tarfile import TarFile, TarInfo

# %%
# BytesIO must be initialized with a bytes object -- which we have in
# bright_star_response.content!
virtual_file = BytesIO(bright_star_response.content)

# now we can initialize the GzipFile object using that virtual file.
gzip_file = GzipFile(fileobj=virtual_file)

# and now we can create an object to untar it!
tar_file = TarFile(fileobj=gzip_file)
files = tar_file.getmembers()
files

# %% [markdown]
"""
#### Fixing Directory Structures

You'll note that these tar files are wrapped up in a less-than-optimal directory structure --
the period at the beginning of the path ("./") means that if you try to just extract the whole archive with `.extractall()`,
you'll get errors (because '././ReadMe', etc., are not legal directory names).
You'll also note that two of the files are still gzipped as indicated by the ".gz" file extension!
So let's make a directory to write them into, and then write them by name,
un-gzipping the ones we would prefer not to be gzipped as we go.
"""

# %% [markdown]
"""
`pathlib.Path` objects are one of Python's most useful tools for working with the filesystem.
Each one is an abstraction for a specific file or directory. They can be combined easily
to put files in a specific directory, and have a lot of convenience methods for manipulating
their names and reading or writing from disk.
"""

# %%
from pathlib import Path
import os

# this represents a path to a subdirectory of your working directory called 'bright_star_directory'
catalog_directory = Path("bright_star_directory")

# it probably doesn't exist yet, so let's make it -- the `exist_ok` argument prevents the function
# from throwing an error if you've run this cell before and the directory already exists
catalog_directory.mkdir(exist_ok=True)

# let's verify it's there
os.listdir()

# %%
# pathlib.Path objects are one of Python's most useful tools for working with the filesystem.
# each one is an abstraction for a specific file or directory. they can be combined easily
# to put files in a specific directory, and have a lot of convenience methods for manipulating
# their names and reading or writing from disk.

# this represents a subdirectory of your working directory called 'bright_star_directory'
catalog_directory = Path("bright_star_directory")
# it probably doesn't exist yet, so let's make it -- the exist_ok argument is in case 
# you've run this cell before
catalog_directory.mkdir(exist_ok=True)
# let's verify it's there
os.listdir()

# %% editable=true slideshow={"slide_type": ""}
for file in files:
    # get a buffer that contains the file data and read bytes out of it
    file_bytes = tar_file.extractfile(file).read()
    # define the actual path we want to write the file to.
    # the '/' operator causes Python to combine the paths in the same way
    # writing a / on the command line would.
    # the 'replace' call makes sure we don't write an un-gzipped file
    # with a '.gz' extension, which can cause issues.
    target = catalog_directory / Path(file.name.replace('.gz', ''))
    print(target)
    # un-gzip if necessary:
    if file.name.endswith('gz'):
        file_bytes = GzipFile(fileobj=BytesIO(file_bytes)).read()
    # 'with opehttp://localhost:8888/notebooks/topst_scratch/getting_data.ipynb#n(filename) as stream' is a very common pattern in Python.
    # the 'with' means that it is a context manager. the indented block
    # below it will operate using a temporary 'stream' argument that will
    # automatically clean itself up when the block finishes running. this
    # can prevent a lot of mess.
    # 'wb' means that we are writing to the file, and writing in binary mode.
    with open(target, 'wb') as stream:
        stream.write(file_bytes)

# %%
# and just for fun, let's check to make sure that worked, using the same
# pattern as before, but in read mode:
with open('bright_star_directory/ReadMe') as stream:
    print(stream.read())

# %%
from astropy.io import ascii

table = ascii.read('bright_star_directory/catalog', format='mrt')

# %% [markdown]
"""
Great! Now we can move on to ways to use some of these files in the next module.
"""
