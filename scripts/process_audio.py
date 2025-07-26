import os
import subprocess
import tempfile
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "input"))
OUTPUT_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "output"))
LOG_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "logs"))
FX_CHAIN = os.path.abspath(os.path.join(BASE_DIR, "CompressorChain.RfxChain"))
REAPER_PATH = "/Applications/REAPER.app/Contents/MacOS/REAPER"  # Update if needed

os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

LOG_PATH = os.path.join(LOG_DIR, "processing.log")

def log(message):
    with open(LOG_PATH, "a") as f:
        f.write(f"{datetime.now().isoformat()} - {message}\n")

def process_file(filepath):
    filename = os.path.basename(filepath)
    reaper_log_path = os.path.join(LOG_DIR, f"reaper_batch_{filename}.log")

    # Write a temporary file list for REAPER
    with tempfile.NamedTemporaryFile("w", delete=False, suffix=".txt") as listfile:
        listfile.write(filepath + "\n")
        listfile_path = listfile.name

    cmd = [
        REAPER_PATH,
        "-nogui",
        "-quit",
        "-batchconvert", listfile_path,
        "-batchconvertoutput", OUTPUT_DIR,
        "-batchconvertfxchain", FX_CHAIN,
        "-batchconvertlog", reaper_log_path
    ]
    print("Full command:", ' '.join(cmd))

    log(f"START processing {filename}")
    subprocess.run(cmd)
    log(f"FINISHED processing {filename}")

    # Clean up the temp file list
    os.remove(listfile_path)

def main():
    files = [f for f in os.listdir(INPUT_DIR) if f.lower().endswith(('.aif', '.mp3'))]
    for fname in files:
        abs_filepath = os.path.abspath(os.path.join(INPUT_DIR, fname))
        process_file(abs_filepath)

if __name__ == "__main__":
    main()
