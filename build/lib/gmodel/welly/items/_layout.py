from dataclasses import dataclass

@dataclass
class Layout:
    """It is a diagram dictionary for a well

    indiameter  : Inner Diameter
    csa         : Cross Sectional Are
    H_diameter  : Hydraulic Diameter; 4*Hydraulic_Radius
    H_radius    : Hydraulic Radius; the ratio of the cross-sectional area of
                  a channel or pipe in which a fluid is flowing to the 
                  wetted perimeter of the conduit.

    Nodes are the locations where the measurements are available, and
    coordinates are selected in such a way that:
    - r-axis shows radial direction
    - theta-axis shows angular direction 
    - z-axis shows lengthwise direction
    
    """