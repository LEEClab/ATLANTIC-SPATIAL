#---------------------------------------------------------------------------
#
# Modeling Atlantic Forest regenerability
# 
# 3. Combining maps to define a final raster map of natural vegetation
#    in the extended limit of the Atlantic Forest
# Including FBDS map
#
# Bernardo BS Niebuhr - bernardo_brandaum@yahoo.com.br
# Mauricio Humberto Vancine
#
# 02/06/2017
# Feel free to modify and share this code
#---------------------------------------------------------------------------

###--------------------------------------------------------------------###
## Import python modules
import os # operational system commands
import grass.script as grass # GRASS GIS commands
###--------------------------------------------------------------------###

# 1. Gather FBDS maps for all regions and all uses and export

# Region of study - for gathering FBDS maps regardless of AF limits

# # First trial - set it manually - NO!
#grass.run_command('g.region', n=3028995, s=138585, w=-74890, e=2742860, res = 30, flags = 'p') 
#grass.run_command('g.region', vector = 'limite_leima_ribeiroetal2009_albers_sad69_dissolve_shp', res = 30, flags = 'ap') 

# List of maps
maps_fbds = grass.list_grouped('rast', pattern = '*v2*')['PERMANENT']

# Region of study
# # Second trial - align it to the resolution - problem - the pixels may displace a little!!
grass.run_command('g.region', rast = maps_fbds, res = 30, flags = 'ap') 

# # Third trial - use base map and increase an extesion to the west (dividible by the resolution 30m) to include all states
grass.run_command('g.region', rast = 'MA_extendido_rast', flags = 'p') # This extension already has resolution = 30m
grass.run_command('g.region', w = 'w-300000', flags = 'p') # reduce the west limit in 300km, which inclues all FBDS state maps and is divisible per 30
# this is ok! we kept only that.

# Combine maps
grass.run_command('r.patch', input = maps_fbds, output = 'FBDS_map_all_states', overwrite = True)

# Export FBDS map for all uses
folder = r'G:\regenerabilidade_MA\02_saidas\FBDS_combined'
os.chdir(folder)
grass.run_command('r.out.gdal', input = 'FBDS_map_all_states', output = 'FBDS_map_all_states.tif')
# With compression
grass.run_command('r.out.gdal', input = 'FBDS_map_all_states', output = 'FBDS_map_all_states_compressed.tif', createopt="COMPRESS=DEFLATE")

# 2. Gather FBDS maps for all regions and each use separately, and export

out_dir = r'G:\regenerabilidade_MA\02_saidas\FBDS_combined\separated_classes'
os.chdir(out_dir)

# 1 = water
expression1 = 'FBDS_map_all_states_water = if(FBDS_map_all_states == 1, 1, 0)'
grass.mapcalc(expression1, overwrite = True)

grass.run_command('r.out.gdal', input = 'FBDS_map_all_states_water', output = 'FBDS_map_all_states_water.tif')

# 2 = antropic areas
expression2 = 'FBDS_map_all_states_antropic_areas = if(FBDS_map_all_states == 2, 1, 0)'
grass.mapcalc(expression2, overwrite = True)

grass.run_command('r.out.gdal', input = 'FBDS_map_all_states_antropic_areas', output = 'FBDS_map_all_states_antropic_areas.tif')

# 3 = building area
expression3 = 'FBDS_map_all_states_building_areas = if(FBDS_map_all_states == 3, 1, 0)'
grass.mapcalc(expression3, overwrite = True)

grass.run_command('r.out.gdal', input = 'FBDS_map_all_states_building_areas', output = 'FBDS_map_all_states_building_areas.tif')

# 4 = forest
expression4 = 'FBDS_map_all_states_forest = if(FBDS_map_all_states == 4, 1, 0)'
grass.mapcalc(expression4, overwrite = True)

grass.run_command('r.out.gdal', input = 'FBDS_map_all_states_forest', output = 'FBDS_map_all_states_forest.tif')

# 5 = non forest natural areas
expression5 = 'FBDS_map_all_states_non_forest_natural_areas = if(FBDS_map_all_states == 5, 1, 0)'
grass.mapcalc(expression5, overwrite = True)

grass.run_command('r.out.gdal', input = 'FBDS_map_all_states_non_forest_natural_areas', output = 'FBDS_map_all_states_non_forest_natural_areas.tif')

# 6 = silviculture
expression6 = 'FBDS_map_all_states_silviculture = if(FBDS_map_all_states == 6, 1, 0)'
grass.mapcalc(expression6, overwrite = True)

grass.run_command('r.out.gdal', input = 'FBDS_map_all_states_silviculture', output = 'FBDS_map_all_states_silviculture.tif')

# better to do 1/null??

# Exporting compressed
per_class_maps_fbds = grass.list_grouped('rast', pattern = 'FBDS_map_all_states_*') ['PERMANENT']
out_dir = r'G:\regenerabilidade_MA\02_saidas\FBDS_combined\separated_classes'
os.chdir(out_dir)

for i in per_class_maps_fbds:
    # With compression
    grass.run_command('r.out.gdal', input = i, output = i+'_compressed.tif', createopt="COMPRESS=DEFLATE")
    

# 3. Cross sugarcane and pasture with antropic areas of FBDS map

# Region
grass.run_command('g.region', raster = 'FBDS_map_all_states', flags = 'p')
grass.run_command('g.region', zoom = 'FBDS_map_all_states', flags = 'p') # This extension already has resolution = 30m

# Cross maps
# First overlap sugarcane
expression7 = 'FBDS_antropic_areas1_sugarcane7 = if(isnull(canasat_2013_albers_sad69_rast), FBDS_map_all_states_antropic_areas, 7)'
grass.mapcalc(expression7, overwrite = True)
# Then, overlap pasture
expression8 = 'FBDS_antropic_areas1_pasture8 = if(pastagens_br_2015_albers_sad69_tif == 1 &&& FBDS_antropic_areas1_sugarcane7 != 7, 8, FBDS_antropic_areas1_sugarcane7)'
grass.mapcalc(expression8, overwrite = True)
# Consider sugarcane and pasture only where antropic areas == 1
expression9 = 'FBDS_antropic_areas1_sugarcane7_pasture8 = if(FBDS_map_all_states_antropic_areas == 0, 0, FBDS_antropic_areas1_pasture8)'
grass.mapcalc(expression9, overwrite = True)

# Remove intermediate maps
grass.run_command('g.remove', type = 'raster', pattern = 'FBDS_antropic_areas1_sugarcane7', flags = 'f')
grass.run_command('g.remove', type = 'raster', pattern = 'FBDS_antropic_areas1_pasture8', flags = 'f')

# Export
out_dir = r'G:\regenerabilidade_MA\02_saidas\FBDS_combined\separated_classes'
os.chdir(out_dir)

grass.run_command('r.out.gdal', input = 'FBDS_antropic_areas1_sugarcane7_pasture8', output = 'FBDS_antropic_areas1_sugarcane7_pasture8.tif')
grass.run_command('r.out.gdal', input = 'FBDS_antropic_areas1_sugarcane7_pasture8', output = 'FBDS_antropic_areas1_sugarcane7_pasture8_compressed.tif', createopt="COMPRESS=DEFLATE")

#------------------------------------------
# 3. Maps for the expanded AF (the consensus limit) - resolution 30m

out_dir_ext_AF = r'G:\regenerabilidade_MA\02_saidas\extended_AF_consensus_30m'
os.chdir(out_dir_ext_AF)

maps_export = []

# Region of study - for the AF
grass.run_command('g.region', vector = 'limit_af_consensus_maa_ribeiroetal2009_lawaf2006_wwf_albers_sad69', res = 30, flags = 'p',
                  align = 'MA_extendido_rast') # nao da a resolucao exata 30m - vamos adicionar um pouco na extensao

# Mask for the AF limit
grass.run_command('r.mask', vector = 'limit_af_consensus_maa_ribeiroetal2009_lawaf2006_wwf_albers_sad69') # Mask for the extended AF

# a. FBDS map for this delimitation

# FBDS map
grass.mapcalc('FBDS_map_extended_AF = FBDS_map_all_states', overwrite = True) # Filling SP with a binary map of forest patches
maps_export = maps_export + ['FBDS_map_extended_AF']

# b. Get only FBDS forest
# With 1/0
grass.mapcalc('FBDS_map_extended_AF_forest = if(FBDS_map_all_states == 4, 1, 0)', overwrite = True)
# With 1/null
grass.mapcalc('FBDS_map_extended_AF_forest_1null = if(FBDS_map_all_states == 4, 1, null())', overwrite = True)

maps_export = maps_export + ['FBDS_map_extended_AF_forest_1null']

# c. SOS MA forest map - 2014

# already calculated for 30m
maps_export = maps_export + ['atlas_ma_sos_ma_2014_mata_restinga_mangue_albers_sad69_rast']

# SOS MA forest map - 2005? export ou mosaic? We won't use it
# mapbiomas all? mapbiomas only forest? mapbiomas only forest < 10ha? export ou mosaic? which biome? We won't use it

# d. map of cities - FBDS + cities(SOS+IBGE) + Argentina

#### CHANGE HERE LATER WHEN PY CITIES IS UPDATED

# Mosaic
maps_cities = ['FBDS_map_all_states_building_areas', 'urban_areas_composition_ibge_SOS_limiteMAestendido_albers_sad69_rast', 'urban_areas_AR_albers_sad69_rast']
grass.run_command('r.patch', input = maps_cities, output = 'cities_FBDS_SOS_IBGE_AR', overwrite = True)

# Version 1/null
expression10 = 'cities_FBDS_SOS_IBGE_AR_1null = if(cities_FBDS_SOS_IBGE_AR == 1, 1, null())'
grass.mapcalc(expression10, overwrite = True)

# Version 1/0
expression11 = 'cities_FBDS_SOS_IBGE_AR_1_0 = if(isnull(cities_FBDS_SOS_IBGE_AR_1null), 0, 1)'
grass.mapcalc(expression11, overwrite = True)

# Remove temp map
grass.run_command('g.remove', type = 'raster', pattern = 'cities_FBDS_SOS_IBGE_AR', flags = 'f')

maps_export = maps_export + ['cities_FBDS_SOS_IBGE_AR_1_0']

# e. forest map Paraguay and Argentina (without considering forest plantation GFW, cities, roads, and water)
#### CHANGE HERE LATER WHEN PY CITIES IS UPDATED

expression12 = 'hansen_2000_treecover_threshold95_no_forestry_no_cities = if(isnull(gfw_tree_plantations_albers_sad69_rast) &&& \
isnull(cities_FBDS_SOS_IBGE_AR_1null) &&& \
isnull(water_AR_albers_sad69_rast) &&& \
isnull(roads_AR_albers_sad69_rast) &&& \
isnull(roads_PY_albers_sad69_rast) &&& \
isnull(rivers_PY_albers_sad69_rast) &&& \
hansen_2000_treecover_threshold95_albers_sad69 > 0, 1, null())'
grass.mapcalc(expression12, overwrite = True)

maps_export = maps_export + ['hansen_2000_treecover_threshold95_no_forestry_no_cities']

# f. water map FBDS + ANA + Argentina

#### CHANGE HERE LATER WHEN PY AND AR WATER MAPS ARE UPDATED

# mosaic ANA + FBDS + AR
maps_water = ['geoft_bho_massa_dagua_albers_sad69_rast', 'FBDS_map_all_states_water', 'water_AR_albers_sad69_rast', 'rivers_PY_albers_sad69_rast']
grass.run_command('r.patch', input = maps_water, output = 'water_FBDS_ANA_AR', overwrite = True)

# transform in 1/null
expression13 = 'water_FBDS_ANA_AR_1null = if(water_FBDS_ANA_AR == 1, 1, null())'
grass.mapcalc(expression13, overwrite = True)

# transform in 1/0
expression14 = 'water_FBDS_ANA_AR_1_0 = if(isnull(water_FBDS_ANA_AR_1null), 0, 1)'
grass.mapcalc(expression14, overwrite = True)

# remove aux map
grass.run_command('g.remove', type = 'raster', pattern = 'water_FBDS_ANA_AR', flags = 'f')

maps_export = maps_export + ['water_FBDS_ANA_AR_1_0']

# g. Roads DNIT + Py + Ar

# Removing roads AR which overlap with Brazilian territory
expression15 = 'roads_AR_albers_sad69_rast_no_BR = if(isnull(FBDS_map_extended_AF), roads_AR_albers_sad69_rast, null())'
grass.mapcalc(expression15, overwrite = True)

# Mosaic
maps_road = ['dnit_pavimentada_albers_sad69_rast', 'roads_PY_albers_sad69_rast', 'roads_AR_albers_sad69_rast_no_BR']
grass.run_command('r.patch', input = maps_road, output = 'roads_DNIT_PY_AR', overwrite = True)

# transform in 1/0
expression16 = 'roads_DNIT_PY_AR_1_0 = if(isnull(roads_DNIT_PY_AR), 0, 1)'
grass.mapcalc(expression16, overwrite = True)

# remove aux map
grass.run_command('g.remove', type = 'raster', pattern = 'roads_AR_albers_sad69_rast_no_BR', flags = 'f')

maps_export = maps_export + ['roads_DNIT_PY_AR_1_0']

# h. FBDS antropic use + sugarcane and pasture

maps_export = maps_export + ['FBDS_antropic_areas1_sugarcane7_pasture8']

# i. pasture LAPIG 2015 (which are inside antropic areas nor crossed by water or roads)

# within FBDS limit - pasture inside antropic areas
expression17 = 'pasture_br_FBDS_limit_AF = if(FBDS_antropic_areas1_sugarcane7_pasture8 == 8, 1, 0)'
grass.mapcalc(expression17, overwrite = True)

# for outside FBDS area - pasture which is not forest SOS 2014 nor Hansen 2000
expression18 = 'pasture_br_non_SOSMA_2014_Hansen = if(pastagens_br_2015_albers_sad69_tif == 1 &&& \
isnull(atlas_ma_sos_ma_2014_mata_restinga_mangue_albers_sad69_rast) &&& \
isnull(hansen_2000_treecover_threshold95_no_forestry_no_cities), 1, 0)'
grass.mapcalc(expression18, overwrite = True)

# mosic pasture inside FBDS limit + outside
grass.run_command('r.patch', input = 'pasture_br_FBDS_limit_AF,pasture_br_non_SOSMA_2014_Hansen', output = 'pasture_non_forest_BR_2015', overwrite = True)

# exclude areas in which there is water and roads
expression19 = 'pasture_non_forest_water_roads_cities_BR_2015 = if(pasture_non_forest_BR_2015 >= 1 &&& \
!isnull(pasture_non_forest_BR_2015) &&& \
isnull(roads_DNIT_PY_AR) &&& \
isnull(water_FBDS_ANA_AR_1null) &&& \
isnull(cities_FBDS_SOS_IBGE_AR_1null), 1, 0)'
grass.mapcalc(expression19, overwrite = True)

# remove aux map
grass.run_command('g.remove', type = 'raster', pattern = 'pasture_br_FBDS_limit_AF', flags = 'f')
grass.run_command('g.remove', type = 'raster', pattern = 'pasture_non_forest_BR_2015', flags = 'f')
grass.run_command('g.remove', type = 'raster', pattern = 'pasture_br_non_SOSMA_2014_Hansen', flags = 'f')

maps_export = maps_export + ['pasture_non_forest_water_roads_cities_BR_2015']

# j. Combine vegetation maps

# SOS MA forest fragment without cities
expression20 = 'forest_sos_no_cities = if(!isnull(atlas_ma_sos_ma_2014_mata_restinga_mangue_albers_sad69_rast) &&& isnull(cities_FBDS_SOS_IBGE_AR_1null), 1, null())'
grass.mapcalc(expression20, overwrite = True)

# combine FBDS forest with SOSMA no cities and Hansen 2000 (without cities and forestry)
maps_forest = ['FBDS_map_extended_AF_forest', 'forest_sos_no_cities', 'hansen_2000_treecover_threshold95_no_forestry_no_cities']
grass.run_command('r.patch', input = maps_forest, output = 'FBDS_AF_forest_sos_2014_Hansen_no_cities', overwrite = True)

#and subtract water and roads
expression21 = 'FBDS_AF_forest_sos_2014_Hansen_no_cities_water_roads = if(FBDS_AF_forest_sos_2014_Hansen_no_cities > 0 &&& \
!isnull(FBDS_AF_forest_sos_2014_Hansen_no_cities) &&& \
isnull(roads_DNIT_PY_AR) &&& \
isnull(water_FBDS_ANA_AR_1null), FBDS_AF_forest_sos_2014_Hansen_no_cities, null())'
grass.mapcalc(expression21, overwrite = True)

maps_export = maps_export + ['FBDS_AF_forest_sos_2014_Hansen_no_cities_water_roads']

# Transform into 1/0
expression22 = 'FBDS_AF_forest_sos_2014_Hansen_no_cities_water_roads_1_0 = if(isnull(FBDS_AF_forest_sos_2014_Hansen_no_cities_water_roads), 0, 1)'
grass.mapcalc(expression22, overwrite = True)

maps_export = maps_export + ['FBDS_AF_forest_sos_2014_Hansen_no_cities_water_roads_1_0']

# Remove intermediate maps
grass.run_command('g.remove', type = 'raster', pattern = 'FBDS_AF_forest_sos_2014_Hansen_no_cities', flags = 'f')

# Exporting maps 30m
out_dir_ext_AF = r'G:\regenerabilidade_MA\02_saidas\extended_AF_consensus_30m'
os.chdir(out_dir_ext_AF)

for i in maps_export:
    # Without compression
    grass.run_command('r.out.gdal', input = i, output = i+'_30m.tif')    
    # With compression
    grass.run_command('r.out.gdal', input = i, output = i+'_30m_compressed.tif', createopt="COMPRESS=DEFLATE")

grass.run_command('r.mask', flags = 'r') # Remove mask

#------------------------------------------
# 3. Maps of vegetation and pasture for the AF (limit AF law + Ribeiro et al 2009) - resolution 30m
# For inferring AF regenerability

# Region of study - for the AF
grass.run_command('g.region', vector = 'limite_leima_ribeiroetal2009_albers_sad69_shp', res = 30, flags = 'p',
                  align = 'MA_extendido_rast')

# Mask for the AF limit
grass.run_command('r.mask', vector = 'limite_leima_ribeiroetal2009_albers_sad69_shp') # Mask for the extended AF

# Export vegetation map and pasture map

mapas_export_regen = ['FBDS_AF_forest_sos_2014_Hansen_no_cities_water_roads_1_0', 'pasture_non_forest_water_roads_cities_BR_2015']

# Exporting maps 30m
out_dir_ext_AF = r'G:\regenerabilidade_MA\02_saidas\regenerability_leima_Ribeiro_30m'
os.chdir(out_dir_ext_AF)

for i in mapas_export_regen:
    # Without compression
    grass.run_command('r.out.gdal', input = i, output = i+'_30m.tif')    
    # With compression
    grass.run_command('r.out.gdal', input = i, output = i+'_30m_compressed.tif', createopt="COMPRESS=DEFLATE")

grass.run_command('r.mask', flags = 'r') # Remove mask

#------------------------------------------
# 4. Maps for the expanded AF (the consensus limit) - resolution 1km

maps_export = []

# Region of study - for the AF
grass.run_command('g.region', vector = 'limit_af_consensus_maa_ribeiroetal2009_lawaf2006_wwf_albers_sad69', res = 1000, flags = 'ap') 

# Mask
grass.run_command('r.mask', vector = 'limit_af_consensus_maa_ribeiroetal2009_lawaf2006_wwf_albers_sad69') # Mask for the extended AF

# a. FBDS map for this delimitation

# FBDS map
maps_export = maps_export + ['FBDS_map_extended_AF']

# b. FBDS only forest
maps_export = maps_export + ['FBDS_map_extended_AF_forest_1null']

# c. SOS MA forest map - 2014

# already calculated for 30m
maps_export = maps_export + ['atlas_ma_sos_ma_2014_mata_restinga_mangue_albers_sad69_rast']

# d. map of cities - FBDS + cities(SOS+IBGE) + Argentina

#### CHANGE HERE LATER WHEN PY CITIES IS UPDATED

maps_export = maps_export + ['cities_FBDS_SOS_IBGE_AR_1_0']

# e. forest map Paraguay and Argentina (without considering forest plantation GFW, cities, roads, and water)
#### CHANGE HERE LATER WHEN PY CITIES IS UPDATED

maps_export = maps_export + ['hansen_2000_treecover_threshold95_no_forestry_no_cities']

# f. water map FBDS + ANA + Argentina

#### CHANGE HERE LATER WHEN PY AND AR WATER MAPS ARE UPDATED

maps_export = maps_export + ['water_FBDS_ANA_AR_1_0']

# g. Roads DNIT + Py + Ar

maps_export = maps_export + ['roads_DNIT_PY_AR_1_0']

# h. FBDS antropic use + sugarcane and pasture

maps_export = maps_export + ['FBDS_antropic_areas1_sugarcane7_pasture8']

# i. pasture LAPIG 2015 (which are inside antropic areas nor crossed by water or roads)

maps_export = maps_export + ['pasture_non_forest_water_roads_cities_BR_2015']

# j. Combine vegetation maps

maps_export = maps_export + ['FBDS_AF_forest_sos_2014_Hansen_no_cities_water_roads']

maps_export = maps_export + ['FBDS_AF_forest_sos_2014_Hansen_no_cities_water_roads_1_0']

# Exporting maps 1km
out_dir_ext_AF = r'G:\regenerabilidade_MA\02_saidas\extended_AF_consensus_1km'
os.chdir(out_dir_ext_AF)

for i in maps_export:
    # Without compression
    grass.run_command('r.out.gdal', input = i, output = i+'_1km.tif')    
    # With compression
    grass.run_command('r.out.gdal', input = i, output = i+'_1km_compressed.tif', createopt="COMPRESS=DEFLATE")

grass.run_command('r.mask', flags = 'r') # Remove mask


