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
## Lesson 3: Drawing the Sky
#### Learning Objectives:
After completing this lesson, users will be able to:
1. objective 1
2. objective 2
3. objective 3

_Python libraries introduced in this lesson:_ 
"""

# %%
from astropy.coordinates import AltAz, EarthLocation, SkyCoord
import astropy.time as at
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

pd.set_option('display.min_rows', 100)
pd.set_option('display.max_rows', 100)
%matplotlib qt

# %% [markdown]
"""
## coordinate transformations

The version of the Bright Star Catalog we fetched through Vizier defines star coordinates in 'J2000'. 'J2000' is a vague term: it can refer to any coordinate system referenced to the celestial equator and equinox of January 1st, 2000 TT (Terrestrial Time -- like Atomic Time but with a small offset), and there are several such systems. *todo: more about transforming time systems? this level of precision is not actually important for this problem...* Usually, however, it refers to an equatorial coordinate system whose origin is at the barycenter of the Solar System, and is interchangeable for most purposes with the International Celestial Reference System (ICRS). **todo, maybe: do i need to talk about what an equatorial coordinate system is? does it matter?**

An equatorial system is a type of inertial coordinate system. Inertial coordinate systems are acceleration-independent and very useful for specifying precise positions and orientations of objects in different accelerational frames. However, body-fixed systems, which move with a particular object such as a planet, and topocentric systems, which are relative to a particular observer, are often more useful for determining _apparent_ positions and trajectories of objects.

Transforming coordinates into other systems is one of the most common tasks in computing for planetary science and astronomy. The scientific Python ecosystem offers many tools to facilitate this task, and some of the most straightforward ones live in `astropy`.
"""

# %%
# let's read our cleaned-up version of the Bright Star Catalog back in.
bsc = pd.read_csv('bright_star_directory/bsc_clean.csv')
# then, let's make a SkyCoord object. SkyCoord is astropy's core class
# for representing the coordinates of celestial objects.
# You can specify other coordinate systems when you initialize a SkyCoord,
# but ICRS is the default, which is convenient for us here.
star_coords = SkyCoord(
    ra=bsc['RAJ2000'], dec=bsc['DEJ2000'], unit='deg'
)

# %% [markdown]
"""
### transforming 'equivalent' systems and representations

Transforming between inertial frames that are simply oriented differently is very easy in `astropy`. You can translate ICRS to systems like Galactic coordinates (another inertial coordinate system centered on the SSB, but with 'up' towards the center of the Milky Way) with no trouble at all. Similarly, if you'd prefer coordinates in Cartesian rather than spherical representation to make some calculation easier, you don't need to provide anything additional to `astropy`.
"""

# %%
star_coords.galactic

# %%
star_coords.cartesian

# %% [markdown]
"""
### transforming 'non-equivalent' systems

Transforming inertial coordinates into topocentric or body-fixed coordinates, however, requires more information. Because these systems take body position and acceleration into account, you need a reliable ephemeris, a specific point in time, and, for topocentric systems, observer location relative to body center.

Because we care about the 'position of rising' relative to an Earth-based observer, we will need to use a topocentric coordinate system: specifically, an altitude-azimuth system. 

**todo: what do you do if you need more precision? what about non-Earth bodies?**
"""

# %%
# we'll want to check the position of the sun and moon to look for 'betweenness'.
# we'll also later want to filter daylight times.

# TODO: explanation of 'solstice' definition related to fullness, c.f. our discussion,
# pending also discussion with Shandin re: Salish perceptions of the relationship
# or lack thereof between the winter solstice and the full moon

# there are lots of ways to get data on the position of objects in the Solar System; 
# one of the best is to query the JPL Horizons service. It has a solid web interface, 
# but multiple wrappers for it also exist that make it easier to get data into Python.
# our favorite is called lhorizon.
from lhorizon import LHorizon

# %%
seattle_coords = {
    'lat': 47.6062, 
    'lon': (360 - 122.3321),
    'elevation': 0,
    # 399 is the horizons code for Earth
    'body': 399
}
# this means: 'give me times starting at Jan 1 1900 and ending at Jan 20 1901, at 1-minute intervals'.
# we're getting a little more than a year to give us some numerical 'room' later.
epochs = {
    'start': '1900-01-01',
    'stop': '1901-01-20',
    'step': '1m'
}


# initialize a LHorizon object. this works something like the Vizier object
# we saw in the last notebook -- it represents a query, or a potential
# query, to the Horizons service.

# 10 is the Horizons code for the Sun.
# calling the .dataframe() method automatically queries Horizons
# and formats its response as a pandas dataframe. .table() provides
# a more compact representation but does not have all the fields we'll need.
# this query will probably take 15-30 seconds.
sun_positions = LHorizon(
    target=10, 
    origin=seattle_coords, 
    epochs=epochs,
    # at this point, we only care about rising and setting times, so we're turning on the 
    # 'rise_transit_set' flag, which causes Horizons to only return times when a body...
    # rises, transits, or sets.
    rise_transit_set=True
).table()

# %%
import pandas as pd

# %%
# create a pandas datetime column so we can do math with it
sun_positions['time'] = sun_positions['time'].astype('datetime64[ns]')
# Horizons returns UTC times, so we'll also offset that by 7 hours.
sun_positions['local'] = sun_positions['time'] - pd.Timedelta(hours=7)
# in rise-transit-set mode, Horizons uses the 'interference_flag' column to note
# which event has happened. to get sunrises, we'll filter the dataframe for just 
# 'r' (rising).
sunrises = sun_positions.loc[sun_positions['interference_flag'] == 'r'].copy().reset_index(drop=True)

# %%
# now let's do the same thing with the Moon. 
# this query will also probably take about 15-30 seconds.
moon_positions = LHorizon(
    # 301 is the Horizons code for the Moon.
    target=301, origin=seattle_coords, epochs=epochs, rise_transit_set=True
).table()

# %%
moon_positions['time'] = moon_positions['time'].astype('datetime64[ns]')
moon_positions['local'] = moon_positions['time'] - pd.Timedelta(hours=7)
moonrises = moon_positions.loc[moon_positions['interference_flag'] == 'r'].copy().reset_index(drop=True)

# %%
# in contemporary Western astronomy, 'winter solstice' has a distinct technical definition.
# but -- across many cultures -- practical astronomy tends to detect the winter solstice
# partly by the southernmost sunrise. (note that true south is a 180-degree azimuth.)
# Even the precision of Horizons doesn't give us an 
# exact date based on this -- look at how the rate of change in rising azimuth bounces 
# around due to quantization noise:
rising_azimuth_change = np.abs(np.diff(sunrises['az']))
plt.plot(rising_azimuth_change)

# %%
rising_azimuths = sunrises['az']
plt.plot(rising_azimuths)

# %%
# traditional methods often focused on grouping or counting days around
# extreme positions of the sunrise. we can emulate that with a moving average.
# surprisingly, Python doesn't offer a lot of
# out-of-the-box methods for computing averages. building lowpass 
# filters with scipy.signal or using convolution techniques are
# common options, but here, we'll use the pd.Series.rolling() method,
# which yields windows of a specified size. You can then do various
# mathematical operations on those windows -- including simple averages.
# the first values will be NaN because the window isn't full yet --
# but that's ok for our current purpose.
rolling_azimuth = pd.Series(sunrises['az']).rolling(15)
smoothed_azimuth = rolling_azimuth.mean()

# %%
# this has gotten rid of the worst of the quantization noise, 
# especially in periods when the azimuth isn't changing much...
# which is to say the summer and winter solstices.
smoothed_azimuth_change = np.abs(np.diff(smoothed_azimuth))
plt.plot(smoothed_azimuth_change)

# %%
# we can now go ahead and pick out reasonable-by-human-scale
# dates for the solstices by looking for the minima of this array.
# np.argsort is an extremely powerful function that gives you the indices
# that _would_ sort the array. we can use it to get indices for the
# two minima.
azimuth_change_indices = np.argsort(smoothed_azimuth_change)
azimuth_change_indices[0:2]

# %%
# because our moving average window didn't 'fill up' immediately, 
# we can expect these indices to be shifted by about half the size of
# the window from the 'true' minima. 7 is close enough to 15 / 2:
solstice_indices = azimuth_change_indices[0:2] - 7

# %%
# and then we can select rows from our sunrise table with them:
solar_solstices = sunrises.loc[solstice_indices]

# %%
# the Sun is not necessarily the most important thing, though.
# TODO: brief explanation of lunar calendars, which we'll talk more about later...
# the full Moon nearest this position marks the 'real' winter solstice.
# the 'Illu%' column of the moonrises table tells us how full the Moon is
# at each moonrise. 0 would be a perfectly new moon; 100 a perfectly full moon.

# full Moons and the solstices have a special relationship. let's take a look at it
# before we select the specific days. we'll do that by using some features of matplotlib
# to compare and color series.

# moonrises and sunrises don't perfectly line up in time, of course, but we've got some tricks
# with matplotlib. matplotlib will happily plot things with different numbers of points,
# which means that whenever you've got directly-comparable axis -- in this case, local time --
# you can use it to correctly align different chunks of data to match one another.
# better yet, matplotlib is aware of datetimes, so we can put dates right on this axis.
# it will automatically select ticks that will work for both time series.
%matplotlib qt
# use a black line for lunar azimuth
plt.plot(moonrises['local'], moonrises['az'], c='black')
# use a red line for solar azimuth
plt.plot(sunrises['local'], sunrises['az'], c='red')
# we're also going to show the phase of the moon at each rise using the plt.scatter function.
# this will enable us to indicate phase by specifying a color scale, which plt.plot can't do.
# greener means fuller; bluer means newer.
# you'll note that the rising azimuths of the moon and sun, at the full moon, 
# are most similar near the equinoxes and most different at the solstices.
# 'ill' means % illumination.
plt.scatter(moonrises['local'], moonrises['az'], c=moonrises['ill'], s=50, cmap='winter')
plt.colorbar()

# %%
# keeping this in mind, let's go ahead and pick the 'real' dates of the solstices --
# the full moons nearest the summer and winter solstice.

# %%
# change in lunar fullness -- this will be positive as the moon approaches full,
# and negative as it recedes from full. we're appending a large negative number
# to prevent np.diff from truncating the series -- we'll filter it later.
fullness_change = np.diff(moon_positions['ill'], append=-9999)
# now, we'll pick the times that this changes from positive to negative.
fullness_switch = np.diff(np.sign(fullness_change))
full_moon_indices = np.nonzero(fullness_switch == -2)[0] - 1
full_moons = moon_positions.loc[full_moon_indices]
# let's validate this real quick by making sure the Moon is quite full at these times:
full_moons['ill'].min()  # great.

# %%
solar_solstices['time'].dt.day_of_year

# %%
# now let's pick the temporally-closest days to the solar solstices by simply subtracting dates
# and picking the smallest offset:
winter_solstice_date = solar_solstices['time'].iloc[0]
lunar_offset = winter_solstice_date - full_moons['time']
# so, for this year, the lunar winter solstice is on January 4th.
# it's in the next year on the Gregorian solar calendar, but
# that's not the calendar that matters here.
full_moons.loc[lunar_offset == lunar_offset.min()]

# %%
# now that we know...

# %%
# TODO: rewrite to get the whole sun position table

# the table that Horizons gave us has a lot of columns. However, the only ones
# we actually care about in this case are 'time' and 'alt' (altitude).
sun_positions.columns

# %%
# let's use the predicate indexing trick we discussed in the last notebook to pick
# just times when the Sun has altitude < 0.
night = sun_positions.loc[sun_positions['alt'] < 0]
night[['time', 'alt']]

# %%
# now, we can use the 'time' series from the night table to construct coordinate frames for
# Seattle in each hour in the year. 
# astropy really likes to use its own objects, and the object it likes to use to define
# time is astropy.time.Time.
# fortunately, it's _really_ easy to make a Time object here, because Time objects can 
# be constructed directly from pandas datetime Series.
# note that astropy.time.Time can interpret a wide variety of other time formats;
# also note that its default scale is UTC (which is the default time scale for this type)
# of Horizons query, so, great.
times = at.Time(night['time'])
# and just like that, we have an astropy.time.Time object representing every hour in the year.
times[100:102]

# %%
# just like astropy likes its own Time objects, it also likes its own location objects. In this
# case, the appropriate one is astropy.coordinates.EarthLocation.
seattle = EarthLocation(lat=seattle_coords['lat'], lon=seattle_coords['lon'])
seattle

# %%
# now we can initialize an altitude-azimuth coordinate frame for each of these times.
# this will provide the specificity astropy needs in order to convert inertial to 
# topocentric coordinates.

# a note: under the hood, astropy uses IERS data to perform these transformations. 
# see: https://docs.astropy.org/en/stable/utils/iers.html#utils-iers

# just like Time can contain many times, astropy is happy to make a coordinate frame
# defined at multiple times or locations -- but because we only have one set of 
# initial coordinates, it'll fail if we try to actually perform the transformation.
# so let's instead make a list of coordinate frames and use them to compute 
# altitude-azimuth coordinates for each star at each time.
# this will probably take 30-60 seconds.
frames = []
for time in times:
    frames.append(AltAz(location=seattle, obstime=time))
star_altaz = []
for frame in frames:
    # note that on each iteration of this for loop, we are calculating alt-az coordinates
    # for _every star_ at a specific time.
    star_altaz.append(star_coords.transform_to(frame))

# %%
# now, in order to find approximate rising times for each star, we'll
# stack the altitude values into a big array...

alt_arrays = []
# grab the numerical altitude values from each list of coordinates as an array:
for altaz in star_altaz:
    # 'value' strips the special astropy information off and gives you just the numbers
    alt_arrays.append(altaz.alt.value)
# np.vstack means 'stack these arrays vertically.' This will give us
# an array oriented differently from our catalog table, so we'll take its
# transpose with .T -- meaning just 'turn it sideways' -- to recover the
# original orientation. We'll end up with an array where each column
# represents a specific time, and each row represents a specific star,
# and the array values represent that star's altitude at that time.
altitudes = np.vstack(alt_arrays).T
altitudes

# %%
# now our array rows correspond to our table rows.
altitudes.shape, bsc.shape

# %%
# we can now conveniently filter stars that are _never_ visible at night 
# from this point on the Earth. np.max tells us the maximum value of
# an array, and the axis=1 argument means 'do this along rows' -- so in other
# words, each star's maximum altitude.
max_altitudes = np.max(altitudes, axis=1)
max_altitudes

# %%
# then we'll use the fancy indexing trick again to reject any that never
# rise above the horizon. we'll also retain this in the never_visible
# variable so that we can filter other stuff with it later.
# TODO: what about circumpolar stars? are they rejected too?
never_visible = max_altitudes < 0
altitudes = altitudes[~never_visible]

# %%
# we'll now find the times that each star rises by looking for points where the
# altitude goes from below 0 to above 0. First, we'll make an array that just tells us whether 
# each point is greater or less than 0.
# np.sign returns -1 for negative numbers, 0 for 0, and 1 for positive numbers.
above_horizon = np.sign(altitudes)
above_horizon

# %%
# now we'll find the points where it changes using np.diff.
# np.diff gives the first discrete difference along the specified
# axis. In some cases, this is a good proxy for the first derivative
# of a function. Here we're just using it to detect change.
# we're going to prepend a large negative number to it so that
# we end up with an array of the same shape (otherwise np.diff will truncate it).
# we'll reject that number in the next step, so this is just a little
# trick to make the array shapes match up.
above_horizon_change = np.diff(above_horizon, axis=1, prepend=-9999)

# %%
# -2 implies that a star set; 2 implies that a star rose.
rising_points = above_horizon_change == 2
# let's validate our method a little bit -- 
# if it worked, successive points for a single star should be 
# separated by roughly 24 hours -- possibly with some slop for times
# that a star was only momentarily visible due to seasonal change, etc.

# np.nonzero can help us do that; it gives us the coordinates of
# all non-zero (or True) values in an array.
star_number, rising = np.nonzero(rising_points)

# %%
# that looks pretty solid.
# TODO: possibly need to handle stars that are _always_ up after the sun is down?
np.diff(rising[star_number == 80])

# %%
# now we'll create an azimuth array using the same technique we used to make the altitude array.
az_arrays = []
for altaz in star_altaz:
    az_arrays.append(altaz.az.value)
azimuths = np.vstack(az_arrays).T
azimuths

# %%
# and we'll reject invisible stars like we did for the altitude array:
azimuths = azimuths[~never_visible]

# %%
# and now we can use the rising points to make a mask for this array --
# specifically, we want to mask every azimuth value that's _not_ 
# associated with a rising event; hence the ~ (not) operator.
masked_azimuths = np.ma.masked_array(azimuths, mask=~rising_points)

# %%
len(np.ma.unique(masked_azimuths[5]))

# %%
np.unique(masked_azimuths[5]).data

# %%
# what does 'same place' mean? what 'same' is cannot be blithely assumed,
# nor can 'place'.
# but let's see what we can do with quantities by taking a look at the 
# maximum variation in rising azimuth for each star.
# TODO: is this problematic in cases where a star barely comes noticeably over
# the horizon in some parts of the year?
rising_azimuth_ranges = []
# a for loop over a numpy array always iterates over its last axis -- so each
# iteration of this loop looks at a different star, which is what we want.
for star in masked_azimuths:
    # np.ma.ptp gives the difference between the minimum and maximum values in an
    # array. in this case, each array is a 1x4374 array containing azimuth values 
    # -- mostly masked! np.ma.ptp will respect the mask and give us only the unmasked values.
    # if all the values are masked, it'll just give us 'masked', which we'll filter later.
    # TODO: these are circumpolar stars, which we maybe want to reject out of hand
    # before this...
    rising_azimuth_ranges.append(np.ma.ptp(star))

# %%
# let's make a histogram of these.
plt.hist(rising_azimuth_ranges, bins=128)

# %%
# it looks like there are a few outliers on the bottom end. let's see which stars have
# < 12 degrees of rising azimuthal variation.
star_candidates = np.nonzero(np.array(rising_azimuth_ranges) < 12)[0]

# %%
# now, let's filter our catalog using the same invisible star mask
# we used for our altitude and azimuth arrays, so that everything is aligned:
bsc_visible = bsc.loc[~never_visible].reset_index(drop=True)

# %%
# and then pick the candidate stars from the table.
bsc_candidates = bsc_visible.loc[star_candidates]
