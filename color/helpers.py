

class Color(object):
    '''
    Attributes:
    r, g, b (0-1)
    hue, saturation, lightness (0-1)

    This stores color values as a list of 4 floats (RGBA) in a 0-1 range.

    The value can come in the following flavours:
    - v
    - (v)
    - (v,a)
    - (r,g,b)
    - (r,g,b,a)
    - #RRGGBB
    - RRGGBB
    - #RRGGBBAA
    - RRGGBBAA
    
    The CMYK parts have been commented out, as it may slow down code execution
    and at this point is quite useless, left it in place for a possible future implementation
    '''

    def __init__(self, *args, **kwargs):
        parameters = len(args)

        # Values are supplied as a tuple.
        if parameters == 1 and isinstance(args[0], tuple):
            a = args[0]
            
        # No values or None, transparent black.
        if parameters == 0 or (parameters == 1 and args[0] == None):
            raise Exception("got Color() with value None!")
            self.r, self.g, self.b, self.a = 0, 0, 0, 0
            
        # One value, another color object.
        elif parameters == 1 and isinstance(args[0], Color):
            self.r, self.g, self.b, self.a = args[0].r, args[0].g, args[0].b, args[0].a
            
        # One value, a hexadecimal string.
        elif parameters == 1 and isinstance(args[0], str):
            r, g, b, a = util.hex2rgb(args[0])
            self.r, self.g, self.b, self.a = r, g, b, a
            
        # One value, grayscale.
        elif parameters == 1:
            if kwargs.has_key("color_range"):
                ra = int(kwargs["color_range"])
            else:
                ra = 1
            
            self.r, self.g, self.b, self.a = args[0]/ra, args[0]/ra, args[0]/ra, 1
            
        # Two values, grayscale and alpha.
        elif parameters == 2:
            if kwargs.has_key("color_range"):
                ra = int(kwargs["color_range"])
            else:
                ra = 1

            self.r, self.g, self.b, self.a = args[0]/ra, args[0]/ra, args[0]/ra, args[1]/ra
            
        # Three to five parameters, either RGB, RGBA, HSB, HSBA, CMYK, CMYKA
        # depending on the mode parameter.
        elif parameters >= 3:
            if kwargs.has_key("color_range"):
                ra = int(kwargs["color_range"])
            else:
                ra = 1            

            alpha, mode = 1, "rgb" 
            if parameters > 3: 
                alpha = args[-1]/ra
        
            if kwargs.has_key("mode"): 
                mode = kwargs["mode"].lower()
            if mode == "rgb":                
                self.r, self.g, self.b, self.a = args[0]/ra, args[1]/ra, args[2]/ra, alpha               
            elif mode == "hsb":                
                self.h, self.s, self.brightness, self.a = args[0]/ra, args[1]/ra, args[2]/ra, alpha


        self.red   = self.r
        self.green = self.g
        self.blue  = self.b
        self.alpha = self.a

        self.data = [self.r, self.g, self.b, self.a]


    def __repr__(self):
        return "%s(%.3f, %.3f, %.3f, %.3f)" % (self.__class__.__name__, 
            self.red, self.green, self.blue, self.alpha)

    def copy(self):
        return tuple(self.data)
        
    def _update_rgb(self, r, g, b):
        self.__dict__["__r"] = r
        self.__dict__["__g"] = g
        self.__dict__["__b"] = b
    
    def _update_hsb(self, h, s, b):
        self.__dict__["__h"] = h
        self.__dict__["__s"] = s
        self.__dict__["__brightness"] = b
    
    def _hasattrs(self, list):
        for a in list:
            if not self.__dict__.has_key(a):
                return False
        return True
    
    #added
    def __iter__(self):
        for i in range(len(self.data)):
           yield self.data[i]

    def __div__(self, other):
        value = float(other)
        return (self.red/value, self.green/value, self.blue/value, self.alpha/value)    

class ColorPalette(Color):
    def darken(self, step=0.1):
        return Color(self.h, self.s, self.brightness-step, self.a, mode="hsb", name="")
        
    def lighten(self, step=0.1):
        return Color(self.h, self.s, self.brightness+step, self.a, mode="hsb", name="")

    def desaturate(self, step=0.1):
        return Color(self.h, self.s-step, self.brightness, self.a, mode="hsb", name="")

    def saturate(self, step=0.1):
        return Color(self.h, self.s+step, self.brightness, self.a, mode="hsb", name="")

    def adjust_rgb(self, r=0.0, g=0.0, b=0.0, a=0.0):
        return Color(self.r+r, self.g+g, self.b+b, self.a+a, mode="rgb", name="")

    def adjust_hsb(self, h=0.0, s=0.0, b=0.0, a=0.0):
        return Color((self.h+h)%1.0, self.s+s, self.brightness+b, self.a+a, mode="hsb", name="")

    def adjust_contrast(self, step=0.1):
        if self.brightness <= 0.5:
            return self.darken(step)
        else:
            return self.lighten(step)
    
    def rotate_rgb(self, angle=180):
        h = (self.h + 1.0*angle/360)%1
        return Color(h, self.s, self.brightness, self.a, mode="hsb", name="")
    
    
    def rotate_ryb(self, angle=180):

        """ Returns a color rotated on the artistic RYB color wheel.
        
        An artistic color wheel has slightly different opposites
        (e.g. purple-yellow instead of purple-lime).
        It is mathematically incorrect but generally assumed
        to provide better complementary colors.
    
        http://en.wikipedia.org/wiki/RYB_color_model
    
        """

        h = self.h * 360
        angle = angle % 360

        # Approximation of Itten's RYB color wheel.
        # In HSB, colors hues range from 0-360.
        # However, on the artistic color wheel these are not evenly distributed. 
        # The second tuple value contains the actual distribution.
        wheel = [
            (  0,   0), ( 15,   8),
            ( 30,  17), ( 45,  26),
            ( 60,  34), ( 75,  41),
            ( 90,  48), (105,  54),
            (120,  60), (135,  81),
            (150, 103), (165, 123),
            (180, 138), (195, 155),
            (210, 171), (225, 187),
            (240, 204), (255, 219),
            (270, 234), (285, 251),
            (300, 267), (315, 282),
            (330, 298), (345, 329),
            (360, 0  )
        ]
    
        # Given a hue, find out under what angle it is
        # located on the artistic color wheel.
        for i in _range(len(wheel)-1):
            x0, y0 = wheel[i]    
            x1, y1 = wheel[i+1]
            if y1 < y0:
                y1 += 360
            if y0 <= h <= y1:
                a = 1.0 * x0 + (x1-x0) * (h-y0) / (y1-y0)
                break
    
        # And the user-given angle (e.g. complement).
        a = (a+angle) % 360

        # For the given angle, find out what hue is
        # located there on the artistic color wheel.
        for i in _range(len(wheel)-1):
            x0, y0 = wheel[i]    
            x1, y1 = wheel[i+1]
            if y1 < y0:
                y1 += 360
            if x0 <= a <= x1:
                h = 1.0 * y0 + (y1-y0) * (a-x0) / (x1-x0)
                break
    
        h = h % 360
        return Color(h/360, self.s, self.brightness, self.a, mode="hsb", name="")
    
    rotate = rotate_ryb
    complement = property(rotate_ryb)
    
    def invert(self):
        return rgb(1-self.r, 1-self.g, 1-self.b)
        
    inverse = property(invert)
    
    def analog(self, angle=20, d=0.5):
        clr = self.rotate_ryb(angle * (random()*2-1))
        clr.brightness += d * (random()*2-1)
        clr.saturation += d * (random()*2-1)
        return clr
        
    def nearest_hue(self, primary=False):
    
        """ Returns the name of the nearest named hue.
    
        For example,
        if you supply an indigo color (a color between blue and violet),
        the return value is "violet". If primary is set  to True,
        the return value is "purple".
    
        Primary colors leave out the fuzzy lime, teal, 
        cyan, azure and violet hues.
    
        """
     
        if self.is_black: return "black"
        if self.is_white: return "white"
        if self.is_grey : return "grey"
    
        if primary:
            hues = primary_hues
        else:
            hues = named_hues.keys()
        nearest, d = "", 1.0
        for hue in hues:
            if abs(self.hue-named_hues[hue])%1 < d:
                nearest, d = hue, abs(self.hue-named_hues[hue])%1
    
        return nearest
    
    def blend(self, clr, factor=0.5):
        
        """ Returns a mix of two colors.
        """
        
        r = self.r*(1-factor) + clr.r*factor
        g = self.g*(1-factor) + clr.g*factor
        b = self.b*(1-factor) + clr.b*factor
        a = self.a*(1-factor) + clr.a*factor
        return Color(r, g, b, a, mode="rgb")
    
    def distance(self, clr):
        
        """ Returns the Euclidean distance between two colors (0.0-1.0).
        
        Consider colors arranged on the color wheel:
        - hue is the angle of a color along the center
        - saturation is the distance of a color from the center
        - brightness is the elevation of a color from the center
          (i.e. we're on color a sphere)
        
        """
        
        coord = lambda a, d: (cos(radians(a))*d, sin(radians(a))*d)
        x0, y0 = coord(self.h*360, self.s)
        x1, y1 = coord(clr.h*360, clr.s)
        z0 = self.brightness
        z1 = clr.brightness
        d = sqrt((x1-x0)**2 + (y1-y0)**2 + (z1-z0)**2)
        return d
    
    def swatch(self, x, y, w=35, h=35, roundness=0):
    
        """ Rectangle swatch for this color.
        """
        
        _ctx.fill(self)
        _ctx.rect(x, y, w, h, roundness)

    draw = swatch

    @property
    def is_black(self):
        if self.r == self.g == self.b < 0.08:
            return True
        return False
        
    @property
    def is_white(self):
        if self.r == self.g == self.b == 1:
            return True
        return False
    
    @property
    def is_grey(self):
        if self.r == self.g == self.b: 
            return True
        return False
        
    is_gray = is_grey
    
    @property
    def is_transparent(self):
        if self.a == 0:
            return True
        return False

    @property
    def hex(self):
        r, g, b = [int(n * 255) for n in (self.r, self.g, self.b)]
        s = "#%2x%2x%2x" % (r, g, b)
        return s.replace(" ", "0")

    def _radial_gradient_step(colors, i, n):
        l = len(colors)-1
        a = int(1.0*i/n*l)
        a = min(a+0, l)
        b = min(a+1, l)
        base = 1.0 * n/l * a
        d = (i-base) / (n/l)
        R = colors[a].r*(1-d) + colors[b].r*d
        G = colors[a].g*(1-d) + colors[b].g*d
        B = colors[a].b*(1-d) + colors[b].b*d
        return (R, G, B)

    def radial_gradient(colors, x, y, radius, steps=300):
        """ Radial gradient using the given list of colors. """
        for i in range(steps):
            ctx.fill(self._radial_gradient_step(colors, i, steps))
            ctx.oval(x+i, y+i, radius-i*2, radius-i*2)  
 
