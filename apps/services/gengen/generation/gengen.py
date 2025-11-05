import os
import sys
import subprocess
import shared.utils.utils as utils
from dotenv import load_dotenv

sys.path.append(".")

load_dotenv()


data_path = os.path.dirname(os.getenv('DATA_DIR'))

run_dir = os.path.join(data_path, "run")
data_dir = os.path.join(data_path, "generate", "output", "time.in.progress", "instagram")  # nopep8
build_dir = os.path.join(data_path, "generate", "img", "build")
generated_data_dir = os.path.join(data_path, "data", "general", "generated", "instagram")  # nopep8


def run_gengen():
    """ Runs the gengen .bat file """

    bat_file = os.path.join(run_dir, "run_generate_absolute_path.bat")
    print('====')
    print(run_dir)

    print(os.listdir(run_dir))
    try:
        subprocess.Popen([bat_file])
        print("Batch file executed successfully.")
        return True
    except Exception as e:
        print(f"Error occurred while executing the batch file: \n\n{e}")
        return False


def check_gengen():
    """ Polls the gengen directory for progress. """

    DATES = utils.get_dates()
    date_now = DATES["date_now"]

    file_output_dir = os.path.join(data_dir, str(date_now))
    file_output_dir_short = f"/time-in-progress-socials/generate/output/time.in.progress/instagram/{str(date_now)}"
    generated_data_file = os.path.join(generated_data_dir, f"{str(date_now)}.json")  # nopep8

    frames_list = os.listdir(build_dir)
    count = len(frames_list) - 1  # minus .gitignore

    generated_file = f"{file_output_dir}/TimeInProgress_simple_bars.mp4"
    generated_file_scaled = f"{file_output_dir}/TimeInProgress_simple_bars_audio.mp4"

    if os.path.exists(generated_data_file):
        if len(os.listdir(file_output_dir)) > 0:

            print("Generation complete")

            data = utils.read_json(generated_data_file)

            return {"done": True,
                    "count": count,
                    "files": {"generated_file": generated_file,
                              "generated_file_scaled": generated_file_scaled,
                              "file_output_dir_short": file_output_dir_short
                              },
                    "manifest": data
                    }

    return {"done": False, "count": count, "files": None, "manifest": None}
