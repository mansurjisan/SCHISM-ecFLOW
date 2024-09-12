import argparse

def generate_job_card(use_wwm, cluster):
    # Define executables based on cluster and WWM option
    executables = {
        'hercules': {
            True: 'pschism_HERCULES_WWM_BLD_STANDALONE_TVD-VL',
            False: 'pschism_HERCULES_BLD_STANDALONE_TVD-VL'
        },
        'frontera': {
            True: 'pschism_FRONTERA_WWM_BLD_STANDALONE_TVD-VL',
            False: 'pschism_FRONTERA_BLD_STANDALONE_TVD-VL'
        }
    }

    # Select the appropriate executable
    executable = executables[cluster][use_wwm]

    # Generate the job card content
    job_card_content = f"""#!/bin/sh
#SBATCH -e err
#SBATCH -o out
#SBATCH --account=nosofs
#SBATCH --qos=batch
#SBATCH --partition={cluster}
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=80
#SBATCH --time=07:00:00
#SBATCH --job-name="run_schism"
##SBATCH --exclusive
set -eux
echo -n " $(date +%s)," > job_timestamp.txt
set +x
echo $PWD
module purge
module load intel-oneapi-compilers/2023.2.4
module load intel-oneapi-mpi/2021.13.0
module load hdf5/1.14.3
module load netcdf-fortran/4.6.1
module load libjpeg-turbo/2.1.3
export NETCDF_C_ROOT=/apps/spack-managed/oneapi-2023.2.4/netcdf-c-4.9.2-qgy4pbuiliwyxhppgqgyb2jtc2vgfhzf
export NETCDF_FORTRAN_ROOT=/apps/spack-managed/oneapi-2023.2.4/netcdf-fortran-4.6.1-6agxmmk6cbyavt472y6ds2d3b5ppekni
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$NETCDF_C_ROOT/lib:$NETCDF_FORTRAN_ROOT/lib:/apps/other/pyferret-7.6.0/lib
ulimit -s unlimited
echo "Model started:  " $(date)
# Number of scribes
NUM_SCRIBES=9
# SCHISM executable
SCHISM_EXEC=./{executable}
# Run SCHISM with srun
srun --label -n $SLURM_NTASKS $SCHISM_EXEC $NUM_SCRIBES
echo "Model ended:    " $(date)
"""

    return job_card_content

def main():
    parser = argparse.ArgumentParser(description="Generate a job card for SCHISM")
    parser.add_argument("--wwm", action="store_true", help="Use WWM version of the executable")
    parser.add_argument("--cluster", choices=["hercules", "frontera"], required=True, help="Specify the cluster")
    
    args = parser.parse_args()

    job_card = generate_job_card(args.wwm, args.cluster)

    # directory path
    workdir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'workdir'))

    # Create the directory if it doesn't exist
    os.makedirs(workdir, exist_ok=True)


    job_card_path = os.path.join(workdir, "job_card")

    # Write the job card 
    with open(job_card_path, "w") as f:
        f.write(job_card)

    print(f"Job card has been generated successfully in {job_card_path}")

if __name__ == "__main__":
    main()
