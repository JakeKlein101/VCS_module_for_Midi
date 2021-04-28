from mido import MidiFile
import filecmp
import os


# Utility methods:

def file_paths_to_midi_objects(latest_file_path, second_to_last_file_path):
    """
    Converts the file paths given to MidiFile objects and returns them
    :rtype: MidiFile, MidiFile
    """
    latest_file = MidiFile(latest_file_path, clip=True)  # Clip might cuase bugs in the future.
    second_to_last_file = MidiFile(second_to_last_file_path, clip=True)

    return latest_file, second_to_last_file


def log_diffs_to_file(latest_file_path, latest_file_ms, track_index, message_index):
    """
    Logs the diffences that were found between the MIDI files to a changes.gitbit file.
    The format of the loggin in the file is as followed:
    Track index of diff:Message index of diff:Diff message.
    """
    with open(os.path.join(os.path.dirname(latest_file_path), "changes.gitbit"), "a") as changes_log_file:
        changes_log_file.write(str(track_index) + ":" + str(message_index) + ":" + str(latest_file_ms) + "\n")


# Main method:

def main_diff(latest_file_path, second_to_last_file_path):  # TODO: check all edge cases.
    if filecmp.cmp(latest_file_path, second_to_last_file_path):
        print("No changes were made.")
        return 0

    latest_file, second_to_last_file = file_paths_to_midi_objects(latest_file_path, second_to_last_file_path)

    for track_index, packed_track_args in enumerate(zip(latest_file.tracks, second_to_last_file.tracks)):
        latest_file_track, second_to_last_file_track = packed_track_args

        # Iterates and compares the tracks in the files, if the tracks are equal, there is no need to iterate over them.
        print(f"Checking track {track_index}:")
        if latest_file_track == second_to_last_file_track:
            print(f"Tracks NO. {track_index} have no difference.")
            continue
        else:
            # Iterates and compares each message over unequal tracks, prints True over equals and false over diffs.
            print(f"Checking track messages for track  {track_index}:")
            for message_index, packed_args in enumerate(zip(latest_file_track, second_to_last_file_track)):
                latest_file_ms, second_to_last_file_ms = packed_args
                print(str(message_index) + " Latest: " + str(latest_file_ms)
                      + " Second Latest: " + str(second_to_last_file_ms))
                if latest_file_ms != second_to_last_file_ms:
                    log_diffs_to_file(latest_file_path, latest_file_ms, track_index, message_index)
                    print(False)
                else:
                    print(True)


main_diff("modified.mid", "origin.mid")  # For testing


