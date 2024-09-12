import os
import shutil
import argparse

def get_next_run_number(base_path):
    existing_dirs = [d for d in os.listdir(base_path) if d.startswith("Test_Duck_") and d[10:].isdigit()]
    if not existing_dirs:
        return 1
    return max([int(d[10:]) for d in existing_dirs]) + 1

def setup_run_directory(workdir, base_path, fix_dir):
    # Get the next run number
    run_number = get_next_run_number(base_path)
    run_dir_name = f"Test_Duck_{run_number:03d}"
    run_dir_path = os.path.join(base_path, run_dir_name)

    # Create the new run directory
    os.makedirs(run_dir_path, exist_ok=True)

    # Create 'outputs' subdirectory
    outputs_dir = os.path.join(run_dir_path, 'outputs')
    os.makedirs(outputs_dir, exist_ok=True)

    # Copy all files from workdir to the new run directory
    copy_directory_contents(workdir, run_dir_path)

    # Copy all files from fix_dir to the new run directory
    copy_directory_contents(fix_dir, run_dir_path)

    print(f"Created new run directory: {run_dir_path}")
    print(f"Created 'outputs' subdirectory: {outputs_dir}")
    print(f"Copied all files from {workdir} to {run_dir_path}")
    print(f"Copied all files from {fix_dir} to {run_dir_path}")

def copy_directory_contents(src_dir, dest_dir):
    for item in os.listdir(src_dir):
        s = os.path.join(src_dir, item)
        d = os.path.join(dest_dir, item)
        if os.path.isfile(s):
            shutil.copy2(s, d)
        elif os.path.isdir(s):
            shutil.copytree(s, d, dirs_exist_ok=True)

def main():
    parser = argparse.ArgumentParser(description="Create a new run directory and copy files from workdir and fix")
    parser.add_argument("--workdir", default="/home/mjisan/workflow/pyschism_suite/workdir",
                        help="Source workdir (default: /home/mjisan/workflow/pyschism_suite/workdir)")
    parser.add_argument("--base_path", default="/work/noaa/nosofs/mjisan/schism/schism_verification_tests",
                        help="Base path for creating run directories (default: /work/noaa/nosofs/mjisan/schism/schism_verification_tests)")
    parser.add_argument("--fix_dir", default="/home/mjisan/workflow/pyschism_suite/fix",
                        help="Fix directory to copy files from (default: /home/mjisan/workflow/pyschism_suite/fix)")

    args = parser.parse_args()

    setup_run_directory(args.workdir, args.base_path, args.fix_dir)

if __name__ == "__main__":
    main()
