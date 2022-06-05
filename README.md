# myphotos
No frills utilities to manage my photos.

Using python with a tkinter windows interface, the utilities allow for exif date and geo data to be updated and files to be renamed to the exif date.

python: 3.10.4

# Library Format
To understand the utilities it helps to know the photo library format it's trying to maintain.
Each year has its own folder, and each event has its own sub-folder within the year.
The year folder is simply the year. The event folders begin with the date and an optional description.
Each photo is an ISO date format of when it was taken.

EG:
-  \2021
-  \2021\21-07-01 Family trip to the beach
-  \2021\21-07-01 Family trip to the beach\2021-07-01T12-14-59.jpg

# Steps

My photos come from a mix of ones taken on my phone, my camera or downloaded from social media. My phone puts the date and geo tags into the photo, for these I just need to update the filename and put them into a folder. My camera is okay with the date (when it is set correctly) but has no geo tags, so these need to be added, filenames updated and foldered. Files from social media could need the whole lot.

# Step 1 - Dates

`myphotos.dates.main`

First off is to add the exif date tags and rename and folderise the photos. If a photo has no exif data, rename the files and use the `Filename to Photo` option. If exif data exists use the `Photo to Filename` option.

This step creates a copy of the photos, if errors occur, they get seperated and if they're any videos or other non-image files they get split out too. The original files do not get changed.

# Step 2 - Descriptions

`myphotos.descs.main`

After step 1 you should have the photos organised into date folders. Before selecting step 2, re-organise and merge these folders as desired and add a description too. So `\21-12-31` and `\22-01-01` may become `\31-12-31 New Years Party`.

Once that's done, select the step 2 option. Select the folder and each photo anywhere under that folder, that doesn't already have a description, will be given the description from the directory. Use windows explorer, or the description field in the next step, to tweak specific images if you so wish.

NB: Description is the title property in the windows explorer file properties 

# Step 3 - Geos

`myphotos.geos.main`

For photos taken with my camera or downloaded, geo tags need to be added. Google maps is my friend here, use the `what's here` option to get the latitude and longitude, copy both in one go to the entry field.

# Step 4 - Check

`myphotos.check.main`

This is just a check to see if I've missed anything. It searches recursively, so set the source directory to the highest level.

# Launch

`myphotos.main`

Just a launchpad for selecting the steps.
