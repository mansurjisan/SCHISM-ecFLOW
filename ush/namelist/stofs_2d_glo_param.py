import argparse
from datetime import datetime
import pathlib

def generate_fort15(start_year, start_month, start_day, start_hour, rnday):
    content = f"""cycle :-6 hr nowcast and +180 hr forecast ! 32 CHARACTER ALPHANUMERIC RUN DESCRIPTION
STOFS 2D GLOBAL v5.6.5     ! 24 CHARACTER ALPHANUMERIC RUN IDENTIFICATION
1                          ! NFOVER
0                          ! NABOUT
1800                       ! NSCREEN
ihot                       ! IHOT
-22                        ! ICS
513113                     ! IM
1                          ! NOLIBF
2                          ! NOLIFA
1                          ! NOLICA
1                          ! NOLICAT
7                          ! NWP
mannings_n_at_sea_floor
subgrid_barrier
internal_tide_friction
surface_submergence_state
surface_canopy_coefficient
surface_directional_effective_roughness_length
elemental_slope_limiter
1                          ! NCOR
2                          ! NTIP
0                          ! NWS
1                          ! NRAMP
9.810000                   ! G
0.053333                   ! TAU0
6                          ! DTDP
0                          ! STATIM
0                          ! REFTIM
{rnday}                      ! RNDY
6.750000                   ! DRAMP
0.8 0.2 0                  ! A00, B00, C00
0.1 0 0 0.01               ! H0, 2*dummy, VELMIN
0.0 45.0                   ! SLAM0, SFEA0
0.000500                   ! CF
-0.200000                  ! ELSM
0.000000                   ! CORI
8                          ! NTIF
Q1                         ! TIPOTAG - NAME OF TIDAL POTENTIAL CONSTITUENT
0.01925600 0.000064958541129 0.695 fft4 facet4 ! TPK, AMIGT, ETRF, FFT, FACET - CONSTITUENT PROPERTIES
O1                         ! TIPOTAG - NAME OF TIDAL POTENTIAL CONSTITUENT
0.10051400 0.000067597744151 0.695 fft2 facet2 ! TPK, AMIGT, ETRF, FFT, FACET - CONSTITUENT PROPERTIES
P1                         ! TIPOTAG - NAME OF TIDAL POTENTIAL CONSTITUENT
0.04684300 0.000072522947400 0.706 fft3 facet3 ! TPK, AMIGT, ETRF, FFT, FACET - CONSTITUENT PROPERTIES
K1                         ! TIPOTAG - NAME OF TIDAL POTENTIAL CONSTITUENT
0.14156500 0.000072921158358 0.736 fft1 facet1 ! TPK, AMIGT, ETRF, FFT, FACET - CONSTITUENT PROPERTIES
N2                         ! TIPOTAG - NAME OF TIDAL POTENTIAL CONSTITUENT
0.04639800 0.000137879699487 0.693 fft7 facet7 ! TPK, AMIGT, ETRF, FFT, FACET - CONSTITUENT PROPERTIES
M2                         ! TIPOTAG - NAME OF TIDAL POTENTIAL CONSTITUENT
0.24233400 0.000140518902509 0.693 fft5 facet5 ! TPK, AMIGT, ETRF, FFT, FACET - CONSTITUENT PROPERTIES
S2                         ! TIPOTAG - NAME OF TIDAL POTENTIAL CONSTITUENT
0.11284100 0.000145444104333 0.693 fft6 facet6 ! TPK, AMIGT, ETRF, FFT, FACET - CONSTITUENT PROPERTIES
K2                         ! TIPOTAG - NAME OF TIDAL POTENTIAL CONSTITUENT
0.03070400 0.000145842317201 0.693 fft8 facet8 ! TPK, AMIGT, ETRF, FFT, FACET - CONSTITUENT PROPERTIES
0                          ! NBFR
90                         ! ANGINN : INNER ANGLE THRESHOLD
nout touts toutf 60        ! NOUTE,TOUTSE,TOUTFE,NSPOOLE:ELEV STATION OUTPUT INFO (UNIT  61)
-1688                      ! NSTAE - NUMBER OF ELEVATION RECORDING STATIONS, FOLLOWED BY LOCATIONS ON PROCEEDING LINES
nout touts toutf 60        ! NOUTV,TOUTSV,TOUTFV,NSPOOLV:VEL STATION OUTPUT INFO (UNIT  62)
-1688                      ! NSTAV - NUMBER OF VELOCITY RECORDING STATIONS, FOLLOWED BY LOCATIONS ON PROCEEDING LINES
nout touts toutf 600       ! NOUTGE,TOUTSGE,TOUTFGE,NSPOOLGE : GLOBAL ELEVATION OUTPUT INFO (UNIT  63)
nout touts toutf 600       ! NOUTGV,TOUTSGV,TOUTFGV,NSPOOLGV : GLOBAL VELOCITY  OUTPUT INFO (UNIT  64)
0                          ! NFREQ - NUMBER OF FREQENCIES IN HARMONIC ANALYSIS
0.0 0.0 0 0.0              ! THAS,THAF,NHAINC,FMV - HARMONIC ANALYSIS PARAMETERS
0 0 0 0                    ! NHASE,NHASV,NHAGE,NHAGV - CONTROL HARMONIC ANALYSIS AND OUTPUT TO UNITS 51,52,53,54
nhstar nhsinc              ! NHSTAR,NHSINC - HOT START FILE GENERATION PARAMETERS
1 0 1e-005 25              ! ITITER, ISLDIA, CONVCR, ITMAX - ALGEBRAIC SOLUTION PARAMETERS
STOFS_2D_GLOBAL.V2.1.0     ! NCPROJ - PROJECT TITLE
NOS/OCS/CSDL/CMMB          ! NCINST - PROJECT INSTITUTION
Dogwood/Cactus             ! NCSOUR - PROJECT SOURCE
PRODUCTION                 ! NCHIST - PROJECT HISTORY
http://www.adcirc.org      ! NCREF  - PROJECT REFERENCES
STOFS_2D_GLOBAL.V2.1.0     ! NCCOM  - PROJECT COMMENTS
NOS/OCS/CSDL/CMMB          ! NCHOST - PROJECT HOST
CF-1.0                     ! NCCONV - CONVENTIONS
Yuji.Funaoshi@noaa.gov     ! NCCONT - CONTACT INFORMATION
{start_year}-{start_month}-{start_day} {start_hour}:00:00        ! NCDASE - BASE_DATE
! -- Begin wetDry Control Namelist --
&wetDryControl outputNodeCode=.false., outputNOFF=.false., noffActive=.true.,
slim = 0.0004,
windlim = T,
directvelWD = T,
useHF = T,
/
! -- End WetDry Control Namelist --"""
    return content

def main():
    parser = argparse.ArgumentParser(description="Generate ADCIRC fort.15 file")
    parser.add_argument("--year", type=int, required=True, help="Start year")
    parser.add_argument("--month", type=int, required=True, help="Start month")
    parser.add_argument("--day", type=int, required=True, help="Start day")
    parser.add_argument("--hour", type=int, required=True, help="Start hour")
    parser.add_argument("--rnday", type=float, required=True, help="Simulation period in days")
    parser.add_argument("--workdir", type=str, required=True, help="Output Directory")

    args = parser.parse_args()

    # Validate date
    try:
        datetime(args.year, args.month, args.day, int(args.hour))
    except ValueError:
        print("Error: Invalid date or time provided.")
        return 1

    # Create content
    content = generate_fort15(args.year, args.month, args.day, args.hour, args.rnday)
    
    # Setup output directory
    outdir = pathlib.Path(args.workdir)
    if not outdir.is_dir():
        print(f"Error: The specified workdir '{args.workdir}' is not a directory.")
        return 1

    # Write output file
    outfile = outdir / "fort.15"
    try:
        with open(outfile, "w") as f:
            f.write(content)
    except Exception as e:
        print(f"Error writing fort.15: {e}")
        return 1

    print("fort.15 file has been generated successfully.")
    return 0

if __name__ == "__main__":
    exit(main())
