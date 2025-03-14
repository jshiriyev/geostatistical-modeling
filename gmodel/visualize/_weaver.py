from matplotlib import pyplot as plt

from matplotlib import colors as mcolors

from matplotlib.patches import PathPatch, Polygon
from matplotlib.path import Path

import numpy

from _templix import PropDict
    
class Weaver():

    @staticmethod
    def fill_solid(axis:plt.Axes,x:numpy.ndarray,y1:numpy.ndarray,y2:numpy.ndarray,prop:PropDict):

        # Fill between the curves
        fill = axis.fill_between(x,y1,y2,facecolor=prop.facecolor,hatch=prop.hatch)

        for motif in prop.motifs:
            # Create the pattern patches
            patches = Weaver.patches(
                x.min(),x.max(),y1.min(),y2.max(),motif
                )

            # Clip the pattern patches
            for patch in patches:
                patch.set_clip_path(
                    fill.get_paths()[0],transform=axis.transData
                    )  # Clip each patch to the filled region

                axis.add_patch(patch)

        return axis

    @staticmethod
    def fill_gradient(axis:plt.Axes,x:numpy.ndarray,y:numpy.ndarray,xmin=None,xmax=None,left=False,fill_color=None,alpha=None,**kwargs):
        """Plot a line with a linear alpha gradient filled beneath it."""
        line, = axis.plot(x,y,**kwargs)

        if fill_color is None:
            fill_color = line.get_color()

        rgb = mcolors.colorConverter.to_rgb(fill_color)
        rgb = numpy.array([rgb]).repeat(y.size,axis=0)

        z = rgb[:,:,numpy.newaxis].transpose((0,2,1))

        xmin = numpy.nanmin(x) if xmin is None else xmin
        xmax = numpy.nanmax(x) if xmax is None else xmax

        ymin,ymax = numpy.nanmin(y),numpy.nanmax(y)

        z[:,0,1] = (xmax-x)/(xmax-xmin)

        im = axis.imshow(z,
            aspect = 'auto',
            extent = [xmin,xmax,ymin,ymax],
            origin = 'lower',
            zorder = line.get_zorder()
            )

        xy = numpy.column_stack([x,y])

        if left:
            xy = numpy.vstack([[xmin,ymin],xy,[xmin,ymax],[xmin,ymin]])
        else:
            xy = numpy.vstack([[xmax,ymin],xy,[xmax,ymax],[xmax,ymin]])

        xy = xy[~numpy.isnan(xy).any(axis=1)]

        clip = Polygon(xy,facecolor='none',edgecolor='none',closed=True)

        axis.add_patch(clip)

        im.set_clip_path(clip)

        return axis

    @staticmethod
    def patches(x_min,x_max,y_min,y_max,motif):
        """Creates individual patches within a bounded region. Returns list of PathPatch objects."""
        offsety = (motif.height_extern-motif.height)/2.

        y_nodes = numpy.arange(y_min+offsety,y_max,motif.height_extern)

        offset1 = motif.length*(motif.length_ratio-1)/2.
        offset2 = motif.length*motif.offset_ratio

        x_lower = numpy.arange(x_min+offset1,x_max,motif.length_extern)
        x_upper = numpy.arange(x_min-offset2,x_max,motif.length_extern)

        patches = []
        
        for y_index,y_node in enumerate(y_nodes):

            x_nodes = x_lower if y_index%2==0 else x_upper
            
            for x_node in x_nodes:

                path = Weaver.path(x_node,y_node,motif)
                
                patches.append(PathPatch(path,**motif.params))
        
        return patches

    def path(x_node,y_node,motif):
        """Returns path for the instance figure."""
        element = getattr(Weaver,motif.element)

        x_func,y_func = element(length=motif.length,height=motif.height,tilted_ratio=motif.tilted_ratio)

        if motif.element == "circle":
            return Path.circle((x_func(x_node),y_func(y_node)),radius=motif.radius)
        
        return Path([(x,y) for x,y in zip(x_func(x_node),y_func(y_node))])

    @staticmethod
    def circle(length=0.2,height=0.2,**kwargs):
        """Returns functions that calculates center coordinates for the given lower left corner."""
        x_func = lambda x: x+numpy.sqrt(length*height)/2
        y_func = lambda y: y+numpy.sqrt(length*height)/2

        return x_func,y_func

    @staticmethod
    def line(length=0.2,height=0.1,**kwargs):
        """Returns functions that calculates line vertex coordinates for the given lower left corner."""
        x_func = lambda x: [x, x+length]
        y_func = lambda y: [y, y+height]

        return x_func,y_func

    @staticmethod
    def triangle(length=0.2,height=0.1,tilted_ratio=0.):
        """Returns functions that calculates triangle vertex coordinates for the given lower left corner."""
        x_func = lambda x: [x, x+length, x+length/2+length*tilted_ratio, x]
        y_func = lambda y: [y, y, y+height, y]

        return x_func,y_func

    @staticmethod
    def quadrupe(length=0.8,height=0.4,tilted_ratio=0.):
        """Returns functions that calculates quadrilateral node coordinates for the given lower left corner."""
        x_func = lambda x: [x, x+length, x+length+length*tilted_ratio, x+length*tilted_ratio, x]
        y_func = lambda y: [y, y, y+height, y+height, y]

        return x_func,y_func

if __name__ == "__main__":

    import numpy as np

    from _templix import PropDict
    from _motifs import MotifPattern

    x = np.linspace(0, 10, 100)

    y1 = np.sin(x) * 2 + 6
    y2 = np.sin(x) * 2 + 8 # Upper curve

    fig,ax = plt.subplots(figsize=(8,5))

    motif = MotifPattern(**dict(
            element="triangle",length=0.4,height=0.3,offset_ratio=0.5,tilted_ratio=0.,length_ratio=4.,height_ratio=2,
            params = dict(edgecolor='black',fill=None)
            ))

    prop = PropDict(**{"facecolor":"tan","hatch":None,"motifs":(motif,)})

    # alpha=0.5,edgecolor='black',lw=1.2,
    ax = Weaver.fill_between(ax,x,y1,y2,prop=prop)

    # Adjust limits and labels
    # ax.set_xlim(x.min(),x.max())
    ax.set_ylim(y1.min(),y2.max()+0.2)  # Extra space for visibility
    ax.set_xlabel("X-axis")
    ax.set_ylabel("Y-axis")

    plt.show()