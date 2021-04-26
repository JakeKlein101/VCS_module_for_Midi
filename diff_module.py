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


def log_diffs_to_file(latest_file_path, latest_file_ms, second_to_last_file_ms, message_index):
    """
    Logs the different messages that were found between the MIDI files that were compared to a changes.gitbit file.
    The file contains the message index, followed by the new version of the message
     that is followed by the message from the second to latest commit.
    """
    with open(os.path.join(os.path.dirname(latest_file_path), "changes.gitbit"), "a") as changes_log_file:
        changes_log_file.write(str(message_index) + ": " + str(latest_file_ms)
                               + "\n" + str(second_to_last_file_ms) + "\n")


# Main method:

def main_diff(latest_file_path, second_to_last_file_path):  # TODO: check all edge cases.
    if filecmp.cmp(latest_file_path, second_to_last_file_path):
        print("No changes were made.")
        return 0

    latest_file, second_to_last_file = file_paths_to_midi_objects(latest_file_path, second_to_last_file_path)

    for latest_file_track, second_to_last_file_track in zip(latest_file.tracks, second_to_last_file.tracks):
        # Iterates and compares the tracks in the files, if the tracks are equal, there is no need to iterate over them.
        if latest_file_track == second_to_last_file_track:
            continue
        else:
            # Iterates and compares each message over unequal tracks, prints True over equals and false over diffs.
            # TODO: Add the track index to the log file.
            for message_index, packed_args in enumerate(zip(latest_file_track, second_to_last_file_track)):
                latest_file_ms, second_to_last_file_ms = packed_args
                print(str(message_index) + " Latest: " + str(latest_file_ms)
                      + " Second Latest: " + str(second_to_last_file_ms))
                if latest_file_ms != second_to_last_file_ms:
                    log_diffs_to_file(latest_file_path, latest_file_ms, second_to_last_file_ms, message_index)
                    print(False)
                else:
                    print(True)


main_diff("modified.mid", "origin.mid")  # For testing


