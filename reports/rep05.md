# Reports

## Rep 05 - 17/01/2022

### Aims

- Ribeiro et al +13 paper: metrics and status of fragmentation of AF now and in the future
- Atlantic Spatial datapaper

### Variables to calculate

- Organize land use map and elevation
  - Elevation - ready
  - Land use: finalizar a preparacao da base de dados
  - estradas mundial - gRoads?
  - urbano - mapbiomas/IBGE
  - pastagens - mapbiomas
  - agricultura - temporaria, perene
  - Remove only roads and urban areas
  - Para integrar: r.mapcalc with "if(condition, true, false)" structure

- Forest metrics
  - Retomar quais sao 

- Proportion of different classes
  - Scales: 250, 500, 750, 1000, 1500, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 15000, 20000

- Landscape heterogeneity/diversity
  - Start simple, with macro-classes
    - forest, pasture, agriculture (perennial, temporary), planted forests, water?

- Elevation-related metrics
  - elevation
  - slope
  - aspect
  - northness, eastness (é o mesmo que aspect?)
  - TPI?
  - TWI? wetness index
  - SD declividade 

- Format for making data available:
  - Pangeia spatial database
  - cloud optimized geotiff (cogeo.org)
  - OSF
  - Zenodo  
  - FBDS
  - Google Earth Engine

- Natural regeneration potential model
  - Script here: https://github.com/LEEClab/seed_dispersal_mapper
  - It works, but we could easily transform it into a GRASS GIS addon.
  - And later implement it into R (through R-GRASS link or within R directly)

- Schedule
  - 
