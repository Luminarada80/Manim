from manim import *

class NodesAndEdges(Scene):
    def construct(self):

        self.camera.background_color=BLACK
        # self.nodes_and_edges_scene()
        vertices = [0, 1, 2]
        edges = [(0, 1), (0, 2)]
        positions = {
            0: [-5, -0.25, 0],
            1: [0, 1, 0],
            2: [0, -1, 0]
        }

        graph = self.create_digraph(vertices, edges, positions)
        node_label = Text("Node").shift(1.5 * UP)

        graph[0].scale(2).move_to([0, 0, 0])
        self.play(Write(node_label),
                  DrawBorderThenFill(graph[0]))
        
        self.play(
            node_label.animate.scale(0.5).shift(1*DOWN).shift(5*LEFT),
            graph[0].animate.move_to([-5, -0.25, 0]).scale(0.5)
            )

        self.play(DrawBorderThenFill(graph[1]),
                  DrawBorderThenFill(graph[2]))
                
        edge_label = Text('Edge').scale(0.5).rotate(0).move_to([-2.5, 0.75, 0])
        
        arrow1 = Arrow(graph[0].align_to(RIGHT), graph[1].align_to(LEFT), buff=0)
        arrow2 = Arrow(graph[0].align_to(RIGHT), graph[2].align_to(LEFT), buff=0)

        self.play(Write(edge_label),
                  Create(arrow1),
                  Create(arrow2))
        
        self.add(graph)

        self.play(FadeOut(arrow1, arrow2))

        self.wait(1)

        self.play(Unwrite(edge_label), Unwrite(node_label))

        self.wait(1)

        # self.play(graph.animate.scale(0.5))

        # New vertices, edges, and positions to add
        new_vertices = [3, 4, 5, 6]  # Adding vertices 3 and 4
        new_edges = [(2, 3), (3, 4), (4, 0), (1, 3), (1, 5), (5, 6), (6, 0)]  # Adding new edges
        new_positions = {
            3: [3, 1, 0],  # Position for vertex 3
            4: [1, -3, 0],  # Position for vertex 4
            5: [2.5, 3, 0],
            6: [-3, 1.5, 0]
        }

        # Update existing structures with new elements
        vertices.extend(new_vertices)
        edges.extend(new_edges)
        positions.update(new_positions)

        # Recreate the graph with the updated information
        updated_graph = self.create_digraph(vertices, edges, positions)
                
        # Animate the updated graph
        self.play(DrawBorderThenFill(updated_graph))
        self.remove(graph)
        self.play(updated_graph.animate.scale(0.5))

        activation_label = Text("Nodes can be \n activated").scale(0.5)
        always(activation_label.next_to, updated_graph[0].get_left(), LEFT*2)

        self.play(Write(activation_label, run_time=0.5),
                  updated_graph[0].animate.scale(1.25).set_fill(GREEN),
                  updated_graph[1].animate.scale(1.25).set_fill(GREEN),
                  updated_graph[2].animate.scale(1.25).set_fill(GREEN))
        self.play(Unwrite(activation_label, run_time=0.5),
            updated_graph[0].animate.scale(0.75).set_fill(BLUE_E),
            updated_graph[1].animate.scale(0.75).set_fill(BLUE_E),
            updated_graph[2].animate.scale(0.75).set_fill(BLUE_E))

        inactivation_label = Text("Nodes can be \n inactivated").scale(0.5)
        always(inactivation_label.next_to, updated_graph[0].get_left(), LEFT*2)
        self.play(Write(inactivation_label, run_time=0.5),
            updated_graph[0].animate.scale(1.25).set_fill(RED),
            updated_graph[1].animate.scale(1.25).set_fill(RED),
            updated_graph[2].animate.scale(1.25).set_fill(RED))
        
        self.play(Unwrite(inactivation_label, run_time=0.5),
            updated_graph[0].animate.scale(0.75).set_fill(BLUE_E),
            updated_graph[1].animate.scale(0.75).set_fill(BLUE_E),
            updated_graph[2].animate.scale(0.75).set_fill(BLUE_E))

        self.play(updated_graph.animate.scale(2).shift(LEFT*3))
        attention_border = Rectangle(width=5, height=3.5, stroke_width=4).shift(LEFT*1.5)

        # List of vertices to keep highlighted
        attention_list = [1, 2, 3]

        # List to store animations
        animations = []

        # Iterate over the vertices in the graph
        for vertex_label, vertex_obj in updated_graph.vertices.items():
            if vertex_label not in attention_list:
                # If the vertex is not in the attention list, dim it
                animations.append(vertex_obj.animate.set_opacity(0.5))

        self.play(
            DrawBorderThenFill(attention_border),
            Circumscribe(attention_border),
            updated_graph[1].animate.scale(1.25),
            updated_graph[2].animate.scale(1.25),
            updated_graph[3].animate.scale(1.25),
            *animations
            )
        text = Text("When there are two nodes signaling to another, \n we dont know the logic connecting them \n (AND, OR, NOT)").scale(0.4)
        always(text.next_to, attention_border.get_right(), RIGHT*1.5)

        self.play(Write(text))

        self.wait(2)
        self.play(Unwrite(text))

        self.play(updated_graph.animate.shift(LEFT*2).scale(0.75),
                  attention_border.animate.shift(LEFT*2.5).scale(0.75))

        table_title = Text("Expression").scale(0.75)
        table = Table([["1", "1", "0", "0", "1", "0", "1"],
                       ["0", "1", "1", "0", "1", "1", "1"],
                       ["0", "1", "0", "0", "1", "0", "1"]],
                       row_labels=[Text("Gene 1"), Text("Gene 2"), Text("Gene 3")],
                       include_outer_lines=True)
        table.scale(0.5)

        always(table_title.next_to, table.get_center(), UP*4)
        always(table.next_to, attention_border.get_right(), RIGHT*4)

        gene1_label = Text('1').scale(0.75)
        gene2_label = Text('2').scale(0.75)
        gene3_label = Text('3').scale(0.75)
        always(gene1_label.move_to, updated_graph[1].get_center())
        always(gene2_label.move_to, updated_graph[2].get_center())
        always(gene3_label.move_to, updated_graph[3].get_center())

        logic_text = Text("We can determine the rule between Genes 1 and 2\n by looking at the expression table and seeing \n when Gene 3 activates")
        logic_text.shift(DOWN*2, RIGHT*2.5)
        logic_text.scale(0.5)

        logic_text2 = Text("In this case, the rule should be AND, because \n Gene 1 AND Gene 2 have to signal \n to activate Gene 3")
        logic_text2.shift(DOWN*2, RIGHT*2.5)
        logic_text2.scale(0.5)

        self.play(Write(table_title),
                  Write(table),
                  Write(logic_text),
                  Write(gene1_label),
                  Write(gene2_label),
                  Write(gene3_label))
        
        self.wait(2)

        column_outline = Rectangle(width=0.79, height=2).set_stroke(YELLOW_C)
        column_outline.move_to(table.get_center()).shift(LEFT*1.55)

        #Column 1
        self.play(DrawBorderThenFill(column_outline),
                  updated_graph[1].animate.scale(1.25).set_fill(GREEN))
        self.wait(1)
        
        # Column 2
        self.play(column_outline.animate.shift(RIGHT*0.80),
                  updated_graph[2].animate.scale(1.25).set_fill(GREEN),
                  updated_graph[3].animate.scale(1.25).set_fill(GREEN))
        # self.wait(0.5)
        
        # Column 3
        self.play(column_outline.animate.shift(RIGHT*0.80),
            updated_graph[1].animate.scale(0.75).set_fill(BLUE_E),
            updated_graph[3].animate.scale(0.75).set_fill(BLUE_E))
        # self.wait(0.5)

        # Column 4
        self.play(column_outline.animate.shift(RIGHT*0.80),
            updated_graph[2].animate.scale(0.75).set_fill(BLUE_E),
            FadeOut(logic_text, shift=DOWN*0.5))
        # self.wait(0.5)

        # Column 5
        self.play(column_outline.animate.shift(RIGHT*0.80),
            updated_graph[1].animate.scale(1.25).set_fill(GREEN),      
            updated_graph[2].animate.scale(1.25).set_fill(GREEN),
            updated_graph[3].animate.scale(1.25).set_fill(GREEN),
            FadeIn(logic_text2, shift=DOWN*0.5))
        # self.wait(0.5)

        # Column 6
        self.play(column_outline.animate.shift(RIGHT*0.80),
            updated_graph[1].animate.scale(0.75).set_fill(BLUE_E),
            updated_graph[3].animate.scale(0.75).set_fill(BLUE_E))
        # self.wait(0.5)
        
        #Column 7
        self.play(column_outline.animate.shift(RIGHT*0.79),
            updated_graph[2].animate.scale(0.75).set_fill(BLUE_E))

        self.wait(2)
        self.play(FadeOut(logic_text2, shift=DOWN*0.5))

        self.wait(5)

    def create_digraph(self, vertices, edges, positions):

        vertex_config = {
            "fill_color": BLUE_E,
            "radius": 0.5,
            "stroke_color": WHITE,
            "stroke_width": 4,
        }

        edge_config = {
            "stroke_width": 5.25,
            "tip_config": {
                "tip_length": 0.35,
                "tip_width": 0.35
            },
        }

        # Create a DiGraph with specified positions
        graph = DiGraph(vertices, edges, layout=positions, edge_config=edge_config, vertex_config=vertex_config)

        return graph

class ErrorCalculationTable(Scene):
    def construct(self):
        pass