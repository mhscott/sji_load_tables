from dataclasses import dataclass
from sji_load_tables import interp
from sji_load_tables.data import joist_database, joists_sorted_by_weight

# Unit Conversions
in_to_mm = 25.4
in4_to_mm4 = in_to_mm**4
mm_to_in = 1/25.4
mm_to_ft = 1/(25.4*12)
plf_to_kNm = 4.448/304.8
kNm_to_plf = 1/plf_to_kNm

@dataclass
class JoistLoadTableEntry:
    designation: str
    series: str
    depth_in: float
    approx_wt_plf: float
    span_ft: float
    total_load_ASD_plf: float
    deflection_limit_load_plf: float
    erection_bridging_color_code: str
    
    # Properties for rounding results
    round_results = True
    ndigits_depth_in = 0
    ndigits_depth_mm = 0
    ndigits_approx_wt_plf = 1
    ndigits_approx_wt_kNm = 2
    ndigits_span_ft = 0
    ndigits_span_mm = 0
    ndigits_load_plf = 0
    ndigits_load_kNm = 2
    ndigits_approx_moment_of_inertia_in4 = 0
    ndigits_approx_moment_of_inertia_mm4 = 0
    
    def __str__(self):
        if self.span_ft is not None:
            s =   f'{self.designation} joist, span_ft={self.span_ft}, approx_wt_plf={self.approx_wt_plf} \n' 
            s +=  f'  total_load_ASD_plf={self.total_load_ASD_plf}, deflection_limit_load_plf={self.deflection_limit_load_plf} \n'
            s +=  f'  erection_bridging_color_code={self.erection_bridging_color_code}'
        else:
            s = f'{self.designation} joist, approx_wt_plf={self.approx_wt_plf}'
        return s
    
    @property
    def total_load_LRFD_plf(self):
        return 1.5*self.total_load_ASD

    def depth(self,units='in'):
        if units == 'in':
            if self.round_results:
                return round(self.depth_in,self.ndigits_depth_in)
            else:
                return self.depth_in
        elif units == 'mm':
            depth_mm = self.depth_in*in_to_mm
            if self.round_results:
                return round(depth_mm,self.ndigits_depth_mm)
            else:
                return depth_mm
        else:
            raise ValueError(f'Unit conversion for depth from inchs to {units} is not implemented')

    def approx_wt(self,units='plf'):
        if units in ['plf','lbs/ft']:
            if self.round_results:
                return round(self.approx_wt_plf,self.ndigits_approx_wt_plf)
            else:
                return self.approx_wt_plf
        elif units == 'kN/m':
            approx_wt_kNm = self.approx_wt_plf*plf_to_kNm
            if self.round_results:
                return round(approx_wt_kNm,self.ndigits_approx_wt_kNm) 
            else:
                return approx_wt_kNm
        else:
            raise ValueError(f'Unit conversion for approx_wt from plf to {units} is not implemented')

    def span(self,units='ft'):
        if units == 'ft':
            if self.round_results:
                return round(self.span_ft,self.ndigits_span_ft)
            else:
                return self.span_ft
        elif units == 'mm':
            span_mm = self.span_ft*in_to_mm
            if self.round_results:
                return round(span_mm,self.ndigits_span_mm)
            else:
                return span_mm
        else:
            raise ValueError(f'Unit conversion for span from ft to {units} is not implemented')    
    
    def total_load(self,design_basis,units='plf'):
    
        # Convert ASD value to specified design basis
        if design_basis == "ASD":
            total_load_plf = self.total_load_ASD_plf
        elif design_basis == "LRFD":
            total_load_plf = 1.5*self.total_load_ASD_plf
        else:
            raise ValueError(f'Unknown design basis: {design_basis}') 

        # Convert to specified units
        if units in ['plf','lbs/ft']:
            if self.round_results:
                return round(total_load_plf,self.ndigits_load_plf)
            else:
                return total_load_plf
        elif units == 'kN/m':
            total_load_kNm = total_load_plf*plf_to_kNm
            if self.round_results:
                return round(total_load_kNm,self.ndigits_load_kNm)
            else:
                return total_load_kNm
        else:
            raise ValueError(f'Unit conversion for total_load from plf to {units} is not implemented')        
    
    def deflection_limit_load(self,L_over=360,units='plf'):

        # Convert to specified deflection limit
        deflection_limit_load_plf = (360/L_over)*self.deflection_limit_load_plf
        
        # Check against total ASD load
        total_load_ASD_plf = self.total_load('ASD',units='plf')
        if deflection_limit_load_plf > total_load_ASD_plf:
            deflection_limit_load_plf = total_load_ASD_plf

        # Convert to specified units
        if units in ['plf','lbs/ft']:
            if self.round_results:
                return round(deflection_limit_load_plf,self.ndigits_load_plf)
            else:
                return deflection_limit_load_plf
        elif units == 'kN/m':
            deflection_limit_load_kNm = deflection_limit_load_plf*plf_to_kNm
            if self.round_results:
                return round(deflection_limit_load_kNm,self.ndigits_load_kNm)
            else:
                return deflection_limit_load_kNm
        else:
            raise ValueError(f'Unit conversion for deflection_limit_load from plf to {units} is not implemented') 

    def approx_moment_of_inertia(self,shear_deformation_factor=1.15,units='in.4'):
        
        # Compute approximate moment of inertia
        W = self.deflection_limit_load(L_over=360,units='plf')
        L = self.span(units='ft') - 0.33
        Ij_in4 = 26.767e-6*W*L**3
        Ieff_in4 = Ij_in4/shear_deformation_factor
        
        # Convert to specified units
        if units == 'in^4':
            if self.round_results:
                return round(Ieff_in4,self.ndigits_approx_moment_of_inertia_in4)
            else:
                return Ieff_in4
        elif units == 'mm^3':
            Ieff_mm = Ieff_in4*in4_to_mm4
            if self.round_results:
                return round(Ieff_mm,self.ndigits_approx_moment_of_inertia_mm4)
            else:
                return Ieff_mm
        else:
            raise ValueError(f'Unit conversion for approx. moment of inertia from in.4 to {units} is not implemented')


def get_joist_data(designation,span=None,span_units='ft'):
    '''
    returns dictionary of information on joist
    '''
    if designation not in joist_database:
        raise ValueError(f'data not available for a {designation} joist')
        
    joist_dict = joist_database[designation]
    
    if span is None:
        total_load_ASD = None
        deflection_limit_load = None
        erection_bridging_color_code = None
    
    else:
        if span_units == 'ft':
            span_ft = span
        elif span_units == 'mm':
            span_ft = span*mm_to_ft
        else:
            raise ValueError(f'Unit conversion for span from {span_units} to ft is not implemented')
    
        min_span_ft = joist_dict['span_ft_list'][0]
        if span_ft < min_span_ft:
            raise ValueError(f'Requested span ({span_ft} ft) is less than minimum span of {min_span_ft} ft for a {designation} joist')
        
        max_span_ft = joist_dict['span_ft_list'][-1]
        if span_ft > max_span_ft:
            raise ValueError(f'Requested span ({span_ft} ft) exceeds maximum span of {max_span_ft} ft for a {designation} joist')
    
        # Linear interpolate load data for total and deflection load
        total_load_ASD_plf = interp(span_ft,joist_dict['span_ft_list'],joist_dict['total_load_ASD_plf_list'])
        deflection_limit_load_plf = interp(span_ft,joist_dict['span_ft_list'],joist_dict['deflection_limit_load_plf_list'])

        # Erection Bridging Color Code
        if joist_dict['series'] == 'K':
            if joist_dict['limiting_span_for_erection_bridging_ft'] == 'na':
                erection_bridging_color_code = None
            elif span_ft < joist_dict['limiting_span_for_erection_bridging_ft']:
                erection_bridging_color_code = None
            else: 
                erection_bridging_color_code = 'Red'            
        else:
            if span_ft < 60:
                if joist_dict['limiting_span_for_erection_bridging_ft'] == 'na':
                    erection_bridging_color_code = None
                elif span_ft < joist_dict['limiting_span_for_erection_bridging_ft']:
                    erection_bridging_color_code = None
                else: 
                    erection_bridging_color_code = 'Red'
            elif span_ft < 100:
                erection_bridging_color_code = 'Blue'
            else: 
                erection_bridging_color_code = 'Gray'  
    
    # Create JoistLoadTableEntry object
    joist = JoistLoadTableEntry(
        designation=designation,
        series=joist_dict['series'],
        depth_in=joist_dict['depth_in'],
        approx_wt_plf=joist_dict['approx_wt_plf'],
        span_ft=span_ft,
        total_load_ASD_plf=total_load_ASD_plf,
        deflection_limit_load_plf=deflection_limit_load_plf,
        erection_bridging_color_code=erection_bridging_color_code,
        )
    
    return joist


def lightest_joist(span,required_total_load=None,required_deflection_limit_load=None,
                   min_depth=None,max_depth=None,series=None,minimize_erection_bridging=False,
                   design_basis='ASD',L_over=360,
                   span_units='ft',depth_units='in',load_units='plf'):
    '''
    Returns a JoistLoadTableEntry object of the lightest joist meeting all the specified criteria.
    If no joist satifying all the criteria can be found, then None is returned.
    '''

    # Convert units
    if span_units == 'ft':
        span_ft = span
    elif span_units == 'mm':
        span_ft = span*mm_to_ft
    else:
        raise ValueError(f'Unit conversion for span from {span_units} to ft is not implemented')    

    if required_total_load is not None:
        if load_units in ['plf','lb/ft']:
            required_total_load_plf = required_total_load
        elif load_units == 'kNm':
            required_total_load_plf = required_total_load*kNm_to_plf
        else:
            raise ValueError(f'Unit conversion for load from {load_units} to plf is not implemented')    

    if required_deflection_limit_load is not None:
        if load_units in ['plf','lb/ft']:
            required_deflection_limit_load_plf = required_deflection_limit_load
        elif load_units == 'kNm':
            required_deflection_limit_load_plf = required_deflection_limit_load*kNm_to_plf
        else:
            raise ValueError(f'Unit conversion for load from {load_units} to plf is not implemented')    

    if min_depth is not None:
        if depth_units == 'in':
            min_depth_in = min_depth
        elif span_units == 'mm':
            min_depth_in = min_depth*mm_to_in
        else:
            raise ValueError(f'Unit conversion for min_depth from {depth_units} to in. is not implemented')   
    
    if max_depth is not None:
        if depth_units == 'in':
            max_depth_in = max_depth
        elif span_units == 'mm':
            max_depth_in = max_depth*mm_to_in
        else:
            raise ValueError(f'Unit conversion for max_depth from {depth_units} to in. is not implemented')   
              
            
    # Loop over joists from lightest to heaviest 
    for designation in joists_sorted_by_weight:
        joist_dict = joist_database[designation]
        
        if series is not None:
            if joist_dict['series'] not in series:
                continue
        
        if min_depth is not None:
            if joist_dict['depth_in'] < min_depth_in:
                continue
        
        if max_depth is not None:
            if joist_dict['depth_in'] > max_depth_in:
                continue
        
        if span_ft < joist_dict['span_ft_list'][0]:
            continue
            
        if span_ft > joist_dict['span_ft_list'][-1]:
            continue
        
        joist = get_joist_data(designation,span_ft)
        
        # Check required total load
        if required_total_load is not None:
            if required_total_load_plf > joist.total_load(design_basis,units='plf'):
                continue
        
        # Check required deflection limit load
        if required_deflection_limit_load is not None:
            if required_deflection_limit_load_plf > joist.deflection_limit_load(L_over=L_over,units='plf'):
                continue

        # Check erection bridging
        if joist.erection_bridging_color_code == 'Red':
            continue
            
        return joist
    
    return None
