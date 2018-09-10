from __future__ import unicode_literals

import math
#import sys
import matplotlib.pyplot as plt
import ephem
import matplotlib.patches as patches

import matplotlib
from matplotlib.axes import Axes   
from matplotlib.patches import Circle
from matplotlib.path import Path
from matplotlib.ticker import NullLocator, Formatter, FixedLocator
from matplotlib.transforms import Affine2D, BboxTransformTo, Transform
from matplotlib.projections import register_projection
import matplotlib.spines as mspines
import matplotlib.axis as maxis
import numpy as np
from matplotlib.mlab import griddata

# This example projection class is rather long, but it is designed to
# illustrate many features, not all of which will be used every time.
# It is also common to factor out a lot of these methods into common
# code used by a number of projections with similar characteristics
# (see geo.py).




class HammerAxes(Axes):
    """
    A custom class for the Aitoff-Hammer projection, an equal-area map
    projection.

    http://en.wikipedia.org/wiki/Hammer_projection
    """
    # The projection must specify a name.  This will be used be the
    # user to select the projection, i.e. ``subplot(111,
    # projection='custom_hammer')``.
    name = 'custom_hammer'

    def __init__(self, *args, **kwargs):
        Axes.__init__(self, *args, **kwargs)
        self.set_aspect(0.5, adjustable='box', anchor='C')
        self.cla()

    def _init_axis(self):
        self.xaxis = maxis.XAxis(self)
        self.yaxis = maxis.YAxis(self)
        # Do not register xaxis or yaxis with spines -- as done in
        # Axes._init_axis() -- until HammerAxes.xaxis.cla() works.
        # self.spines['hammer'].register_axis(self.yaxis)
        self._update_transScale()

    def cla(self):
        """
        Override to set up some reasonable defaults.
        """
        # Don't forget to call the base class
        Axes.cla(self)

        # Set up a default grid spacing
        self.set_longitude_grid(60)
        self.set_latitude_grid(30)
        self.set_longitude_grid_ends(90)

        # Turn off minor ticking altogether
        self.xaxis.set_minor_locator(NullLocator())
        self.yaxis.set_minor_locator(NullLocator())

        # Do not display ticks -- we only want gridlines and text
        self.xaxis.set_ticks_position('none')
        self.yaxis.set_ticks_position('none')
        for tx in self.xaxis.get_major_ticks():
            tx.label.set_fontsize(15)
        for ty in self.yaxis.get_major_ticks():
            ty.label.set_fontsize(15)

        # The limits on this projection are fixed -- they are not to
        # be changed by the user.  This makes the math in the
        # transformation itself easier, and since this is a toy
        # example, the easier, the better.
        Axes.set_xlim(self, -np.pi, np.pi)
        Axes.set_ylim(self, -np.pi / 2.0, np.pi / 2.0)

    def _set_lim_and_transforms(self):
        """
        This is called once when the plot is created to set up all the
        transforms for the data, text and grids.
        """
        # There are three important coordinate spaces going on here:
        #
        #    1. Data space: The space of the data itself
        #
        #    2. Axes space: The unit rectangle (0, 0) to (1, 1)
        #       covering the entire plot area.
        #
        #    3. Display space: The coordinates of the resulting image,
        #       often in pixels or dpi/inch.

        # This function makes heavy use of the Transform classes in
        # ``lib/matplotlib/transforms.py.`` For more information, see
        # the inline documentation there.

        # The goal of the first two transformations is to get from the
        # data space (in this case longitude and latitude) to axes
        # space.  It is separated into a non-affine and affine part so
        # that the non-affine part does not have to be recomputed when
        # a simple affine change to the figure has been made (such as
        # resizing the window or changing the dpi).

        # 1) The core transformation from data space into
        # rectilinear space defined in the HammerTransform class.
        self.transProjection = self.HammerTransform()

        # 2) The above has an output range that is not in the unit
        # rectangle, so scale and translate it so it fits correctly
        # within the axes.  The peculiar calculations of xscale and
        # yscale are specific to a Aitoff-Hammer projection, so don't
        # worry about them too much.
        xscale = 2.0 * np.sqrt(2.0) * np.sin(0.5 * np.pi)
        yscale = np.sqrt(2.0) * np.sin(0.5 * np.pi)
        self.transAffine = Affine2D() \
            .scale(0.5 / xscale, 0.5 / yscale) \
            .translate(0.5, 0.5)

        # 3) This is the transformation from axes space to display
        # space.
        self.transAxes = BboxTransformTo(self.bbox)

        # Now put these 3 transforms together -- from data all the way
        # to display coordinates.  Using the '+' operator, these
        # transforms will be applied "in order".  The transforms are
        # automatically simplified, if possible, by the underlying
        # transformation framework.
        self.transData = \
            self.transProjection + \
            self.transAffine + \
            self.transAxes

        # The main data transformation is set up.  Now deal with
        # gridlines and tick labels.

        # Longitude gridlines and ticklabels.  The input to these
        # transforms are in display space in x and axes space in y.
        # Therefore, the input values will be in range (-xmin, 0),
        # (xmax, 1).  The goal of these transforms is to go from that
        # space to display space.  The tick labels will be offset 4
        # pixels from the equator.
        self._xaxis_pretransform = \
            Affine2D() \
            .scale(1.0, np.pi) \
            .translate(0.0, -np.pi)
        self._xaxis_transform = \
            self._xaxis_pretransform + \
            self.transData
        self._xaxis_text1_transform = \
            Affine2D().scale(0.80, 0.0) + \
            self.transData + \
            Affine2D().translate(0.0, 50.0)
        self._xaxis_text2_transform = \
            Affine2D().scale(0.85, 0.0) + \
            self.transData + \
            Affine2D().translate(0.0, -50.0)

        # Now set up the transforms for the latitude ticks.  The input to
        # these transforms are in axes space in x and display space in
        # y.  Therefore, the input values will be in range (0, -ymin),
        # (1, ymax).  The goal of these transforms is to go from that
        # space to display space.  The tick labels will be offset 4
        # pixels from the edge of the axes ellipse.
        yaxis_stretch = Affine2D().scale(np.pi * 2.0, 1.0).translate(-np.pi*1.0, 0.0)
        yaxis_space = Affine2D().scale(-1.0, 1.1)     # modify1
        self._yaxis_transform = \
            yaxis_stretch + \
            self.transData
        yaxis_text_base = \
            yaxis_stretch + \
            self.transProjection + \
            (yaxis_space + \
             self.transAffine + \
             self.transAxes)
        self._yaxis_text1_transform = \
            yaxis_text_base + \
            Affine2D().translate(-8.0, 0.0)
        self._yaxis_text2_transform = \
            yaxis_text_base + \
            Affine2D().translate(8.0, 0.0)

    def get_xaxis_transform(self,which='grid'):
        """
        Override this method to provide a transformation for the
        x-axis grid and ticks.
        """
        assert which in ['tick1','tick2','grid']
        return self._xaxis_transform

    def get_xaxis_text1_transform(self, pixelPad):
        """
        Override this method to provide a transformation for the
        x-axis tick labels.

        Returns a tuple of the form (transform, valign, halign)
        """
        return self._xaxis_text1_transform, 'bottom', 'center'

    def get_xaxis_text2_transform(self, pixelPad):
        """
        Override this method to provide a transformation for the
        secondary x-axis tick labels.

        Returns a tuple of the form (transform, valign, halign)
        """
        return self._xaxis_text2_transform, 'top', 'center'

    def get_yaxis_transform(self,which='grid'):
        """
        Override this method to provide a transformation for the
        y-axis grid and ticks.
        """
        assert which in ['tick1','tick2','grid']
        return self._yaxis_transform

    def get_yaxis_text1_transform(self, pixelPad):
        """
        Override this method to provide a transformation for the
        y-axis tick labels.

        Returns a tuple of the form (transform, valign, halign)
        """
        return self._yaxis_text1_transform, 'center', 'right'

    def get_yaxis_text2_transform(self, pixelPad):
        """
        Override this method to provide a transformation for the
        secondary y-axis tick labels.

        Returns a tuple of the form (transform, valign, halign)
        """
        return self._yaxis_text2_transform, 'center', 'left'

    def _gen_axes_patch(self):
        """
        Override this method to define the shape that is used for the
        background of the plot.  It should be a subclass of Patch.

        In this case, it is a Circle (that may be warped by the axes
        transform into an ellipse).  Any data and gridlines will be
        clipped to this shape.
        """
        return Circle((0.5, 0.5), 0.5)

    def _gen_axes_spines(self):
        return {'custom_hammer':mspines.Spine.circular_spine(self,
                                                      (0.5, 0.5), 0.5)}

    # Prevent the user from applying scales to one or both of the
    # axes.  In this particular case, scaling the axes wouldn't make
    # sense, so we don't allow it.
    def set_xscale(self, *args, **kwargs):
        if args[0] != 'linear':
            raise NotImplementedError
        Axes.set_xscale(self, *args, **kwargs)

    def set_yscale(self, *args, **kwargs):
        if args[0] != 'linear':
            raise NotImplementedError
        Axes.set_yscale(self, *args, **kwargs)

    # Prevent the user from changing the axes limits.  In our case, we
    # want to display the whole sphere all the time, so we override
    # set_xlim and set_ylim to ignore any input.  This also applies to
    # interactive panning and zooming in the GUI interfaces.
    def set_xlim(self, *args, **kwargs):
        Axes.set_xlim(self, -np.pi, np.pi)
        Axes.set_ylim(self, -np.pi / 2.0, np.pi / 2.0)
    set_ylim = set_xlim

    def format_coord(self, lon, lat):
        """
        Override this method to change how the values are displayed in
        the status bar.

        In this case, we want them to be displayed in degrees N/S/E/W.
        """
        lon = lon * (180.0 / np.pi)
        lat = lat * (180.0 / np.pi)
        if lat >= 0.0:
            ns = 'N'
        else:
            ns = 'S'
        if lon <= 0.0:
            ew = 'E'
        else:
            ew = 'W'
        # \u00b0 : degree symbol
        return '%f\u00b0%s, %f\u00b0%s' % (abs(lat), ns, abs(lon), ew)

    class xDegreeFormatter(Formatter):
        """
        This is a custom formatter that converts the native unit of
        radians into (truncated) degrees and adds a degree symbol.
        """
        def __init__(self, round_to=1.0):
            self._round_to = round_to

        def __call__(self, x, pos=None):
            degrees = (x / np.pi) * 180.0
            degrees = round(degrees / self._round_to) * self._round_to
            if (degrees<0):
                degrees += 360
            # \u00b0 : degree symbol
            #return "%d\u00b0" % degrees
            degrees = degrees*1.0/360*24
            return "$\mathrm{%d ^h}$" % degrees 

    class yDegreeFormatter(Formatter):
        """
        This is a custom formatter that converts the native unit of
        radians into (truncated) degrees and adds a degree symbol.
        """
        def __init__(self, round_to=1.0):
            self._round_to = round_to

        def __call__(self, x, pos=None):
            degrees = (x / np.pi) * 180.0
            degrees = round(degrees / self._round_to) * self._round_to
            # \u00b0 : degree symbol
            return "%d\u00b0" % degrees

    def set_longitude_grid(self, degrees):
        """
        Set the number of degrees between each longitude grid.

        This is an example method that is specific to this projection
        class -- it provides a more convenient interface to set the
        ticking than set_xticks would.
        """
        # Set up a FixedLocator at each of the points, evenly spaced
        # by degrees.
        number = (360.0 / degrees) + 1
        self.xaxis.set_major_locator(
            plt.FixedLocator(
                np.linspace(-np.pi, np.pi, number, True)[1:-1]))
        # Set the formatter to display the tick labels in degrees,
        # rather than radians.
        self.xaxis.set_major_formatter(self.xDegreeFormatter(degrees))

    def set_latitude_grid(self, degrees):
        """
        Set the number of degrees between each longitude grid.

        This is an example method that is specific to this projection
        class -- it provides a more convenient interface than
        set_yticks would.
        """
        # Set up a FixedLocator at each of the points, evenly spaced
        # by degrees.
        number = (180.0 / degrees) + 1
        self.yaxis.set_major_locator(
            FixedLocator(
                np.linspace(-np.pi / 2.0, np.pi / 2.0, number, True)[1:-1]))
        # Set the formatter to display the tick labels in degrees,
        # rather than radians.
        self.yaxis.set_major_formatter(self.yDegreeFormatter(degrees))

    def set_longitude_grid_ends(self, degrees):
        """
        Set the latitude(s) at which to stop drawing the longitude grids.

        Often, in geographic projections, you wouldn't want to draw
        longitude gridlines near the poles.  This allows the user to
        specify the degree at which to stop drawing longitude grids.

        This is an example method that is specific to this projection
        class -- it provides an interface to something that has no
        analogy in the base Axes class.
        """
        longitude_cap = degrees * (np.pi / 180.0)
        # Change the xaxis gridlines transform so that it draws from
        # -degrees to degrees, rather than -pi to pi.
        self._xaxis_pretransform \
            .clear() \
            .scale(1.0, longitude_cap * 2.0) \
            .translate(0.0, -longitude_cap)

    def get_data_ratio(self):
        """
        Return the aspect ratio of the data itself.

        This method should be overridden by any Axes that have a
        fixed data ratio.
        """
        return 1.0

    # Interactive panning and zooming is not supported with this projection,
    # so we override all of the following methods to disable it.
    def can_zoom(self):
        """
        Return True if this axes support the zoom box
        """
        return False
    def start_pan(self, x, y, button):
        pass
    def end_pan(self):
        pass
    def drag_pan(self, button, key, x, y):
        pass

    # Now, the transforms themselves.

    class HammerTransform(Transform):
        """
        The base Hammer transform.
        """
        input_dims = 2
        output_dims = 2
        is_separable = False

        def transform_non_affine(self, ll):
            """
            Override the transform_non_affine method to implement the custom
            transform.
            The input and output are Nx2 numpy arrays.
            """
            longitude = ll[:, 0:1]
            latitude  = ll[:, 1:2]

            # Pre-compute some values
            half_long = longitude / 2.0
            cos_latitude = np.cos(latitude)
            sqrt2 = np.sqrt(2.0)

            alpha = 1.0 + cos_latitude * np.cos(half_long)
            x = - (2.0 * sqrt2) * (cos_latitude * np.sin(half_long)) / alpha   # modify2
            y = (sqrt2 * np.sin(latitude)) / alpha
            return np.concatenate((x, y), 1)

        # This is where things get interesting.  With this projection,
        # straight lines in data space become curves in display space.
        # This is done by interpolating new values between the input
        # values of the data.  Since ``transform`` must not return a
        # differently-sized array, any transform that requires
        # changing the length of the data array must happen within
        # ``transform_path``.
        def transform_path_non_affine(self, path):
            ipath = path.interpolated(path._interpolation_steps)
            return Path(self.transform(ipath.vertices), ipath.codes)
        transform_path_non_affine.__doc__ = \
                Transform.transform_path_non_affine.__doc__

        if matplotlib.__version__ < '1.2':
            # Note: For compatibility with matplotlib v1.1 and older, you'll
            # need to explicitly implement a ``transform`` method as well.
            # Otherwise a ``NotImplementedError`` will be raised. This isn't
            # necessary for v1.2 and newer, however.
            transform = transform_non_affine

            # Similarly, we need to explicitly override ``transform_path`` if
            # compatibility with older matplotlib versions is needed. With v1.2
            # and newer, only overriding the ``transform_path_non_affine``
            # method is sufficient.
            transform_path = transform_path_non_affine
            transform_path.__doc__ = Transform.transform_path.__doc__

        def inverted(self):
            return HammerAxes.InvertedHammerTransform()
        inverted.__doc__ = Transform.inverted.__doc__

    class InvertedHammerTransform(Transform):
        input_dims = 2
        output_dims = 2
        is_separable = False

        def transform_non_affine(self, xy):
            x = xy[:, 0:1]
            y = xy[:, 1:2]

            quarter_x = 0.25 * x
            half_y = 0.5 * y
            z = np.sqrt(1.0 - quarter_x*quarter_x - half_y*half_y)
            longitude = 2 * np.arctan((z*x) / (2.0 * (2.0*z*z - 1.0)))
            latitude = np.arcsin(y*z)
            return np.concatenate((longitude, latitude), 1)
        transform_non_affine.__doc__ = Transform.transform_non_affine.__doc__

        # As before, we need to implement the "transform" method for
        # compatibility with matplotlib v1.1 and older.
        if matplotlib.__version__ < '1.2':
            transform = transform_non_affine

        def inverted(self):
            # The inverse of the inverse is the original transform... ;)
            return HammerAxes.HammerTransform()
        inverted.__doc__ = Transform.inverted.__doc__

# Now register the projection with matplotlib so the user can select
# it.
register_projection(HammerAxes)









#=========The part below can be modified freely================

# Define transformRDJ function     
def transformRDJ(hms):
    if len(hms) == 3:
       (h, m, s) = hms
    elif len(hms) == 2:
       (h, m) = hms
       s = 0
    elif len(hms) == 1:
       h = hms[0]
       m = 0
       s = 0
    else:
       (h, m, s) = [0] * 3
    if h > 0:
       return math.copysign((h+m/60.+s/3600.), h)
    else:
       return math.copysign((h-m/60.-s/3600.), h)

# Class switch function
class switch(object):
    def __init__(self, value):     
        self.value = value
        self.fall = False         
 
    def __iter__(self):
        yield self.match            
        raise StopIteration         
 
    def match(self, *args):        
        if self.fall or not args:   
                                    
            return True
        elif self.value in args:    
            self.fall = True
            return True
        else:                       
            return False

# EC transform GC
def ec2gc(RA,Dec):
    erdot = ephem.Equatorial(RA,Dec,epoch=2000)
    gdot = ephem.Galactic(erdot)
    return gdot.lon,gdot.lat




files0 = open('GCs-FASTsky_40.txt','r')
#files1 = open('IPTApsr_all.txt','r')
#files2 = open('Allmsp.txt','r')
#files3 = open('Allpsr.txt','r')

#files3 = open('/Users/leizhang/work/psr_review/PSRCAT/3surveysn.db','r')


files = [files0]
#files = [files0, files1, files2]
#files = [files0, files1, files2, files3]
numfile = 0
i = 0

plot_x0=[]
plot_y0=[]
plot_x1=[]
plot_y1=[]
plot_x2=[]
plot_y2=[]
plot_x3=[]
plot_y3=[]
lines = []
RA = []
Dec = []

plot_x01=[]
plot_y01=[]
colors01 = []
size01 = []
plot_x021=[]
plot_y021=[]
colors021 = []
size021 = []
plot_x022=[]
plot_y022=[]
colors022 = []
size022 = []







while numfile < len(files):

    for each_line in files[numfile]:    
        lines.append(each_line.split())
    
   


    
    
    while i < len(lines):
        GC_RA = ((transformRDJ(map(float,lines[i][2].split(':')))) * 15)*np.pi/180.0      
        GC_Dec =( transformRDJ(map(float,lines[i][3].split(':'))))*np.pi/180.0
        #Nknown = float(lines[i][4])
        Npsr = np.log10(float(lines[i][5])+0.001)*35
        #Nexp = float(lines[i][6])
        Ndrift = float(lines[i][7])


        if float(GC_RA) > 3.1415926:
           Change_RA = float(GC_RA) - 6.2831852
        else:
           Change_RA = float(GC_RA)
    
        RA.append(float(Change_RA))    
        Dec.append(float(GC_Dec)) 
        
        
    
        

    
        for case in switch(numfile):
            if case(0):
                if Npsr == 0.0:                    
                   plot_x01.append(RA[i])
                   plot_y01.append(Dec[i])
                   size01.append(Npsr)
                   colors01.append(Ndrift)
                else:
                    if Ndrift > 100.0:                       
                       plot_x021.append(RA[i])
                       plot_y021.append(Dec[i])
                       size021.append(Npsr)
                       colors021.append(Ndrift)
                    else:
                       plot_x022.append(RA[i])
                       plot_y022.append(Dec[i])
                       size022.append(Npsr)
                       colors022.append(Ndrift)
            break 
            if case(1):
               plot_x1.append(RA[i])
               plot_y1.append(Dec[i])
            break 
            if case(2):
               plot_x2.append(RA[i])
               plot_y2.append(Dec[i])
            break 
            if case(3):
               plot_x3.append(RA[i])
               plot_y3.append(Dec[i])
                          

               
        i = i+1
    #print "Npsr:", i 
    
    numfile = numfile + 1

#print  "size01:", size01
#print  "size02:", size02







if __name__ == '__main__':
#    # Now make a simple example using the custom projection.
#    fig = plt.figure()    
#    ax = fig.add_subplot(111,projection="custom_hammer")
#
#    plot_x0=np.array(plot_x0);plot_y0=np.array(plot_y0);colors=np.array(colors);
#    ngridx=2000;ngridy=2000;
#    xi = np.linspace(plot_x0.min(), plot_x0.max(), ngridx)
#    yi = np.linspace(plot_y0.min(), plot_y0.max(), ngridy)
#    zi = griddata(plot_x0, plot_y0, colors, xi, yi, interp='linear')
#    b3=ax.contourf(xi, yi, zi, 30, cmap=plt.cm.nipy_spectral,
#             norm=plt.Normalize(vmin=zi.min()-1,vmax=zi.max()+1))
#    plt.colorbar(b3)
    







    plt.subplot(111, projection="custom_hammer")
   # plt.plot(plot_x01,plot_y01, marker = 'o', color = 'r',markersize=6, alpha = 1,ls='None',mec='r',mew=1,fillstyle='none')
    #plt.plot(plot_x021,plot_y021, marker = 'o', color = 'r',markersize=6, alpha = 1,ls='None',mec='b',mew=1,fillstyle='none')
    #b2=plt.scatter( plot_x022,plot_y022, c=colors022,s=size022,cmap=plt.cm.nipy_spectral,alpha=1,edgecolor="w")
    idx=1.2;    
    size022b= (size022/np.max(size022))**idx*150    
    b2=plt.scatter( plot_x022,plot_y022, c=np.log10(colors022/np.max(colors022)),s=size022b,cmap='gist_ncar',alpha=1,edgecolor="w")
    b2.set_array(np.log10(colors022/np.max(colors022)))
    plt.colorbar(b2)
    
#    b2=plt.scatter( plot_x022,plot_y022, c=colors022,s=size022b,cmap='gist_ncar',alpha=1,edgecolor="w")
#    b2.set_array(np.array(colors022))
#    plt.colorbar(b2)

    #plt.axis([0,np.pi])
    #plt.ayis([0,np.pi])

    #plt.plot(-1.772270,0.136026, marker = '+', label = 'J1713+0747', color = 'k', markersize=10,alpha = 1,fillstyle='full',ls='None')
     
    
    
    
     #ax.grid(True)
     #ax.legend(bbox_to_anchor=(0.55,1.28,),loc = 2, borderaxespad=0., prop={'size':10}) 
    plt.grid(True)
    #plt.legend(loc='upper right', prop={'size':9})
 #   plt.savefig('3sur_background.png')
#    plt.savefig('3sur_background.pdf')
#    plt.savefig('3sur_background.eps')    #  How to save as .eps  ???
    
    plt.show()
    







    

    
