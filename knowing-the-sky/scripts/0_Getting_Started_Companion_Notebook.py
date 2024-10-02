# ---
# jupyter:
#   jupytext:
#     cell_markers: '"""'
#     comment_magics: true
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

# %% [markdown] jp-MarkdownHeadingCollapsed=true
"""
# Notebook basics

This Notebook is intended to teach you the basics of using Jupyter Notebook to run
Python code. You'll need to know these basics in order to use the rest of the 
_Knowing the Sky_ interactive content. If you're already familiar with 
Notebook, you can skip it, although there might still be a few tidbits for you.

Read the rest of this cell to learn how to navigate between and run cells,
then go ahead and move cell-by-cell through the rest of the Notebook.

Notebook has many features we don't cover here. If you'd like to dig deeper,
you can check out the 
[official Notebook documentation](https://jupyter-notebook.readthedocs.io/en/latest/notebook.html)
or explore the links in the Jupyter Notebook 'Help' menu above.

## Commands

Notebook has two 'modes': Command Mode and Edit Mode. When you open a Notebook, you start in Command Mode. Command Mode lets you navigate, create, delete, and reorganize cells. The easiest way to do this is to use
keyboard shortcuts:

* To move between cells, press the `Up` or `Down` arrow.
* To run a cell, press `Shift+Enter`.
* To make a new cell below the active cell, press `b`.
* To make a new cell above the active cell, press `a`.
* To delete the active cell, press `d` twice.
* To undo deleting a cell, press `z`.
* For a complete list of shortcuts, press `Ctrl+Shift+h`. (If you're on Mac use `Command+Shift+h`)


### Switching modes

* To switch into Edit Mode in the active (highlighted) cell, press `Enter`. You can also enter Edit Mode by clicking inside a cell.
* When you run a cell in Edit Mode, you automatically switch back to Command Mode.
* You can also go back to Command Mode by pressing Escape or clicking outside a cell.

There are several ways to tell what mode you're in:
* In Edit Mode, the border around the cell will turn blue and the background color changes. Press `Enter` while the blue bar is highlighted on the left of this cell to see what it looks like unformatted and in edit mode (remember you can press `Shift+Enter` to run/format it again)
* When you are in edit mode, you'll see a blinking cursor inside the active cell.
"""

# %% [markdown]
"""
----
# cell execution and output
"""

# %%
# When you run a cell, Jupyter prints its result underneath the cell.
# If you highlight this cell and run it with Shift+Enter, '10' 
# will appear below the cell.

x = 5
5 + x

# %%
# Jupyter only automatically prints the result of the last expression in a cell,
# so if you want to print earlier expressions, you need to use print statements. Running
# this cell will print '3' and '5' before printing '10'. Note that the '3 + 3'
# expression doesn't produce any text.

print(1 + 2)
print(2 + 3)
3 + 3
4 + 6

# %%
# variables defined in one cell are accessible in other cells:

x + 3

# %%
# only the order you run cells in matters, not how they're arranged in the Notebook.
# if you run this cell, then run the previous cell again, its output will change to '12'.

x = 9


# %%
# being able to run cells out of order is very convenient, but can get confusing.
# wrapping variable definitions in functions is a good way to make sure they don't 
# end up in places you'd rather they didn't:

def timestwo(number):
    """multiplies things by 2."""
    y = number * 2
    return y

print(timestwo(2))
try:
    print(y)
except NameError:
    print("y didn't sneak out of the scope of timestwo().")

# %% [markdown]
"""
# TODO: Not available in all versions of jupyter (not in 7), make sure we use a compatible version
"""

# %%
# if a cell's output is very long, Jupyter will put its output in a scrolling
# panel. if you like, you can switch a cell's output between scrolling 
# and non-scrolling modes by using Shift+O in Command Mode.
# you can also completely hide and unhide output by using O. try it out:

for i in range(1000):
    print(i)

# %% [markdown]
"""
----
# interactive help
"""

# %%
# Jupyter has great interactive help and inspection features.
# if you place '?' after a variable and run the cell, it will open
# up a panel with some basic information about the object the variable refers to,
# including its type, its docstring (if any), its string representation, the module
# it's defined in (if available), and, if it's a function (including a class constructor), 
# its signature. 

# You can grow or shrink the panel by dragging its border.
# You can close the panel with Escape or by clicking its X button. TODO: Not in all versions of jupyter (not 7)

# this will show you that x is the integer 9, and also tell you about Python ints:

# x?

# %%
# if you place '??' after a variable, you'll also be able to see the object's complete 
# source code, if available. This will show you the full definition of timestwo() from 
# the earlier cell:

# timestwo??

# %%
# if you'd like to print help text so that it sticks around, you can use the built-in
# Python help function:

help(str)

# %% [markdown]
"""
----

# system operations 


### saving

Notebook autosaves every few minutes. This means that if you make changes to a Notebook, they'll stick around in the file. If you want to make *sure* that your work is saved, you can press `Ctrl+S` (on Mac `Command+S`) to 'save and checkpoint'. This not only immediately saves the Notebook, but creates a 'checkpoint' -- a timestamped version of the Notebook file. You can later use 'revert to checkpoint' in the File menu to go back to that specific state.

### closing

If you terminate the Jupyter Server by pressing `Ctrl+C` in the terminal you executed it in, it will shut down all running Notebooks.

If you are running multiple Notebooks and want to shut down a specific one, use the 'close and shut down Notebook' option in the File menu.

### restarting

You can restart a Notebook by pressing `0` twice in Command Mode. This preserves printed output but completely resets the state of the Python interpreter. If you also want to clear all output, making the Notebook pristine, use the 'restart and clear output' option in the Kernel menu.

### interrupting

If you want to stop a running cell -- maybe because you've noticed there's an infinite loop or something -- you can press `I` twice in Command Mode to interrupt the Notebook. 

*Technical note: this is just like pressing Ctrl+C in a terminal. It works by raising a `KeyboardInterrupt` exception in the interpreter.*
"""

# %% [markdown]
"""
----
# importing code

Import statements work in Notebooks just like they do in other Python code: if you want to use Python objects that aren't defined in the Notebook and aren't [Python built-ins](https://docs.python.org/3/library/functions.html), you need to import them. See the example below.

*Technical note: importing code **into** a Notebook is easy, but [importing code **from** a Notebook is complicated](https://jupyter-notebook.readthedocs.io/en/stable/examples/Notebook/Importing%20Notebooks.html), and we don't advise doing it. If you want to reuse a piece of code you wrote in a Notebook, you should put it in a regular Python module.*
"""

# %%
# this attempt to use search() from re, the Python Standard Library's regex
# module, won't work:

try:
    ip_address = re.search(
        r"(?:\d{1,3}\.){3}\d{1,3}(:\d{2,4})?", 
        "Jupyter Server's default address is 127.0.0.1:8888."
    ).group()
    print(ip_address)
except NameError as err:
    print(err)

# %%
# however, if you run this import statement, the previous cell will work.
import re

# %% [markdown]
"""
----
# cell types

Notebooks have three types of cell. You've seen two of them in this Notebook: code cells and Markdown cells. 
* Code cells have an `[ ]` in their left sidebar, and Notebook treats them as executable code. As you've seen, when you run a code cell, Notebook runs the code in that cell.
* Markdown cells -- like this one -- have highlighted Markdown syntax but no `[ ]`. When you run a Markdown cell, Notebook typesets the text in that cell, letting you make italics, headers, lists, and so on -- just like this cell. Enter Edit Mode in the next cell for more examples.
* There are also plain text cells, which just hold any text you type and don't do anything with it.

From Command Mode, you can change the type of a highlighted cell by pressing `y` (for code), `m` (for Markdown), or `r` (for plain text).
"""

# %% [markdown]
r"""
# This is 

## an example

### Markdown 

#### cell.

**Markdown is a markup language** *that lets you* 
`format` ***text*** [in many different ways.](https://www.markdownguide.org/)
1. including
2. different
    * types
    * of
    * lists,

mathematical expressions,
$$\sin \kappa = \int_\epsilon^{\epsilon+\delta} \sqrt{1 - \gamma^2}$$

> quotations,

----

```javascript
// and nicely-highlighted (non-executable) code blocks.
let markdownRenderHighlighted = code === in_ ? many : languages;
```

```erlang
really(a) whole < lot -> of_languages;
```
"""

# %% [markdown]
"""
----

# special commands

Finally, it's good to know that Notebook provides some special commands that aren't Python code. Here are a few useful examples. We'll use some more in subsequent Notebooks. [See the iPython documentation for a full list.](https://ipython.readthedocs.io/en/stable/interactive/magics.html)
"""

# %%
# 'line magics' have a % prefix and work as one-shot commands or modify a single line
# of code. For instance, the %time magic measures how long a line of code takes to run:

from time import sleep
# %time sleep(1)

# %%
# # %whos prints a table briefly describing all the objects 
# you've defined or imported in the top-level scope of the Notebook.

# %whos

# %%
# # %history prints the contents of all the cells you've run so far, in the order you ran them in.

# %history

# %%
# %%time
# 'cell magics' have a %% prefix and modify, or take instructions from, an entire cell.
# cell magics always have to go at the very top of a cell.
# the %%time magic measures how long a whole cell takes to run. 

for _ in range(10):
    sleep(0.1)

# %%
# You can also directly run commands in the system shell by prefixing them with !. You can
# even assign the output of these commands to variables and use them in Python code.
# TODO: does this work in windows?

# notebooks = !ls *.ipynb
for n in notebooks:
    print(n.replace('.ipynb', ''))

# %% [markdown]
"""
#### Okay, now you are ready to begin the content in _Knowing the Sky_! Let's move on to Lesson 1!
"""
