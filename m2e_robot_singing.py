"""
This module demonstrates how to make a Create Robot SING.

Authors: David Mutchler, Amanda Stouder, Chandan Rupakheti, Katie Dion,
         Claude Anderson, Delvin Defoe, Curt Clifton, Matt Boutell,
         Dave Fisher and their colleagues. January 2014.
"""
#-----------------------------------------------------------------------
# Students: Read and run this program.  There is nothing else
#           for you to do in here.  Just use it as an example.
#     *** Get your instructor to explain the concept of BLOCKING ***
#     *** and its relevance to playing notes and songs.
#-----------------------------------------------------------------------

import new_create
import time


def main():
    """ Calls the   TEST   functions in this module. """
    first_notes_and_song()
    bad_singing()
    using_a_sensor_to_block()


#-----------------------------------------------------------------------
# Students: Read and run this program.  There is nothing else
#           for you to do in here.  Just use it as an example.
#           Before you leave this example, be sure you understand:
#  -- How to use the   playNote   method
#  -- How to use the   playSong   method
#  -- The limitations of each of the above, especially the implications
#       of the fact that neither of them "blocks"
#-----------------------------------------------------------------------
def first_notes_and_song():
    """ Demonstrates the    playNote   and    playSong    methods. """
    # Construct a robot, put it in safe mode.
    # Make it play two notes, then a song, then disconnect.

    time.sleep(2)  # In case the robot has recently been shutdown.

    port = 'sim'  # Or use YOUR laptop's COM number
    hal = new_create.Create(port)
    hal.toSafeMode()  # So you can try this out on a table if you want.

    #-------------------------------------------------------------------
    # playNote(pitch, duration):
    #
    # Notes range from 31 (low G, 49.0 Hz) to 127 (high G, 12543.9 Hz).
    # They can be played from as little as 1/64th of a second to as
    # long as 255/64 seconds (i.e., almost 4 seconds).
    # The    playNote    method takes TWO (2) arguments:
    #   -- The note (should be in the range 31 to 127, inclusive)
    #   -- The duration to play that note, in 64th's of a second
    #        (must be between 0 and 255, inclusive)
    #-------------------------------------------------------------------

    hal.playNote(31, 255)  # Very long, low note.
    time.sleep(5.0)  # See next example for why we need sleeps.

    hal.playNote(110, 1)  # Very short, high note.
    time.sleep(1.0)

    #-------------------------------------------------------------------
    # playSong(LIST of pitch-duration TWO-TUPLEs)
    #
    # If you want to play a sequence of notes, it is almost always
    # better to use the    playSong   method instead of doing a
    # sequence of calls to playNote.  The   playSong  method takes
    # ONE (1) argument.  That argument must be:
    #  -- a LIST
    #  -- with no more than 16 items
    #  -- where each item is a 2-tuple
    #       whose first element is the pitch (31 to 127)
    #       and whose second element is the duration (1 to 255)
    #  -- where pitch and duration are as in playNote.
    #-------------------------------------------------------------------

    song = [(60, 8), (64, 8), (67, 8), (72, 8)]  # a quick C chord
    hal.playSong(song)
    time.sleep(2.0)

    hal.shutdown()


def bad_singing():
    """
    Demonstrates the effect of sending a new note/song before the
    old one has finished.  Try running this both in the simulator
    and with a real robot (expect strange results with the latter).
    """
    time.sleep(2)

    port = 'sim'
    hal = new_create.Create(port)
    hal.toSafeMode()  # So you can try this out on a table if you want.

    for k in range(31, 128):
        hal.playNote(k, 16)
        # Try with the following commented-out, then not commented-out.
        # time.sleep(16 / 64)

    song = [(60, 32), (64, 32), (67, 32), (72, 32)]  # a slower C chord
    hal.playSong(song)
    hal.playSong(song)
    hal.playSong(song)

    hal.shutdown()


def using_a_sensor_to_block():
    """
    Demonstrates using the   song_playing   sensor to "block"
    until the note/song is finished before starting the next one.
    """
    time.sleep(2)

    port = 'sim'
    hal = new_create.Create(port)
    hal.toSafeMode()  # So you can try this out on a table if you want.)

    is_playing_sensor = new_create.Sensors.song_playing
    for k in range(31, 128):
        hal.playNote(k, 4)
        while True:
            is_playing = hal.getSensor(is_playing_sensor)
            if not is_playing:
                break

    song = [(60, 32), (64, 32), (67, 32), (72, 32)]  # a slower C chord

    hal.playSong(song)
    while True:
        is_playing = hal.getSensor(is_playing_sensor)
        if not is_playing:
            break

    hal.playSong(song)
    while True:
        is_playing = hal.getSensor(is_playing_sensor)
        if not is_playing:
            break

    hal.shutdown()

#-----------------------------------------------------------------------
# If this module is running at the top level (as opposed to being
# imported by another module), then call the 'main' function.
#-----------------------------------------------------------------------
if __name__ == '__main__':
    main()
