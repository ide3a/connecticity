# %% NAMES OF THE LID CONTROLS

class lidNames():
    bio_retention_cell_short = 'BC'
    bio_retention_cell = 'bio_retention_cell'
    green_roof_short = 'GR'
    green_roof = 'green_roof'
    permeable_pavement_short = 'PP'
    permeable_pavement = 'permeable_pavement'
    rain_garden_short = 'RG'
    rain_garden = 'rain_garden'
    rain_barrel_short = 'RB'
    rain_barrel = 'rain_barrel'


# %% LID LAYERS

class lidLayers():
    layers_ext = '_layers'

    surface_layer = 'surface'
    soil_layer = 'soil'
    storage_layer = 'storage'
    drain_layer = 'drain'
    drainmat_layer = 'drainmat'
    pavement_layer = 'pavement'


# %% LID PARAMETERS

class lidParams():
    berm_height = 'berm_height'
    vegetative_volume = 'vegetative_volume'
    surface_roughness = 'surface_roughness'
    surface_slope = 'surface_slope'
    swale_side_slope = 'swale_side_slope'

    thickness = 'thickness'
    porosity = 'porosity'
    field_capacity = 'field_capacity'
    wilting_point = 'wilting_point'
    conductivity = 'conductivity'
    conductivity_slope = 'conductivity_slope'
    suction_head = 'suction_head'

    void_ratio = 'void_ratio'
    seepage_rate = 'seepage_rate'
    clogging_factor = 'clogging_factor'

    flow_coefficient = 'flow_coefficient'
    flow_exponent = 'flow_exponent'
    offset = 'offset'
    open_level = 'open_level'
    closed_level = 'closed_level'
    control_curve = 'control_curve'

    void_fraction = 'void_fraction'
    roughness = 'roughness'

    impervious_surface_fraction = 'impervious_surface_fraction'
    permeability = 'permeability'
    regeneration_interval = 'regeneration_interval'
    regeneration_fraction = 'regeneration_fraction'


# %% LID PARAMETERS PER LAYER

class lidParamsPerLayer():
    layer_param_names_ext = '_layer_param_names'

    surface_layer_param_names = [lidParams.berm_height, lidParams.vegetative_volume, lidParams.surface_roughness,
                                 lidParams.surface_slope, lidParams.swale_side_slope]
    soil_layer_param_names = [lidParams.thickness, lidParams.porosity, lidParams.field_capacity,
                              lidParams.wilting_point, lidParams.conductivity, lidParams.conductivity_slope,
                              lidParams.suction_head]
    storage_layer_param_names = [lidParams.thickness, lidParams.void_ratio, lidParams.seepage_rate,
                                 lidParams.clogging_factor]
    drain_layer_param_names = [lidParams.flow_coefficient, lidParams.flow_exponent, lidParams.offset,
                               lidParams.open_level, lidParams.closed_level, lidParams.control_curve]
    drainmat_layer_param_names = [lidParams.thickness, lidParams.void_fraction, lidParams.roughness]
    pavement_layer_param_names = [lidParams.thickness, lidParams.void_ratio, lidParams.impervious_surface_fraction,
                                  lidParams.permeability, lidParams.clogging_factor, lidParams.regeneration_interval,
                                  lidParams.regeneration_fraction]


# %% LAYERS PER LID CONTROL

class lidLayersPerControl():
    bio_retention_cell_layers = [lidLayers.surface_layer, lidLayers.soil_layer, lidLayers.storage_layer,
                                 lidLayers.drain_layer]
    green_roof_layers = [lidLayers.surface_layer, lidLayers.soil_layer, lidLayers.drainmat_layer]
    permeable_pavement_layers = [lidLayers.surface_layer, lidLayers.pavement_layer, lidLayers.soil_layer,
                                 lidLayers.storage_layer, lidLayers.drain_layer]
    rain_garden_layers = [lidLayers.surface_layer, lidLayers.soil_layer, lidLayers.storage_layer]
    rain_barrel_layers = [lidLayers.storage_layer, lidLayers.drain_layer]


# %% STANDARD VALUES PER LID CONTROL

class lidParamStdValues():
    param_defaults_ext = '_layer_param_defaults'

    # BIORETENTION CELL - BC
    surface_layer_param_defaults_BC = [200, 0.0, 0.2, 0.0, 5]
    soil_layer_param_defaults_BC = [800, 0.4, 0.135, 0.05, 358, 42.1, 71.7]
    storage_layer_param_defaults_BC = [300, 0.653, 1, 0]
    drain_layer_param_defaults_BC = [0, 0.5, 6, 6, 0, 0]

    # GREENROOF - GR
    surface_layer_param_defaults_GR = [50, 0.2, 0.13, 1.0, 5]
    soil_layer_param_defaults_GR = [200, 0.5, 0.3, 0.1, 0.5, 10.0, 3.5]
    drainmat_layer_param_defaults_GR = [60, 0.43, 0.03]

    # PERMEABLE PAVEMENT - PP
    surface_layer_param_defaults_PP = [25, 0.0, 0.12, 1.0, 5]
    pavement_layer_param_defaults_PP = [60, 0.13, 0, 200, 0, 0, 0]
    soil_layer_param_defaults_PP = [150, 0.5, 0.2, 0.1, 0.5, 10.0, 45]
    storage_layer_param_defaults_PP = [250, 0.43, 600, 0]
    drain_layer_param_defaults_PP = [0.69, 0.5, 6, 6, 0, 0]

    # RAIN GARDEN - RG
    surface_layer_param_defaults_RG = [150, 0.1, 0.12, 0.3, 5]
    soil_layer_param_defaults_RG = [500, 0.3, 0.2, 0.1, 500, 10.0, 3.5]
    storage_layer_param_defaults_RG = [0, 0.75, 400, 0]

    # RAIN BARREL - RB
    storage_layer_param_defaults_RB = [990.6, 0.75, 0.5, 0]
    drain_layer_param_defaults_RB = [298, 0.5, 101.6, 6, 0, 0]