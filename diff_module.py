from mido import MidiFile
import filecmp


def file_paths_to_midi_objects(latest_file_path, second_to_last_file_path):
    """
    Converts the file paths given to MidiFile objects and returns them
    :rtype: MidiFile, MidiFile
    """
    latest_file = MidiFile(latest_file_path, clip=True)  # Clip might cuase bugs in the future.
    second_to_last_file = MidiFile(second_to_last_file_path, clip=True)

    return latest_file, second_to_last_file


def main_diff(latest_file_path, second_to_last_file_path):  # TODO: finish the method fully.
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
            for latest_file_ms, second_to_last_file_ms in zip(latest_file_track, second_to_last_file_track):
                # TODO: Make a counter so the logged lines will be numbered.
                print("Latest: " + str(latest_file_ms) + " Second Latest: " + str(second_to_last_file_ms))
                if latest_file_ms == second_to_last_file_ms:
                    print(True)
                else:
                    print(False)


main_diff("modified.mid", "origin.mid")  # For testing

