This is a very simple Blender Extension for a very simple Blender problem.
It's an extension, so add it as an extension from disk.

#### Be mindful that this extension's approach could create most undesirable results if you're a fan of the incremental save feature!
#### That would be an un-recommended combination!

If you find yourself pulling textures from various locations on your storage, or worse, switch from Windows to Linux, or much, much worse, from Linux to Windows,
you are liable to break links to textures.  This gets you the purple everywhere and while the Find My Textures addon is amazing for solving this, 
how much better it would be never to have the problem in the first place.

One solution is under File -> External Data -> Automatically Pack Resources (or manually, Pack Resources).
This does what it sounds like, and packs all the assets into the .blend file.
Problem with this is, with any file of size, like many things you do in Blender, it can grind Blender to a halt everytime you save, or auto save.

The happy medium is to make a local copy of your textures, and Blender has a built-in way to do that as well, in the same menu area.
"Unpack Resources" will spew all the textures into a folder called "textures" in the working directory, and there's no way to customize this directory.

We're halfway there, but this only keeps things organized if you literally create a separate folder for every .blend file you create.
Otherwise, if everything is in "textures," you'll have textures of various .blend files you saved in that particular directory.

You might be fine with this under a lot of circumstances, but if you're messing with material variations, etc... on a bunch of files,
it can be annoying to sort through textures all in a single folder, and almost as annoying to have a separate folder for every bloody file.

Enter this extension.  This adds "Unpack Textures to Scene Folder" to that "External Data" menu:
<img width="535" height="603" alt="image" src="https://github.com/user-attachments/assets/833fc32a-dc4a-49dd-9145-0a30378df1e7" />

All this does is the same as "Unpack Resources," except it names the folder after your .blend file name, i.e. {filename}_textures.
It then automatically runs "Make Paths Relative," which should make this portable and reduce the possibility of the scenario
outlined above, in which texture links get broken, moved, used on other models, etc...
