#---------------------------------------------------------------------------
#
# Modeling Atlantic Forest regenerability
# 
# 2. Rasterizing shapefiles (all with the same extent and resolution = 30m)
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

###--------------------------------------------------------------------###
## Rasterize shapefiles

# Define the region of study

#grass.run_command('g.region', vector = 'limite_ma_extendido_albers_sad69_shp', res = 30, flags = 'p')
#grass.run_command('g.region', vector = 'limite_leima_ribeiroetal2009_albers_sad69_dissolve_shp', flags = 'p') 
# The above command does not set the exact resolution of 30m - we are going to add some meters to the extent to get an exact resolution of 30m

# Region of study - for the AF
grass.run_command('g.region', vector = 'limite_ma_extendido_albers_sad69_shp', res = 30, flags = 'p',
                  align = 'MA_extendido_rast') # nao da a resolucao exata 30m - vamos adicionar um pouco na extensao

# 1. Forest fragmentos of AF - SOSMA 2014 (considering forest, mangroove, humid areas, and restinga)
grass.run_command('v.to.rast', input = 'atlas_ma_sos_ma_2014_mata_restinga_mangue_albers_sad69_shp',
                  output = 'atlas_ma_sos_ma_2014_mata_restinga_mangue_albers_sad69_rast', use='val', value=1, overwrite = True)

# 2. Urban areas (SOSMA 2014 + IBGE)
grass.run_command('v.to.rast', input = 'mancha_urbana_composicao_ibge_SOS_limiteMAestendido_albers_sad69_shp',
                  output = 'urban_areas_composition_ibge_SOS_limiteMAestendido_albers_sad69_rast', use='val', value=1, overwrite = True)

# 3. Water bodies of Brazil (ANA)
grass.run_command('v.to.rast', input = 'geoft_bho_massa_dagua_albers_sad69_shp',
                  output = 'geoft_bho_massa_dagua_albers_sad69_rast', use='val', value=1, overwrite = True)

# 4. Roads of Brazil DNIT
grass.run_command('v.to.rast', input = 'dnit_pavimentada_albers_sad69_shp',
                  output = 'dnit_pavimentada_albers_sad69_rast', use='val', value=1, overwrite = True)

# 5. Tree plantations - Global Forest Watch 2013-2014
grass.run_command('v.to.rast', input = 'gfw_tree_plantations_albers_sad69_shp',
                  output = 'gfw_tree_plantations_albers_sad69_rast', use='val', value=1, overwrite = True)

# 6. Forest fragments of AF in Rio de Janeiro State - SOS Mata Atlantica 30m resolution, 2015 (considering forest, mangroove, humid areas, and restinga)
#grass.run_command('v.to.rast', input = 'atlas_sosma_rj_2014_2015_albers_sad69_shp',
                  #output = 'atlas_sosma_rj_2014_2015_albers_sad69_rast', use='attr', attribute_column='code_hab2', overwrite = True)

# 7. Forest fragments of AF - SOS Mata Atlantica 30m resolution, 2005
grass.run_command('v.to.rast', input = 'mata_atlantica_remanescentes_sad69_albers_2005_shp',
                  output = 'mata_atlantica_remanescentes_sad69_albers_2005_rast', use='val', value = 1, overwrite = True)

# 8. Sugarcane areas - Canasat 2013
grass.run_command('v.to.rast', input = 'canasat_2013_albers_sad69_shp',
                  output = 'canasat_2013_albers_sad69_rast', use='val', value = 1, overwrite = True)

# 9. Argentinian shapes

# Cities
grass.run_command('v.to.rast', input = 'areas_urbanas_AR_albers_sad69',
                  output = 'urban_areas_AR_albers_sad69_rast', use='val', value = 1, overwrite = True)
# Water 1 - rivers
grass.run_command('v.to.rast', input = 'cursos_dagua_AR_albers_sad69',
                  output = 'water_rivers_AR_albers_sad69_rast', use='val', value = 1, overwrite = True)
# Water 2 - lakes/large rivers
grass.run_command('v.to.rast', input = 'corpos_dagua_AR_albers_sad69',
                  output = 'water_bodies_AR_albers_sad69_rast', use='val', value = 1, overwrite = True)
# Mosaic water AR
grass.run_command('r.patch', input = ['water_bodies_AR_albers_sad69_rast', 'water_rivers_AR_albers_sad69_rast'], output = 'water_AR_albers_sad69_rast')
# Removing separated water maps AR
grass.run_command('g.remove', type = 'raster', pattern = 'water_bodies_AR_albers_sad69_rast', flags = 'f')
grass.run_command('g.remove', type = 'raster', pattern = 'water_rivers_AR_albers_sad69_rast', flags = 'f')
# Roads
grass.run_command('v.to.rast', input = 'rodovias_AR_albers_sad69',
                  output = 'roads_AR_albers_sad69_rast', use='val', value = 1, overwrite = True)

# 10. Paraguay shapes
# Roads
grass.run_command('v.to.rast', input = 'paraguay_2002_rutas_albers_sad69',
                  output = 'roads_PY_albers_sad69_rast', use='val', value = 1, overwrite = True)
# Rivers
grass.run_command('v.to.rast', input = 'paraguay_2002_rios_principales_albers_sad69',
                  output = 'rivers_PY_albers_sad69_rast', use='val', value = 1, overwrite = True)
