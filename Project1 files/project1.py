from pathlib import Path
from read_input import readContent, interpret_content
from run_simul import start

def _read_input_file_path() -> Path:
    # I have not created unittest for this function as I had no idea how to specify user input in unittest.
    """
    Reads the input file path from the standard input
    """
    return Path(input())


def main(*, testPath=None) -> None:
    """
    Runs the simulation program in its entirety
    """
    # I could not cover the next two lines in my unittest as I did not know how to unittest
    #   _read_input_file_path function, as I commented above the function.
    # Therefore, in order to test other lines, I added keyword only argument testPath in the
    #   function parameter, allowing me to manually type in the path for unittest.
    if testPath is None:
        input_file_path = _read_input_file_path()
    else:
        input_file_path = testPath

    try:
        with open(input_file_path, 'r') as input_file:
            content = readContent(input_file)
        simul = interpret_content(content)
        start(simul)
    except FileNotFoundError:
        print('FILE NOT FOUND')


if __name__ == '__main__':
    main()
