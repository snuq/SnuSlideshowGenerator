# Snu Slideshow Generator For Blender 4.0

This addon for Blender assists in creation of high quality slideshows.  The aim is to be easy to use, but with many customization features if you want to dig under the surface.

Watch the demo video:  
[![Demo Video](https://img.youtube.com/vi/3cQYzMZ3b7k/0.jpg)](https://www.youtube.com/watch?v=3cQYzMZ3b7k)


Development for this script is supported by my multimedia and video production business, [Creative Life Productions](http://www.creativelifeproductions.com)  
But, time spent working on this addon is time I cannot spend earning a living, so if you find this addon useful, consider donating:  

PayPal | Bitcoin
------ | -------
[![paypal](https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=XHRXZBQ3LGLH6) | ![Bitcoin Donate QR Code](http://www.snuq.com/snu-bitcoin-address.png) <br> 1JnX9ZFsvUaMp13YiQgr9V36EbTE2SA8tz  

Or support me by hiring Creative Life Productions if you have a need for the services provided.


## Installation
* Click on 'Releases' on the right
* Select the release that most closely matches your Blender version
* Click 'Assets' to expand the downloads if necessary
* Download the addon by clicking the 'Source code (.zip)' link
* Open Blender, and from the 'Edit' menu, select 'Preferences'.
* In this new window, click on the "Add-ons" tab at the left.
* Click the 'Install...' button at the top-right of this window.
* Browse to and select the zip file you downloaded, click the 'Install Add-on' button.
* You should now see the addon displayed in the preferences window, click the checkbox next to the name to enable it.
* Once installed, the interface can be found in the 3d View area sidebar, under the 'Slideshow' tab.


## Creating A Slideshow Generator
The first step is to create the slideshow generator scene.  This is a special scene that allows you to organize the images, change transitions and add effects to the slides.  
* Place all the images and videos you wish to use in a slideshow in a folder.  
* Select that folder using the directory browser button next to 'Image Directory' in the slideshow generator panel.  
   Images can be added after creating the scene as well, but adding an entire directory in this way is easier.  

* Set the slide length to an appropriate length to display each slide.  
   Use the estimated length, but be aware that videos may cause this length to be inaccurate.  
   Slide lengths can be easily set later as well.  

* Slide movement, or 'Transforms' will be randomized per slide.  Undesired transforms can be disabled by selecting them in the 'Toggle Transforms' menu.  
   Transforms can be randomized or changed later as well.  

* Special effects, or 'Extras' will be randomized per slide.  Undesired effects can be disabled by selecting them in the 'Toggle Extras' menu.  
   As with transforms, these can be randomized or changed later.  

* Extra Textures are an image or video that can be used as an effect in a slide.  These can used by Extras like the 'Video Foreground' and 'Video Background'.   
   Select a texture file by clicking the browse button next to the 'Extra Texture' field.  
   Click the '+' button to add the texture to the 'Extra Texture Presets' menu.  
   To remove a texture, open the 'Extra Texture Presets' menu, and click the 'X' button next to the undesired texture.  

* Once everything is set, click the 'Create Slideshow Generator' button.  
   Note that creating a slideshow generator with a lot of images may take some time and appear to freeze blender while it loads in the images.  
   If this step is taking too long, resizing the images smaller should help.


## Configuring The Slideshow
Once the slideshow generator is created, the slides will be placed in a new scene and presented in the 3d viewport.  Make sure the 3d view is set to 'Look Dev' or 'Rendered' display mode to be able to see the slide previews.  

### The Slideshow Generator panel should now be in Create Slideshow mode.
* The 'Create Slideshow' button will finalize the slideshow that is set up.  
* An accurate representation of the final slideshow length will be shown.  
* Set the Crossfade Length to determine how long the fade between slides will be in the final slideshow.  
* An audio track can be added to the slideshow automatically:  
   * The 'Enable Audio Track' checkbox must be activated.  
   * Use the browse button next to the 'Audio Track' field to select an audio file.  This must be a format that Blender recognizes, or the audio will not be added.  
   * Loop Overlap is used when the slideshow is longer than the audio track.  The audio will be repeated as many times as needed, and this value will determine how much crossfade overlap (in frames) the repeated tracks have with each other.  
   * Fade Out is used when the audio track (after being looped) is longer than the slideshow.  The audio volume of the last loop will be faded down for this many frames.  

* The sorting order of the slides can be changed.  Clicking one of the sort option buttons will immediately reorder the slides. 
* Transforms or Extras can be randomized.  Clicking a randomize button will immediately assign new transforms or extras to all slides. 
* Additional images or videos can be added to the slideshow with the 'Add New Slide(s)' button, it/they will be placed at the end of the list.  
   Hold Shift to select multiple single files.  
   Hold Shift and Ctrl to select all files between two clicks.  
   Press 'a' to de/select all files in the directory.  
* Unwanted slides can be deleted by selecting any component of them, and pressing the delete slides button.  
   Do not manually delete slides from the 3d view, as this may confuse the generator.  

### In the 3d view:
* Click-drag an object to move it.  
* Click to select an object.  When selected:  
   Press 'g' to move the object.  Not all objects can be moved in all ways.  
   Press 'r' to rotate the object.  Not all objects can be rotated.  
   Press 's' to scale the object.  Not all objects can be scaled.  

* Selecting a View area:  
   Around each image slide is a rectangular box that represents the area of this slide that will be visible in the final slideshow.   
   * This box can be rotated to adjust the angle the image will be displayed at.  
   * This box can be scaled to crop the area of the slide that will be visible.  Scaling larger will make the slide smaller, scaling smaller will make the slide larger.  
   * The box can be grabbed/moved to change the view area of the slide.  
      Note that some transforms such as the zoom types, and the pan to target, will use this as the starting point for the movement.  

* Selecting the Target:  
   At the center of each image slide is a cross that is the view target.  This target will be the focal point of the zoom and pan to target transforms.  This target can be grabbed/moved to change where a zoom or pan transform will end on.  

* Selecting an image or video:  
   Grab the image to rearrange it in the sequence of images.  
   A 'Slideshow Image' panel will be visible in the sidebar, this will give settings for the selected slide.  
   * Rotation allows the rotation of the image in 90 degree increments, use this if the image is rotated wrong in the 3d view.  
   * A group of buttons for moving the slide are available:  
      "|<<" - Will move the slide to the beginning of the slideshow.  
      "<"   - Will move the slide back one place in the index.  
      ">"   - Will move the slide forward one place in the index.  
      ">>|" - Will move the slide to the end of the slideshow.  

   * Lock Position excludes the slide from being sorted by the sort buttons.  This is helpful for setting the first or last slide, for instance.  
   * The Slide Length variable can be changed to make some slides longer or shorter.  
      For images, this value will be in seconds, for a video, it will be in frames.  

   * Use the 'Apply To Selected' and 'Apply To All' buttons to apply the current length to other slides.  
      These buttons are not available for video slides.  

   * Lock Length will prevent this slide from being affected by the apply slide length buttons.  
      This is not available for video slides, as they will always be 'locked'.  

   * Video Offset is the number of frames that will be removed from the beginning of a video clip.  
      This option is only visible for video slides.  

   * Import Audio From Video File will cause the audio track from the selected video slide to be added to the final slideshow.  Unchecking this will result in a silent slide.  
      This is only visible for video slides.

   * Add Blurred Background If Needed will automatically add a scaled blurred copy of a video slide to fill out empty space around it if the video is a different size than the final slideshow.  
      This option is only visible for video slides.  

   * Currently selected transform will be shown.  
      Transforms and all related options are not available for video slides.  
      * Select a new transform for the current slide by using the 'Change Transform' menu.  
      * Transforms not to be used for randomizations can be deselected in this menu, click the checkbox next to the transform to toggle it.  
      * Use the 'Apply To Selected' and 'Apply To All' buttons to apply the current transform to other slides.  
      * Lock Transform will prevent this slide from being affected by apply transform or randomize buttons.  

   * The currently selected extra will be shown.  
      Extras and all related options are not available for video slides.  
      A number of default extras are included, and more can be added with some python programming.  
      * The 'Text Normal Top' and 'Text Normal Bottom' utilize the 'Extra Text' variable to add a title to the slide.  
      * The 'Video Foreground' and 'Video Background' utilize the 'Extra Texture' variable to add an overlay or background image or video.  
      * The extras will be affected by the 'Extra Amount' variable in different ways, mostly determining the strength of the effect.  
         The Extra Amount should probably be kept between 0.25 and 0.75 for most effects.  A value of 0 will be none, or too little of the effect for normal usage.  A value of 0.5 will be an average amount.  A value of 1 will be too much of the effect for normal usage.  
         * Background With Shadows Dark/Light: It will determine how bumpy the background is.  
         * Blurred Scaled Image Background: It will determine how blurred the background is.  
         * Compositor Glare: It will determine the threshold for the glare (how bright something is before it glares).  
         * Image Glint: It will determine the amount of glint.  
         * Overlay Curves Left/Right: It will determine how much the curves overlap the image.  
         * Parallax Frame Overlay: It will determine how far from the image the frame is, affecting the amount of parallax.  
         * Plain Background With/Without Shadows: It will determine the brightness of the background.  
         * Text Normal Bottom/Top: It will determine the extrude and bevel amount of the text.  
         * Video Background/Foreground: It will determine how visible the image or video is.  
         * Vignette: It will affect the contrast of the vignette.  

      * Use the 'Apply To Selected' and 'Apply To All' buttons to apply the current extra to other slides.  
      * Lock Extra will prevent this slide from being affected by apply extra or randomize buttons.  

   * Transition To Next Slide can be selected from the drop-down menu.  
      This will control how the current slide image fades to the next one.  
      * Crossfade is a standard smooth transition between the two slides.  
      * Gamma Cross is a variation on the Crossfade, it is slightly brighter.  
      * Wipe is a transition that will convert one slide to another using a moving line.  
         Wipe settings will be available when it is selected, these correspond with the settings used by the 'Wipe' effect in Blender's VSE.  
      * Custom allows the usage of a black and white video file as a mask to create a specialized transition.  
         Click the browse button next to the 'Transition Video' field to select a video file to be used.  
         These video files should be black-and-white only, and should start as fully black, and end with fully white.  
         If no video, or an invalid video is given, the transition will instead be a default Crossfade.  

      * The 'Apply To Selected' and 'Apply To All' buttons will apply the current transition to other slides.  
      * The 'Lock Transition' checkbox will prevent this slide's transition from being affected by apply to buttons.  



## Testing And Rendering The Slideshow
Once the slides are all configured, click the 'Create Slideshow' button to generate the slideshow sequence.  The slideshow will be created in a new Scene called 'Slideshow'.  
The final slideshow will be in the Video Sequence Editor and can be edited like any other video project.  
After this is done, the slide settings can still be changed, but the 'Create Slideshow' button must be clicked again to regenerate the slideshow and update the settings.  Any changes made in the vse will be erased if the slideshow is re-generated.

In the VSE there will be a new panel in the properties area titled 'Snu Slideshow Generator'.  This panel provides some helpful shortcuts for previewing the slideshow.  
   * Apply 50% Render Size: This will change the render size of all image slides to 50% of full, greatly reducing image quality.  Use this if you wish to render out a preview of the slideshow.  
   * Apply 100% Render Size: This will change the render size of all image slides to full, ensuring full image quality.  This is the default for the finished slideshow already, so use this only after rendering out a preview at 50% size.  
   * Return To Generator Scene: Click this to return to the slideshow generator scene to make edits.  

If any editing in the VSE is to be done at this point, it is recommended that the sequencer view mode be switched to Look Dev mode.  This will not be a completely accurate representation of the final render, but it should look good and images will display relatively quickly.  
More music can be added now, the timing of images can be tweaked, fades can be changed, or sequencer effects can be added.  
The individual slides are now scenes which can be edited or changed in any way if desired.  
The finished slideshow may now be rendered out to a video as a standard VSE video would be rendered.  



## Advanced Editing, Extras
Extras are python scripts kept in a subfolder 'Extras' placed where this addon file is located.  Each extra script defines what is created in the slide scene when it is imported.  The script's filename will determine the name of the extra listed in the UI, minus the .py extension.  
An extra script with the filename "None.py" will always be ignored by the generator, and is used as an example file.  

All extra scripts must contain the following function: `def extra(data):`  
The 'data' variable is a dictonary containing the following keys:


Passed in variable is a dictionary with the following keys:
* 'image_scene' - a Blender Scene  
   This is the scene that the slide has been placed in.  
   The script should be working in this scene, so starting with setting the current scene to image_scene is a good idea.

* 'image_plane' - a 3D Object, specifically a mesh plane  
   This is the plane object that the slide image is on.  
   The image_plane will be located at the point (0, 0, 0).  It will be 1 blender unit long on it's y axis, and it will be facing in the positive global z direction.  
   This plane is not animated in any way.  

* 'material' - a Material  
   The Material applied to the image plane.  

* 'material_output' - a 'ShaderNodeOutputMaterial' Node  
   This is the shader output for the node tree.  

* 'material_mix' - a 'ShaderNodeMixShader' Node  
   Input 1 controls the mix between the shaded and shadeless nodes - 0 is fully shadeless, 1 is fully shaded.  

* 'material_texture' - a 'ShaderNodeTexImage' Node  
   This contains the image texture.  

* 'material_shadeless' - a 'ShaderNodeEmission' Node  
   This node's texture is the image, and it outputs to the mix node.  

* 'material_shaded' - a 'ShaderNodeBsdfPrincipled' Node  
   This node's texture is the image, and it outputs to the mix node.  

* 'target_empty' - a 'plain axes' empty  
   This is the empty that is shown in the slideshow generator as the cross.  
   This is meant specifically for the transforms, but may have other uses.  

* 'camera' - a Camera object  
   This is the scene camera.  
   The camera will be located about 1.93 blender units (depending on the transform) above the plane in the global z direction, and pointing in the global negative z direction.  
   This is already set up and parented to the transform, and will be moving and/or scaled in most cases.  
   If you wish for an object to be stationary relative to the camera, make sure to parent it to this.  

* 'extra_amount' - a float variable between 0.0 and 1.0  
   This is exposed to the UI and is meant to control the 'strength' of the extra scene - for instance the amount of blur on a blurred background, or the extrusion amount of text.  
   The value of 0.5 should be a nice average amount, 0 should be too little for normal usage, and 1 should be too much for normal usage.  

* 'extra_text' - a string variable  
   This is exposed to the UI and can be used for text objects in the extra scene.  

* 'extra_texture' - a Blender Image, or a None if not able to be loaded  
   This is exposed to the UI and can be a still image or a video.  



## Advanced Editing, Transforms
These are defined by the 'transforms' list variable in the script.  
A single transform is a dictionary containing: name, influence, zLoc, zRot, xLoc  
* 'name' is required, a string value and will show up as the transform's name.  
* The next four values are lists of tuples, each tuple representing a point on the animation curve for the value.  
* Each tuple has two values: y location, and x scale (0-1 representing distance of handles, or how smooth the curve will be).  

If no points are included, or the variable is left out, there will be no animation for that value.  
If one point is included, the variable will remain at that value for the duration.  
If two points are included, they will determine the beginning and end points of the animation curve.  
If more than two are included, the middle points will be distributed evenly throughout the curve.  
