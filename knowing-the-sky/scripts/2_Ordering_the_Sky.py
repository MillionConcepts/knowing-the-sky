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
## Lesson 2: Ordering the Sky
#### Learning Objectives:
After completing this lesson, users will be able to:
1. Describe array and table data types and their uses
2. Utilize python packages to open array and table data as represented by the data providers
3. Index and manipulate data within arrays and tables
4. Load and manipulate astronomical data into formats compatible with standard Python libraries

_Python libraries introduced in this lesson:_ [`astropy.io.fits`](https://docs.astropy.org/en/stable/io/fits/index.html), [`matplotlib`](https://matplotlib.org/stable/), [`numpy`](https://numpy.org/doc/stable/), [`pandas`](https://pandas.pydata.org/docs/)
"""

# %%
# Python Standard Library imports
from pathlib import Path

# third-party imports
from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# %% [markdown]
"""
### Introduction
In our last lesson, we aquired data from online NASA repositories to begin an investigation to identify which stars were being referred to by the Salish individual(s) interviewed by Claude Schaffer:

>There was a group of three stars that rose from the place that was between the sun and the moon and it never changed its positon of rising.

In this lesson, we'll learn how to read that data into python standard objects and the basics of how to work with them. The two main types of data we'll cover in this lesson are arrays and tables.
"""

# %% [markdown] jp-MarkdownHeadingCollapsed=true
"""
### Arrays

Arrays are one of the most important data structures in scientific programming, and, for that matter, practical mathematics more generally -- they are a basic pattern used in many systems and cultures. Computers are very good at working with them, so knowing how to manipulate them effectively is extremely powerful. If you are reading this, it is entirely possible you have extensive experience with array data. Things may be different in Python than other languages, though, so we recommend not skipping it.

#### What is an array?

Basically, an array is simply a regular grid of 'elements', which are often but not always numbers. It can be 1-D, 2-D, 3-D, or even more. A 1-D array is a lot like a list. 

You can access elements in an array by coordinates, which means that they work like coordinate spaces. This is *very* useful for scientific programming. You can also perform mathematical operations on an entire array at once, which is both convenient and typically much faster than performing the same operations on each element one-by-one.

(footnote for the mathematically inclined): an array is *not* a vector, matrix, or tensor, but it can be used to *represent* a vector, matrix, or tensor. 

#### How do you work with arrays in Python?

`numpy` is the most common library for creating and manipulating arrays. Most scientific programs use `numpy` at some point, partly because many other libraries use it 'under the hood'. A very important point is that raster images (images made up of pixels, as opposed to vector images) can always be converted to and from arrays, which means that arrays let you do very powerful image manipulation. Let's start with a very quick introduction to the most important parts of the `numpy` library.
"""

# %% [markdown]
"""
First, let's make a little 4x4 triangular array we can play with:
"""

# %%
triangle = np.tri(4)
triangle

# %% [markdown]
"""
You can access single elements of an array by entering their coordinates in slice `[]` notation -- much 
like a Python list but with possible extra dimensions.

A reminder that python is "zero-indexed" meaning when you are counting elements in an array, list, etc. You start from 0 not 1. (This is one of the major differences between Python and MatLab!)

For a 2-D array, the row (y-axis) always goes first, then the column (x-axis). You get exactly the elements you specify, which means that yif you don't enter a number for every dimension, you can pick more than one element at a time. For instance, `[0]` means "all the elements with 0-coordinate on the y-axis", or, in other words, the first row. `[:,0]` (`:` is numpy's placeholder) means "all the elements with 0-coordinate on the x-axis", and returns the first column. If you specify a number for every dimension you can get just a single elements: `[0,0]` means "the number
in the upper-left corner".

Let's test this in action:
"""

# %%
triangle[0], triangle[:, 0], triangle[0, 0]

# %% [markdown]
"""
You can also specify ranges. For instance, `[0:2, 0:2]` means "give me the square in the upper left corner of size (2,2)". 

Note here that the range is exclusive of the final index you're entering. In other words, you'll get rows/columns indexed 0-1, not data from row/column 2.
"""

# %%
triangle[0:2, 0:2]

# %% [markdown]
"""
When working with arrays you read in from data, you won't always know what shape it is because you won't have made it like we did above. In numpy, `shape` can be used to return how many elements an array has along each of its dimensions. It's important to know an array's shape for a variety of reasons, but on eo fhtem is to know exactly how much there is to slice. Let's return our array's shape:
"""

# %%
triangle.shape

# %% [markdown]
"""
Remember that Python is 0-indexed, and that `.shape` returns the _number of elements_, not the index. That means this will throw an error:
"""

# %% editable=true slideshow={"slide_type": ""} tags=["raises-exception"]
triangle[4]

# %% [markdown]
"""
Slice notation can also be used to set elements. If you do the same things we've been doing, but add an assignment (`=`), you can set all the values to a number -- or even set to the contents of another array, if it's the right size.

This will set all the elements of the first row to 2:
"""

# %%
triangle[0] = 2
triangle

# %% [markdown]
"""
If you do an arithmetic operation on an array with a scalar (like a single number), it will apply that operation to ever element of the array. Unlike slice assignment, this does not modify the array in place unless you use a special operator. It retuns a copy, leaving the original array unchanged. 

For instance, to get a copy of the array with every element doubled:
"""

# %%
double = triangle * 2
double

# %% [markdown]
"""
Doing arithmetic using two array perfoms the operation elementwise -- elements with matching indexes from each array. Let's create a random array to test this with. We'll use [`np.random.randint`](https://numpy.org/doc/stable/reference/random/generated/numpy.random.randint.html) to create an array of random whole numbers between 0-10 the same shape as triangle:
"""

# %%
randarray = np.random.randint(0,10,size=triangle.shape)
randarray

# %% [markdown]
"""
and then multipy it by triangle...
"""

# %%
randarray * triangle

# %% [markdown]
"""
This doesn't work if you try to multiply two arrays with mis-matched shapes! Let's test this by trying to multipy a 3 x 3 array of 3 by triangle:
"""

# %% editable=true slideshow={"slide_type": ""}
three = np.full((3, 3), 3)
three

# %% editable=true slideshow={"slide_type": ""} tags=["raises-exception"]
three * triangle

# %% [markdown]
"""
As expected, we get an error. But if we slice our larger array to be the same shape as our 3x3 array we can multiply them:
"""

# %%
three * triangle[0:3, 0:3]

# %% [markdown]
"""
You can even do assignment like this! This will multiply the upper-left 3x3 square of `triangle` by `three`, in place:
"""

# %%
triangle[0:3, 0:3] = three * triangle[0:3, 0:3]
triangle

# %% [markdown]
"""
Finally, you can also slice an array _with_ another array. This can get complicated fast: `numpy` calls it "fancy indexing" for a reason. However, there are a lot of very simple ways to use it. This most common one is to just select all the elements of an array tha tmeet some condition. For instance, this means "pick all the elements of triangle that are less than 3":
"""

# %% editable=true slideshow={"slide_type": ""}
triangle[triangle < 3]

# %% [markdown] editable=true slideshow={"slide_type": ""}
"""
### Loading images

Ok, intro examples over; let's take a look at something more practical. We'll load a FITS image into memory using `astropy.io.fits` and look at some basic ways to use it.

FITS files are the most popular standard for astronomy data and are becoming increasingly popular in planetary science data. They consist of multiple header-data units or HDUs. Each HDU includes a header area containing metadata and a data area containing, unsurprisingly, data. This data can be an array or a table. In  this case, all the HDUs are arrays. `astropy.io.fits` loads FITS file into an `HDUList` object, whichin most cases can simply be treated as a Python list with  some extra useful methods, like `.info()`.

_Remember_: at the beginning of this notebook we imported `astropy.io.fits` as `fits` so we can call it like that here.
"""

# %% editable=true slideshow={"slide_type": ""}
# TODO: placeholder image

hdul = fits.open('placeholder_images/e23456-nd-t0060-b00-f0008-r.fits')
hdul.info()

# %% [markdown]
"""
As you can see from the () dimensions entry, HDU 0 contains no actual data -- it's a placeholder to help organize the rest of the file. HDU 1, however, contains an actual array. Let's go ahead and get the data from it:
"""

# %%
hdu = hdul[1]
image = hdu.data
image

# %% [markdown]
"""
### Exploring arrays

As we saw earlier, the representation `numpy` provides for arrays is excellent for small arrays. Unfortunately, as we can see here, for large arrays, it doesn't really tell you much except the data type **todo: should we have a section on data types?** and what's in the corners. Fortunately, Python offers many tools for summarizing and visualizing arrays. 

#### Dealing with nonfinite values

Before we start exploring, we need to deal with the fact that lots of scientific data -- including this image -- contain 'nonfinite' values: `nan` (not-a-number, sometimes called 'null', used for missing or invalid entries), `inf` (infinity), and `-inf` (negative infinity). This means many statistical tools will fail on them out of the box: what, after all, is the mean of 2, 3, and not-a-number? There are several ways to work with data despite nonfinite values. The most powerful tool `numpy` provides is the masked array, which allows you to ignore specific elements and work with the array just like you would otherwise. A caveat: not all libraries 'respect' masked arrays, so you may have to do fancier tricks when working with some tools. However, many do. We'll show a common trick for dealing with libraries that don't a little further down.
"""

# %% [markdown]
"""
Here you'll see due to the `nan` values `np.mean` does not provide a useful result on the original array:
"""

# %%
np.mean(image)

# %% [markdown]
"""
However, if we construct an array that masks all nonfinite elements, we're in business:
"""

# %%
image = np.ma.masked_invalid(image)
np.mean(image)

# %% [markdown]
"""
Let's go ahead and also mask everything below 0 (0 is valid minimum for this image). The mask is just an array of boolean (True/False) values, and you can slice an assign it just like any other array. We'll use the fancy indexing trick from above:
"""

# %%
image.mask[image < 0] = True

# %% [markdown]
"""
#### Summarizing arrays

`numpy` offers many built-in tools that are good for simply describing arrays as well as performing mathematical operations. Commonly-useful ones include `std` (standard deviation), `mean`, and `median`. We just looked at `mean`. Let's look at the others.
"""

# %%
(
    np.std(image), 
    # using the version from the np.ma namespace because of a little glitch in core numpy
    np.ma.median(image)
)

# %% [markdown]
"""
These can also be used along an individual axis. for example, if you'd like the mean of every column:
"""

# %%
np.mean(image, axis=0)

# %% [markdown]
"""
#### Outside of numpy

For really serious statistical work, it's often useful to turn to `scipy.stats`, which has a wide range of useful tools. `scipy.describe` is great for getting a bunch of basic descriptive statistics at once, *usually*...
"""

# %%
from scipy import stats
stats.describe(image)

# %% [markdown]
"""
Hmmm...that's a lot of nans, and it worked along only one axis, which probably isn't what 
we wanted. here's a little trick for getting just the unmasked elements of an array, 
'raveled' into a single dimension:
"""

# %%
valid = image[~image.mask]
stats.describe(valid)

# %% [markdown]
"""
### Visualizing arrays

Since many arrays are images, we often want to simply *look* at them. This, of course, can even be useful for arrays that _aren't_ exactly images. There are many ways to do this, but the `imshow` function from `matplotlib.pyplot` is one of the most straightforward: it simply plots a 1D, 2D, or 3D array on a grid. Let's use it to take a look at the image we just opened -- although the results may not be satisfying at first.
"""

# %%
plt.imshow(image)

# %% [markdown]
"""
Unfortunately, plt.imshow, by default, applies a linear 'stretch' to the image. Because the range
of values in this image are so wide, it doesn't look like much at all -- almost everything is at the
lower extreme of the color scale.
Let's write a little function that uses numpy to range-clip the image so we can look at it more clearly.

"""


# %%
def std_clip(array, sigma=1):
    # find the mean and standard deviation of the array
    mean, std = np.mean(array), np.std(array)
    # restrict the bounds of the array to (mean - sigma * std, mean + sigma * std)
    return np.clip(array, mean - sigma * std, mean + sigma * std)

clipped = std_clip(image)
plt.imshow(clipped)

# %% [markdown]
"""
Because we made the `sigma` variable as part of the function input, we can modify the stretch however we like. If we'd like a brighter (but noisier) image:
"""

# %%
really_clipped = std_clip(image, sigma=0.25)
plt.imshow(really_clipped)

# %% [markdown]
"""
Slicing works very well on arrays considered as images. For instance, you can use it to take a 'cutout' from an image to look at a portion in detail:
"""

# %%
plt.imshow(clipped[1000:1200, 1000:1200])

# %% [markdown]
r"""
## Tables
Tables are basically arrays.

### Ok, but what is a table, really?
A table is _like_ an array, with the following differences:
* 'Table' implies 2-D: it has rows and columns and nothing else.
* The columns of a table are also called 'fields', and have
    *meanings* that are distinct from one another: for instance, a table created from a radiometer 
    on a satellite might have fields representing time, latitude, longitude, and brightness temperature;
    individual rows would represent individual observations.
    * This is different from arrays, where, in general, every element has a roughly equivalent *meaning*, but in a different *place*.
* A table can have more than one data type: for instance, a star catalog might have a field representing
    right ascension in 64-bit floating-point numbers, and a field representing star names as strings.
* **todo: maybe not necessary here** A table also generally has an 'index', which can be 
    a numerical series that simply corresponds to row number, but can be something else
    entirely -- for instance, a table of personnel data might be indexed by employee ID number.

Like arrays, tables are of ancient origin and found in many forms in many contexts, but computers really like to work with them. Tables are even more widely used than arrays in general-purpose computing. Common examples include spreadsheets and SQL databases. The world runs on tables.

### Tabular file formats

#### Broad categories: binary vs. text
Tables can be stored in many formats. The two major _categories_ of format are binary and text tables. Text table formats store values as human-readable strings, like:

| RA | DEC |
| ------ | ----- |
| 17.222 | -12.301 |
| 17.223 | -12.311 |
| 17.222 | -12.323 |

These sorts of tables are relatively easy to look at and manipulate in spreadsheet programs or text editors -- unless they get so big that the program will refuse to load them!

By contrast, binary table formats store values as raw bytes. The number of bytes per entry depends on the underlying data type. They are poorly human-readable, but tend to use less disk space and be quicker to load than text tables. As 32-bit floating point numbers expressed in bytes, the preceding table might look like:
| | |
|-|-|
| \xa8\xc6\x89 | \xe5\xd0D\xc1 |
| \xb4\xc8\x89A | \xe5\xd0D\xc1 |
| \xa8\xc6\x89 | \x02+E\xc1 |

This is about 50% smaller in terms of data volume than the text version, but most people are not going to get much out of just _looking_ at it, and trying to manipulate it by copy-pasting would be fruitless. To use it, you need to load it into software that will translate it into meaningful numbers.

Some binary table formats simply contain encoded values. Other formats embed metadata along with the values (for instance, cell colors in an Excel file). These formats tend to be harder to read.

The upshot of all this is that really large tables -- tables that you wouldn't be able to visually scan, or maybe even successfully load, in a spreadsheet or text editor -- should almost always be stored in binary formats. Small tables are fine to store as text. If you're only planning to use them as intermediate data, though, small tables might also just as well be binary.

#### Characteristics of some specific formats
There are many, many tabular data formats. This is not an exhaustive list, but here are some common formats you are likely to encounter in planetary science and astronomy:

**DSV (delimiter-separated value)**

DSV is a family of text table formats that place each row on a separate line, and separates columns with a special delimiter character, usually a comma or a tab (a tab is represented by '\t' in most programming languages). Comma-separated tables are often called CSV, and tab-separated TSV. This is a CSV table:
```
satellite,1.002,-379,True
unknown,1.547,-22,False
```
Common file extensions for DSV files are .csv, .tsv, .txt, and .tab, but there are many others.


**FWF (fixed-width file)**

FWF is a text table format that places each row on a separate line, and separates columns by defining a specific 'width' -- number of characters -- for each column. These columns may also have whitespace 'padding' to make them easier to read (and for programs to figure out how to parse them if they don't have the definition available). FWF files were traditionally easier for programs to read than DSV files, but this is no longer true. In general, we recommend choosing DSV formats over FWF, because the delimiters make it easier for a wider variety of programs to parse them, they are usually a little smaller (because not every row has to be the same width), and you are less likely to make mistakes if you edit them manually. This is a fixed-width version of the DSV table above:
```
satellite 1.002 -379 True 
unknown   1.547 -22  False
```
.tab and .txt are common file extensions for FWF, but, like DSV, providers often exercise creativity.


**Excel (and other spreadsheet formats)**

Spreadsheet files are generally binary tables with embedded metadata that allow spreadsheet programs to retain formatting like fonts, cell colors, and sheet breaks. These are usually *proprietary* formats: although they can be reverse-engineered, the makers of the software do not publish specifications for them, and they are subject to change between software versions. This means that they are poorly portable and not very future-proof. For these reasons, we do not recommend exchanging scientific data in spreadsheet formats, and most spreadsheet software can easily export data in standard formats like CSV. Most spreadsheet formats have extensions that indicate the specific software used to produce them: for instance, Excel uses .xlsx or .xls.

**FITS**

FITS files, which were invented for astronomy but have seen widespread adoption in other scientific disciplines, can contain either binary or text tables (although FITS text tables are rarely used in practice). Because FITS files, as we discussed earlier, can have multiple HDUs, a single FITS file can contain multiple tables. FITS files usually have a .fits or .fit extension. We think FITS is one of the best ways to save tables due to its widespread support and mature, stable standard.

**PDS binary tables**

Many tabular data products in the PDS have ad-hoc structures they describe in external metadata. Standards differ between PDS3 and PDS4. In PDS3, structures can be defined in either their attached or detached PDS3 labels, or in an arbitrary number of distinct format (.fmt) files. In PDS4, binary table structure must be completely defined in a file's detached XML (.xml) label. Common extensions for these files include .dat and .tab.

**SQL databases**

**TODO: maybe skip this?**

**Parquet**

Parquet is a newer tabular interchange format that has seen wide adoption in industry and is increasingly common in scientific contexts. It is a _columnar_ format, which means that every field is stored in a distinct area and can be both compressed and readily accessed individually, which makes it very efficient for many purposes. We think Parquet is also an excellent choice for tabular data, especially very large tables that you don't want to load into memory all at once.

**general-purpose data formats**

Finally, while this category is much to broad to detail, it's worth noting that tables can also be represented in structured data formats that aren't specialized for tables, like Javascript Object Notation (JSON) and Extended Markup Language (XML). (In fact, Excel files rely in part on a compressed and modified version of XML!) Features of programming languages that save in-memory objects to disk, like Python `pickle` files or MATLAB .mat files, can similarly be used to store tables -- but then they can only be opened in that programming language! We don't recommend doing this unless you have a really good reason to.

**TODO: maybe something about headers?**


### Working with tables in Python

There are many packages for working with tabular data in Python. `pandas` is by far the most common, and it's what we'll mostly use in this book. `pandas` has built-in support for reading and writing a wide variety of table formats, but not all, so you'll sometimes need to use a helper package to load data into `pandas`. For instance, `pandas` can't read FITS tables, so you'll need to go through a specialty FITS library like `astropy.io.fits` or `fitsio`. Similarly, to read tables described in PDS metadata, you'll need to use a library like `pdr` or `pds4-tools`.

Also, as you saw in the previous lesson, people often compress table files 'monolithically', wrapping the whole file at once in a compression format like gzip. Some packages can decompress files like this automatically, but most can't, so you'll often need to decompress table files before you can use them.

`pandas` is very, very powerful; however, it has many features that don't follow a common idiom, so it needs to be used with care. Let's move on to some basic ways to use `pandas`. We'll use the Bright Star Catalog as our sample data.
"""

# %% [markdown]
"""
The BSC 'catalog' file has no file extension. However, if you open it in a text editor like Notepad or TextEdit (go ahead and do that now), you'd quickly see that:

1.  it has a text table, and
2.  it has no delimiter characters. (characters that show where each piece of data ends; like commas in a .csv file)

This means that the BSC catalog is a fixed-width file. (Each cell of table is an equal number of bytes)
You'd also notice that a lot of the fields appear to run togehter, which meake it somewhat hard to read -- both for humans and for `pandas`. Let's see what happns if we just use the `pandas` `read_fwf` function, which attempts to read a FWFby inferring the width of each field. The `header=None` argument tells `pandas` that the table has no column headers (data in the file before the start of the table that usually provides metadata or other information).

"""

# %%
bsc_take_1 = pd.read_fwf('bright_star_directory/catalog', header=None)
bsc_take_1

# %% [markdown]
"""
Ok, that looks _sort of_ reasonable. We can validate it by opening the specification of the table in bright_star_catalog/ReadMe in a text editor...

(Do that now so you can follow along and get experience looking at these kinds of documents. This kind of check is your main line of defense against using data you _think_ was read in properly but actually wasn't!)

And, unfortunately, if you scroll down to line 77, "Byte-by-byte Description of file", you'll see that it's not correct. The specification gives over 50 columns, while pandas detected only 14:
"""

# %%
bsc_take_1.columns

# %% [markdown]
"""
So, we have a couple of options here. If you take a look at the read_fwf() documentation [here](https://pandas.pydata.org/docs/reference/api/pandas.read_fwf.html), you'll see that you can pass a list of column specifications to read_fwf() in its colspecs argument.
However, we'd have to type all of those in, which is doable, but doesn't sound like much fun.

The easy direct download we used last time deceived us. So let's, instead, try to get this into `pandas` another way. [CNRS](https://www.cnrs.fr/en)'s Vizier service offers access to many complete catalogs. Let's see if it has the BSC.
"""

# %%
from astroquery.vizier import Vizier

catalogs = Vizier.find_catalogs('Bright Star Catalogue')
len(catalogs.keys()) # print the number of matching results

# %% [markdown]
"""
`Vizier.find_catalogs()` returns an `OrderedDict`. Each key in the dictionary will be a different catalog name. We used `len(catalogs.keys())` to print the length of the `keys()` attribute of the `OrderedDict` to know how many catalogs matched our search. It's got 19 catalogs related to 'Bright Star Catalogue'! Let's take a look at which specific one we want based on their descriptions:
"""

# %%
{
    c: r.description for c, r in catalogs.items()
}

# %% [markdown]
"""
It looks like 'V/50' is our target. Let's go ahead and download the whole thing from Vizier.
by default, Vizier will only return 50 rows, and we want the whole table, so let's 
make a new Vizier object with changed settings:
"""

# %%
big_vizier_fetcher = Vizier(row_limit=99999)
tables = big_vizier_fetcher.get_catalogs([catalogs['V/50']])
tables

# %% [markdown]
"""
Now we've got the catalog _and_ the notes in `tables`. Let's look at the catalog.
"""

# %%
tables[0]

# %% [markdown]
"""
This doesn't have quite as many columns as the 'full' version, but they're separated correctly,
and we don't need most of that metadata. 
you'll also note that `astroquery.vizier` returned this as an `astropy Table` object, but we'd rather
work with it in `pandas` so that works better with other python libraries we might use. `astropy Tables` can be easily converted to `pandas`, so let's do that:
"""

# %%
bsc = tables[0].to_pandas()
bsc

# %% [markdown]
"""
That's more like it! now, to prevent us from having to fetch it again,
Let's write it out in a format pandas will be able to understand more easily --
a simple CSV file.

*Note*: the `index=None` argument means "don't write the index as a separate column".)
"""

# %%
bsc.to_csv('bright_star_directory/catalog.csv', index=None)

# %% [markdown]
"""
Now, let's verify that we can read it in again:
"""

# %%
bsc_in = pd.read_csv('bright_star_directory/catalog.csv')
bsc_in

# %% [markdown]
"""
Great! It looks the same, with one notable exception: it reinterpreted some
of the columns as numbers, which also caused it to fill in blank spaces with NaNs. 
This is, in fact, a very good thing! For instance, if we'd wanted to look at all the
stars with Double Star Catalog designation (ADS) < 50, and had tried to do that on the 
original table, we would have gotten an error, because Vizier specified that column
as a string.
"""

# %% [markdown]
"""
Okay, so what can we do with this object?

First, a little vocab. This object is called a **DataFrame**.

This is one of the two basic `pandas` types. The other basic `pandas` type is a **Series**. Every field/column in a DataFrame is a Series. You can get the type of a python object with the `type()` function. Let's try that here to confirm what we've just learned:
"""

# %%
type(bsc_in), type(bsc_in['RAJ2000'])

# %% [markdown]
"""
Like `numpy`, `pandas` has a lot of tools for accessing elements of a table, but it works differently, principally because rows and columns can have names, not just numbers.

`pandas`' core tools for this are called **indexers**, and it has three of them:
`.at`, `.loc`, and `.iloc.`.

`.at` is rarely used, so we won't focus on it here. You can read more about it [here](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.at.html) in the pandas docs.

`.loc` fetches one or more elements by name: index name(s) first, column name(s) second. Like `numpy`, `pandas` uses `:` as a placeholder, and you don't have to give it both index and column. Let's look at some examples:
"""

# %% [markdown]
"""
This is how you would get the visual magnitude (Vmag) of stars 3000-3010:
"""

# %%
bsc_in.loc[3000:3010, 'Vmag']

# %% [markdown]
"""
You might be thinking: Well how did you know to type `'Vmag'` in the example above? In the examples where we printed the table itself we saw the column names. So you could have gotten them from them there, but what if you don't want to print the entire table? You could get a list of the column names using `.columns`:
"""

# %%
bsc_in.columns

# %% [markdown]
"""
Back to our `.loc` examples, this is how you would get everything in the 2001th row: (!Remember! the first row is 0)
"""

# %%
bsc_in.loc[2000]

# %% [markdown]
"""
This would return the entire Vmag column:
"""

# %%
bsc_in.loc[:, 'Vmag']

# %% [markdown]
"""
If you simply use slice notation right on the dataframe, this will work the same as using `.loc[:, column_name]`:
"""

# %%
bsc_in['Vmag']

# %% [markdown]
"""
You'll note that these last few gave `Series` objects rather than `DataFrame` objects. (Again if you'd like to test that just use `type()`). This is becuase we only got a single row or column at once. It's possible to slice a dataframe out of another dataframe. Because the columns have string names rather than numbers, you can do this by passing a list. Here is the visial magnitude and right ascension of stars 30-40, presented as a dataframe:
"""

# %%
bsc_in.loc[30:40, ['Vmag', 'RAJ2000']]

# %% [markdown]
"""
Like `numpy` arrays, you can select elements of a DataFrame that meet some special condition. The easiest way to do that is by using an expression that evaluates to either true or false. An expression like this is called a **logical predicate** and this one will produce a [boolean](https://www.w3schools.com/python/python_booleans.asp) Series giving us only very bright star with Vmag < 2:
"""

# %%
bright_condition = bsc_in['Vmag'] < 2
bright_condition

# %% [markdown]
"""
We can then pass that Series to `.loc` in order to select all the rows of the DataFrame for which that condition is True.
"""

# %%
bright = bsc_in.loc[bright_condition]
bright

# %% [markdown]
"""
Like arrays, the values in DataFrames can be easily plotted with matplotlib.
For instance, to make a scatter plot of Vmag vs. color (B-V) the following expression could be used:
"""

# %%
plt.scatter(bsc_in['Vmag'], bsc_in['B-V'])

# %% [markdown]
"""
Like arrays, you can assign values to particular elements of a DataFrame,
and you can do operations on big swaths of a DataFrame at once.

If we look at one of the values for in the 'Name' field, you'll note that there's some uncessary padding (extra spaces):
"""

# %%
bsc_in.loc[2, 'Name']

# %% [markdown]
"""
Here we can use the `.str` method of the `pandas Series` to treat each value in the 'Name' field as a string, and use `.replace` to switch out the sequences that match the regex pattern `' +'`. That plus sign tells the code to look for any sequence of more than one of the character it comes after, in this instance, a space. Of course, we use `regex=True` to tell `.replace` we are using a regex pattern otherwise it will look for the literal characters space then plus sign in the strings.
"""

# %%
bsc_in['Name'] = bsc_in['Name'].str.replace('  +', ' ', regex=True)
bsc_in.loc[2, 'Name']

# %% [markdown]
"""
Unlike arrays, you can add new columns as you please. Vmag is logarithmic in base ~2.512, so 
if you wanted a linear version of it for some calculation, you could do this:
"""

# %%
bsc_in['Vmag_exp'] = 2.512 ** bsc_in['Vmag']
bsc_in['Vmag_exp']

# %% [markdown]
"""
We don't really want to keep that though, so let's take a look at how we can easily drop that column:
"""

# %%
bsc_in = bsc_in.drop(columns='Vmag_exp')
bsc_in

# %% [markdown]
"""
You can also drop rows. There are a few entries in the BSC that don't have actual
coordinates. Let's clean them up quickly. Note that the '~' means 'not', so we're 
saying: "get rid of all the rows that don't have a real RAJ2000 value".
"""

# %%
bsc_in = bsc_in.loc[~(bsc_in['RAJ2000'] == '')]

# %% [markdown]
"""
After you do this sort of thing, it's usually a good idea to copy the dataframe and reset the
index -- otherwise you can get confusing errors. (There are cases where this isn't
true, of course, but it's a good rule of thumb.) This is the easiest way to do it:
"""

# %%
bsc_in = bsc_in.copy().reset_index(drop=True)

# %% [markdown]
"""
There's one more thing we should do before we move on. The BSC gives RA and DEC
in hours/minutes/seconds notation. This is all well and good, but can be hard for general-purpose
tools to work with, because they don't usually understand this notation. Hence this error:
"""

# %%
bsc_in.loc[(bsc_in['RAJ2000'] < 20) & (bsc_in['DEJ2000'] > 0)]

# %% [markdown]
"""
Fortunately, `astropy` _does_ understand this notation, and we can use it to convert these
from hours/minutes/seconds to decimal. The `Angle` object from `astropy.coordinates` is our helper here.
Note that you have to specify the units, or astropy will be unhappy.
"""

# %%
from astropy.coordinates import Angle
ra0 = Angle(bsc_in.loc[0, 'RAJ2000'], unit='hour')
# astropy parses and prints it nicely:
ra0

# %% [markdown]
"""
and then you can convert it from hour-minute-second to decimal degrees:
"""

# %%
ra0_decimal = ra0.degree
ra0_decimal

# %% [markdown]
"""
That's all well and good for a single value -- but you can even pass the entire
Series at once...
"""

# %%
ra_angles = Angle(bsc_in['RAJ2000'], unit='hour')
ra_angles

# %% [markdown]
"""
And convert it all to decimal at once!
"""

# %%
ra_decimal = ra_angles.degree
ra_decimal

# %% [markdown]
"""
Let's do the same thing with declination, which is in degree-minute-second
rather than hour-minute-second:
"""

# %%
dec_angle = Angle(bsc_in['DEJ2000'], unit='deg')
dec_angle

# %%
dec_decimal = dec_angle.degree
dec_decimal

# %% [markdown]
"""
Now we can go ahead and replace the ra/dec strings in the dataframe
with our decimal numbers.
"""

# %%
bsc_in['RAJ2000'] = ra_decimal
bsc_in['DEJ2000'] = dec_decimal

# %% [markdown] editable=true slideshow={"slide_type": ""}
"""
And you'll find that our earlier expression will work:
"""

# %%
bsc_in.loc[(bsc_in['RAJ2000'] < 20) & (bsc_in['DEJ2000'] > 0)]

# %% [markdown]
"""
Now we can write our nice-cleaned up table to a new CSV file and use it in the next 
Notebook without worrying about all of these fiddly details again:
"""

# %%
bsc_in.to_csv("bright_star_directory/bsc_clean.csv", index=None)
