from manim import *

class ORGate(VGroup): 
    def __init__(self, scene):
        super().__init__()
        self.scene = scene

        # Create the shapes of the OR gate
        self.or_uparc = ArcBetweenPoints(start = [-1,-1,0], end = [1,0,0], angle = PI/4)
        self.or_lowarc = ArcBetweenPoints(start = [-1,1,0], end = [1,0,0], angle = -PI/4)
        self.or_leftarc = ArcBetweenPoints(start = [-1,1,0], end = [-1,-1,0], angle = -PI/3)
        self.or_text = Text("OR").scale(0.75)

        self.A_pos = self.or_leftarc.get_left() + UP*0.5 + RIGHT*0.18
        self.B_pos = self.or_leftarc.get_left() + DOWN*0.5 + RIGHT*0.18
        self.O_pos = self.or_uparc.get_end()

        # Wires
        self.wireA = Line(
            start = self.or_leftarc.get_left() + UP*0.5 + RIGHT*0.18,
            end = self.or_leftarc.get_left() + LEFT*0.75 + UP*0.5 + RIGHT*0.15
        )
        self.wireB = Line(
            start = self.or_leftarc.get_left() + DOWN*0.5 + RIGHT*0.18,
            end = self.or_leftarc.get_left() + LEFT*0.75 + DOWN*0.5 + RIGHT*0.15
        )
        self.wireO = Line(
            start = self.or_uparc.get_end(),
            end = self.or_uparc.get_end() + RIGHT*0.75
        )

        # Add shapes to the group
        self.object = Group(self.or_uparc, self.or_lowarc, self.or_leftarc, self.or_text)
    
    def draw_gate(self):
        self.object = Group(self.or_uparc, self.or_lowarc, self.or_leftarc, self.or_text, self.wireA, self.wireB, self.wireO)
        return [
            Create(self.or_uparc),
            Create(self.or_lowarc),
            Create(self.or_leftarc),
            Write(self.or_text)
            ]
    
    def undraw_gate(self):
        self.object = Group(self.or_uparc, self.or_lowarc, self.or_leftarc, self.or_text)
        return [
            FadeOut(self.or_uparc), 
            FadeOut(self.or_lowarc), 
            FadeOut(self.or_leftarc), 
            FadeOut(self.or_text)
            ]
    
    def add_wires(self, draw=False):
        if draw:
            return [Write(self.wireA), Write(self.wireB), Write(self.wireO)]
        else:
            return [self.wireA, self.wireB, self.wireO]


    def remove_wires(self):
        return [FadeOut(self.wireA), FadeOut(self.wireB), FadeOut(self.wireO)]


class ANDGate(VGroup):
    def __init__(self, scene):
        super().__init__()
        self.scene = scene  

        # Create AND gate
        self.and_uphor  = Line(start = [0,1,0], end = [-1,1,0])
        self.and_lowhor = Line(start = [0,-1,0], end = [-1,-1, 0])
        self.and_ver    = Line(start = [-1,1,0], end = [-1,-1,0])
        self.and_arc    = Arc(radius = 1.0, start_angle = -PI/2 , angle = PI)
        self.and_text   = Text("AND").scale(0.75)

        self.A_pos = self.and_uphor.get_left() + UP*0.5 + RIGHT*0.18
        self.B_pos = self.and_uphor.get_left() + DOWN*0.5 + RIGHT*0.18
        self.O_pos = self.and_arc.get_end()

        # Wires
        self.wireA = Line(
            start = self.and_uphor.get_left() + DOWN*0.5,
            end = self.and_uphor.get_left() + LEFT*0.75 + DOWN*0.5
        )
        self.wireB = Line(
            start = self.and_uphor.get_left() + DOWN*1.5,
            end = self.and_uphor.get_left() + LEFT*0.75 + DOWN*1.5
        )
        self.wireO = Line(
            start = self.and_arc.get_right(),
            end = self.and_arc.get_right() + RIGHT*0.75
        )

        self.object = Group(self.and_uphor, self.and_lowhor, self.and_ver, self.and_arc, self.and_text)
    
    def draw_gate(self):
        self.object = Group(self.and_uphor, self.and_lowhor, self.and_ver, self.and_arc, self.and_text, self.wireA, self.wireB, self.wireO)
        return [
            Create(self.and_uphor),
            Create(self.and_lowhor),
            Create(self.and_ver),
            Create(self.and_arc),
            Write(self.and_text)
            ]
    
    def undraw_gate(self):
        self.object = Group(self.and_uphor, self.and_lowhor, self.and_ver, self.and_arc, self.and_text)
        return [
            FadeOut(self.and_uphor),
            FadeOut(self.and_lowhor),
            FadeOut(self.and_ver),
            FadeOut(self.and_arc),
            FadeOut(self.and_text)
        ]

    def add_wires(self, draw=False):
        # Create wires that always redraw based on the gate's position
        if draw:
            return [Write(self.wireA), Write(self.wireB), Write(self.wireO)]
        else:
            return [self.wireA, self.wireB, self.wireO]
        
    def remove_wires(self):
        return [FadeOut(self.wireA), FadeOut(self.wireB), FadeOut(self.wireO)]

class NOTGate(VGroup):
    def __init__(self, scene):
        self.scene = scene  

        # Create AND gate
        self.not_tri = Polygon([1 - np.sqrt(3),1,0],[1 - np.sqrt(3),-1,0],[1,0,0], color = WHITE)
        self.not_cir = Circle(radius = 0.2, color = WHITE).move_to([1.2,0,0])
        self.not_text = Text("NOT").scale(0.75)

        self.wireA = Line(
            start = self.not_tri.get_left() + UP*0.5,
            end = self.not_tri.get_left() + LEFT*0.75 + UP*0.5
        )
        self.wireB = Line(
            start = self.not_tri.get_left() + DOWN*0.5,
            end = self.not_tri.get_left() + LEFT*0.75 + DOWN*0.5
        )
        self.wireO = Line(
            start = self.not_cir.get_right(),
            end = self.not_cir.get_right() + RIGHT*0.75
        )

        self.object = Group(self.not_tri, self.not_cir, self.not_text)
    
    def draw_gate(self):
        self.object = Group(self.not_tri, self.not_cir, self.not_text, self.wireA, self.wireB, self.wireO)
        return [
            Create(self.not_tri),
            Create(self.not_cir),
            Write(self.not_text)
        ]

    
    def undraw_gate(self):
        self.object = Group(self.not_tri, self.not_cir, self.not_text)
        return [
            FadeOut(self.not_tri),
            FadeOut(self.not_cir),
            FadeOut(self.not_text)
        ]

    def add_wires(self, draw=False):
        if draw:
            return [Write(self.wireA), Write(self.wireB), Write(self.wireO)]
        else:
            return [self.wireA, self.wireB, self.wireO]
        
    def remove_wires(self):
        return [FadeOut(self.wireA), FadeOut(self.wireB), FadeOut(self.wireO)]

def connect(object1_wire, object2_wire):
    connecting_line = Line(start=[object1_wire.get_right()], end=[object2_wire.get_left()])

    return connecting_line