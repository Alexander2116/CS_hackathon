from manim import *
import numpy as np
import math

class basis2( Scene ):
    def construct( self ):

        radius = 4
        axes = Axes( x_range = [0, 1, 1], y_range = [0, 1, 1], x_length = radius, y_length = radius,
                        axis_config = {"include_tip": True, "numbers_to_exclude": [0]} ).add_coordinates()

        origin = axes.coords_to_point( 0, 0 )
        e1dir = RIGHT
        e2dir = UP

        x1 = origin + radius * e1dir
        x2 = origin + radius * e2dir

        r = lambda t: origin + radius * e1dir * np.cos( t * 0.5 * PI ) + radius * e2dir * np.sin( t * 0.5 * PI )
        tv = lambda t: - e1dir * np.sin( t * 0.5 * PI ) + e2dir * np.cos( t * 0.5 * PI )

        def rmove(a, t):
            p = r(t)
            d = (p - origin)/4
            a.put_start_and_end_on( p, p + d )

        def tmove(a, t):
            p = r(t)
            d = tv(t)
            a.put_start_and_end_on( p, p + d )
        
        def u1(mob):
            t = t_parameter.get_value()
            rmove( mob, t )

        def u2(mob):
            t = t_parameter.get_value()
            tmove( mob, t )

        t_parameter = ValueTracker(0)
        e1 = Arrow( start = x1, end = x1 + e1dir, color = GREEN, buff = 0 ).add_updater(u1).update()
        e2 = Arrow( start = x1, end = x1 + e2dir, color = GREEN, buff = 0 ).add_updater(u2).update()

        g1 = ParametricFunction( r,
                                    t_range=[0, 1],
                                    scaling=axes.x_axis.scaling, color=YELLOW )

        self.add( VGroup( axes, g1, e1, e2 ) )
        self.wait( 1 )

        self.play( UpdateFromAlphaFunc( t_parameter, 
                                        lambda mob, alpha: mob.set_value( alpha ) ),
                                        run_time=6 )
        self.wait( 1 )