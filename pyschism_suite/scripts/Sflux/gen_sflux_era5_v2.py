import numpy as np
import pandas as pd
import netCDF4 as nc
from datetime import datetime, timedelta
from time import time
import pathlib
from pyschism.mesh.hgrid import Hgrid

class LocalERA5DataInventory:
    def __init__(self, file_path, start_date, rnday):
        self.file_path = pathlib.Path(file_path)
        self.start_date = start_date
        self.rnday = rnday
        self.end_date = self.start_date + timedelta(days=self.rnday + 1)
        
    @property
    def files(self):
        return [self.file_path]
    
    @property
    def lon(self):
        with nc.Dataset(self.file_path) as ds:
            return ds.variables['longitude'][:]
    
    @property
    def lat(self):
        with nc.Dataset(self.file_path) as ds:
            return ds.variables['latitude'][:]
    
    def xy_grid(self):
        return np.meshgrid(self.lon, self.lat)

def put_sflux_fields(iday, date, timevector, ds, nx_grid, ny_grid, air, rad, prc, output_interval, OUTDIR):
    rt = pd.to_datetime(str(date))
    idx = np.where(rt == timevector)[0].item()
    times = [i/24 for i in range(0, 25, output_interval)]

    if air:
        with nc.Dataset(OUTDIR / f"sflux_air_1.{iday+1:04d}.nc", 'w', format='NETCDF3_CLASSIC') as dst:
            dst.setncatts({"Conventions": "CF-1.0"})
            dst.createDimension('nx_grid', nx_grid.shape[1])
            dst.createDimension('ny_grid', ny_grid.shape[0])
            dst.createDimension('time', None)
            
            v_lon = dst.createVariable('lon', 'f4', ('ny_grid', 'nx_grid'))
            v_lon.long_name = "Longitude"
            v_lon.standard_name = "longitude"
            v_lon.units = "degrees_east"
            v_lon[:] = nx_grid

            v_lat = dst.createVariable('lat', 'f4', ('ny_grid', 'nx_grid'))
            v_lat.long_name = "Latitude"
            v_lat.standard_name = "latitude"
            v_lat.units = "degrees_north"
            v_lat[:] = ny_grid

            v_time = dst.createVariable('time', 'f4', ('time',))
            v_time.long_name = 'Time'
            v_time.standard_name = 'time'
            v_time.units = f'days since {rt.year}-{rt.month:02d}-{rt.day:02d} 00:00 UTC'
            v_time.base_date = (rt.year, rt.month, rt.day, 0)
            v_time[:] = times

            v_prmsl = dst.createVariable('prmsl', 'f4', ('time', 'ny_grid', 'nx_grid'))
            v_prmsl.long_name = "Pressure reduced to MSL"
            v_prmsl.standard_name = "air_pressure_at_sea_level"
            v_prmsl.units = "Pa"
            v_prmsl[:,:,:] = ds['msl'][idx:idx+25:output_interval, :, :]

            v_spfh = dst.createVariable('spfh', 'f4', ('time', 'ny_grid', 'nx_grid'))
            v_spfh.long_name = "Surface Specific Humidity (2m AGL)"
            v_spfh.standard_name = "specific_humidity"
            v_spfh.units = "1"
            d2m = ds['d2m'][idx:idx+25:output_interval, :, :]
            msl = ds['msl'][idx:idx+25:output_interval, :, :]
            Td = d2m - 273.15
            e1 = 6.112 * np.exp((17.67*Td)/(Td + 243.5))
            spfh = (0.622*e1)/(msl*0.01 - (0.378*e1))
            v_spfh[:,:,:] = spfh

            v_stmp = dst.createVariable('stmp', 'f4', ('time', 'ny_grid', 'nx_grid'))
            v_stmp.long_name = "Surface Air Temperature (2m AGL)"
            v_stmp.standard_name = "air_temperature"
            v_stmp.units = "K"
            v_stmp[:,:,:] = ds['t2m'][idx:idx+25:output_interval, :, :]

            v_uwind = dst.createVariable('uwind', 'f4', ('time', 'ny_grid', 'nx_grid'))
            v_uwind.long_name = "Surface Eastward Air Velocity (10m AGL)"
            v_uwind.standard_name = "eastward_wind"
            v_uwind.units = "m/s"
            v_uwind[:,:,:] = ds['u10'][idx:idx+25:output_interval, :, :]

            v_vwind = dst.createVariable('vwind', 'f4', ('time', 'ny_grid', 'nx_grid'))
            v_vwind.long_name = "Surface Northward Air Velocity (10m AGL)"
            v_vwind.standard_name = "northward_wind"
            v_vwind.units = "m/s"
            v_vwind[:,:,:] = ds['v10'][idx:idx+25:output_interval, :, :]

    if prc:
        with nc.Dataset(OUTDIR / f"sflux_prc_1.{iday+1:04d}.nc", 'w', format='NETCDF3_CLASSIC') as dst:
            dst.setncatts({"Conventions": "CF-1.0"})
            dst.createDimension('nx_grid', nx_grid.shape[1])
            dst.createDimension('ny_grid', ny_grid.shape[0])
            dst.createDimension('time', None)
            
            v_lon = dst.createVariable('lon', 'f4', ('ny_grid', 'nx_grid'))
            v_lon.long_name = "Longitude"
            v_lon.standard_name = "longitude"
            v_lon.units = "degrees_east"
            v_lon[:] = nx_grid

            v_lat = dst.createVariable('lat', 'f4', ('ny_grid', 'nx_grid'))
            v_lat.long_name = "Latitude"
            v_lat.standard_name = "latitude"
            v_lat.units = "degrees_north"
            v_lat[:] = ny_grid

            v_time = dst.createVariable('time', 'f4', ('time',))
            v_time.long_name = 'Time'
            v_time.standard_name = 'time'
            v_time.units = f'days since {rt.year}-{rt.month:02d}-{rt.day:02d} 00:00 UTC'
            v_time.base_date = (rt.year, rt.month, rt.day, 0)
            v_time[:] = times

            v_prate = dst.createVariable('prate', 'f4', ('time', 'ny_grid', 'nx_grid'))
            v_prate.long_name = "Surface Precipitation Rate"
            v_prate.standard_name = "precipitation_flux"
            v_prate.units = "kg/m^2/s"
            tp = ds['tp'][idx:idx+25:output_interval, :, :]
            prate = tp / (3600 * output_interval)  # Convert from m to m/s
            v_prate[:,:,:] = prate

    if rad:
        print("Radiation data not available in the provided ERA5 file.")

if __name__ == '__main__':
    startdate = datetime(1994, 10, 12)
    rnday = 3
    t0 = time()
    hgrid = Hgrid.open('/work/noaa/nosofs/mjisan/pyschism-main/PySCHISM_tutorial/data/hgrid.gr3', crs='EPSG:4326')
    bbox = hgrid.get_bbox('EPSG:4326', output_type='bbox')
    outdir = pathlib.Path('../../workdir/')
    interval = 1
    local_era5_file = 'data_stream-oper.nc'  # Your downloaded ERA5 file

    inventory = LocalERA5DataInventory(local_era5_file, startdate, rnday)
    ds = nc.Dataset(local_era5_file)
    
    time_var = ds.variables['valid_time']
    times = nc.num2date(time_var[:], units=time_var.units, only_use_cftime_datetimes=False)
    
    nx_grid, ny_grid = inventory.xy_grid()

    for iday in range(rnday):
        date = startdate + timedelta(days=iday)
        put_sflux_fields(iday, date, times, ds, nx_grid, ny_grid, 
                         air=True, rad=False, prc=True, 
                         output_interval=interval, OUTDIR=outdir)

    ds.close()

    with open(outdir / "sflux_inputs.txt", "w") as f:
        f.write("&sflux_inputs\n/\n")

    print(f'It took {(time()-t0)/60} minutes to generate {rnday} days')
