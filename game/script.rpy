# The script of the game goes in this file.

init python:

    import random, re, time

    # This function is optional. Only include it if you want automatic pauses between punctuation
    #def typography(what):
    #    replacements = [
    #             ('. ','. {w=.2}'), # Moderate pause after periods
    #           ('? ','? {w=.25}'), # Long pause after question marks
    #            ('! ','! {w=.25}'), # Long pause after exclamation marks
    #            (', ',', {w=.15}'), # Short pause after commas
    #    ]
    #    for item in replacements:
    #        what = what.replace(item[0],item[1])
    #    return what
    #config.say_menu_text_filter = typography # This ensures the text block has the same ID value, even after all the replacements are made

# This function plays text sounds at a rate that is based on the current CPS. 
# A slower CPS means that the sounds play at a slower rate. A faster CPS means the sounds play at a faster rate.
# The current limitation with this function, is that it can only handle one text speed per dialog block. It cannot switch between speeds within the same dialog block.
# You need to begin a dialog block with a {cps=} tag in order for this function to use that speed.
# Example:
#    ce "{cps=90}The text sounds will play one after another with almost no pauses in between."
#    ce "{cps=5}The text sounds will have a noticeable pause between each char"
#    ce "{cps=5}Despite the increase in character speed midway through this dialog block, {cps=190} the text sounds will remain at the lower speed. The function will only use the first instance of the CPS tag in a dialog block, and ignore the others"
    renpy.music.register_channel("textsound", "sfx", False) # Add a new sound channel for the text sounds so that they don't overlap with anything else

    _TAG = re.compile(r'{cps=(\d+)}') # Use regex to find and store the first instance of the {cps=} tag in a character dialog block

    def adaptive_text_sounds(event, interact=True, **kw):
        if event == "show":
            renpy.sound.stop(channel="textsound")
            raw  = renpy.store._last_say_what or ""
            text = renpy.substitute(raw)
            cps  = (kw.get("slow_cps") or kw.get("cps") or renpy.store.preferences.text_cps)

            for chunk in _TAG.split(text):
                if chunk.isdigit():
                    cps = int(chunk)
                    continue
                pause = 0 if cps <= 0 else 1.0 / cps

                for char in chunk:
                    if not char.isspace():
                        rsound = renpy.random.randint(0,2)
                        if rsound == 0:
                            renpy.sound.queue(f"audio/speech1.wav",channel="textsound") # Replace "audio/popcat{random.randint(1,11)}.wav" with sound files of your choice
                        elif rsound == 1:
                            renpy.sound.queue(f"audio/speech2.wav",channel="textsound")
                        elif rsound == 2:
                            renpy.sound.queue(f"audio/speech3.wav",channel="textsound")
                    if pause:
                        renpy.sound.queue(f"<silence {pause}>", channel="textsound")

        elif event in ("slow_done", "end"):
            renpy.sound.stop(channel="textsound")



define b = Character("Bubonnie", who_color="#010B13", callback=adaptive_text_sounds)

transform hop:
    yalign 0
    linear 0.1 ypos 0.1
    linear 0.1 ypos 0
    

# The game starts here.

label start:

    # Show a background. This uses a placeholder by default, but you can
    # add a file (named either "bg room.png" or "bg room.jpg") to the
    # images directory to show it.

    scene villagebg

    # This shows a character sprite. A placeholder is used, but you can
    # replace it by adding a file named "eileen happy.png" to the images
    # directory.

    show bbgreeting at hop

    # These display lines of dialogue.

    b "{cps=50}Hello there. You look... Unwell. How can I help you?"

    # This ends the game.

    return
