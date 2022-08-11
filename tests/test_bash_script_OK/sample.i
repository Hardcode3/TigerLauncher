[Mesh]
  type = GeneratedMesh
  dim = 3
  nx = 2
  ny = 10
  nz = 2
  ymax = 0
  ymin = -1
[]

[GlobalParams]
  displacements = 'disp_x disp_y disp_z'
[]

[Modules]
  [./TensorMechanics]
    [./Master]
      [./all]
        add_variables = true
        strain = SMALL
        incremental = true
        temperature = temp
        eigenstrain_names = 'reduced_eigenstrain'
        additional_generate_output = 'stress_yy stress_xx stress_zz vonmises_stress'
      [../]
    [../]
  [../]
  [./FluidProperties]
    [./water_uo]
    type = TigerWaterConst
    viscosity = 0.001
    [../]
  [../]
[]

[UserObjects]
  [./rock_uo]
    type = TigerPermeabilityVar
    permeability_type = isotropic
    k0 = '1.0e-12'
    n0 = 0.2
  [../]
[]

[Variables]
  [./pressure]
  [../]
  [./temp]
    initial_condition = 373.15
  [../]
[]

[Kernels]
  [./hm]
    type = TigerHydroMechanicsKernelHM
    variable = pressure
    displacements = 'disp_x disp_y disp_z'
  [../]
  [./hm_time]
    type = TigerHydraulicTimeKernelH
    variable = pressure
  [../]
  [./t]
    type = TigerThermalTimeKernelT
    variable = temp
  [../]
  [./t_time]
    type = TigerThermalDiffusionKernelT
    variable = temp
  [../]
  [./poro_x]
    type = PoroMechanicsCoupling
    variable = disp_x
    porepressure = pressure
    component = 0
  [../]
  [./poro_y]
    type = PoroMechanicsCoupling
    variable = disp_y
    porepressure = pressure
    component = 1
  [../]
  [./poro_z]
    type = PoroMechanicsCoupling
    variable = disp_z
    porepressure = pressure
    component = 2
  [../]
[]

[BCs]
  [./no_x]
    type = DirichletBC
    variable = disp_x
    boundary = bottom
    value = 0.0
  [../]
  [./no_y]
    type = DirichletBC
    variable = disp_y
    boundary = bottom
    value = 0.0
  [../]
  [./no_z]
    type = DirichletBC
    variable = disp_z
    boundary = bottom
    value = 0.0
  [../]
  [./pressure]
    type = DirichletBC
    variable = pressure
    boundary = top
    value = 0
  [../]
  [./temp]
    type = FunctionDirichletBC
    variable = temp
    boundary = top
    function = if(x>0.5&z>0.5&t>5000,320,373.15)
  [../]
[]

[Materials]
  [./Elasticity_tensor]
    type = ComputeElasticityTensor
    fill_method = symmetric_isotropic_E_nu
    C_ijkl = '0.5e8 0'
    [../]
  [./stress]
    type = ComputeFiniteStrainElasticStress
  [../]
  [./thermal_expansion]
    type = ComputeThermalExpansionEigenstrain
    thermal_expansion_coeff = 1e-5
    temperature = temp
    stress_free_temperature = 373.15
    eigenstrain_name = 'thermal_eigenstrain'
  [../]
  [./reduced_order_eigenstrain]
    type = ComputeReducedOrderEigenstrain
    input_eigenstrain_names = 'thermal_eigenstrain'
    eigenstrain_name = 'reduced_eigenstrain'
  [../]
  [./rock_g]
    type = TigerGeometryMaterial
    gravity = '0 0 0'
  [../]
  [./rock_p]
    type = TigerPorosityMaterial
    porosity = 0.2
    specific_density = 2500
    porosity_evolotion = true
    output_properties = 'porosity'
    outputs = exodus
  [../]
  [./rock_m]
    type = TigerMechanicsMaterialM
    incremental = true
  [../]
  [./rock_f]
    type = TigerFluidMaterial
    fp_uo = water_uo
  [../]
  [./rock_h]
    type = TigerHydraulicMaterialH
    pressure = pressure
    compressibility = 1.0e-9
    kf_uo = rock_uo
    output_properties = 'permeability_by_viscosity'
    outputs = exodus
  [../]
  [./rock_t]
    type = TigerThermalMaterialT
    specific_heat = 850
    lambda = 2
    conductivity_type = isotropic
    advection_type = pure_diffusion
  [../]
[]

[Preconditioning]
  [./p1]
    type = SMP
    full = true
    petsc_options_iname = '-snes_type -snes_linesearch_type'
    petsc_options_value = 'newtonls basic
    '
  [../]
[]

[Executioner]
  type = Transient
  end_time = 50000
  dt = 5000
  nl_abs_tol = 1e-10
  l_max_its = 20
  automatic_scaling = true
  compute_scaling_once = false
[]

[Outputs]
  exodus = true
  print_linear_residuals = false
[]
