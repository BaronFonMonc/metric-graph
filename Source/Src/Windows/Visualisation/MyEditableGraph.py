from netgraph import EditableGraph

from Data.Utils import parseStrToLatex


class MyEditableGraph(EditableGraph):

    def __init__(self, nodes, axes):
        super(MyEditableGraph, self).__init__(nodes, ax=axes, edge_label_fontdict=dict(
                                                                fontsize = 13,
                                                                bbox = dict(alpha=0.7,
                                                                            boxstyle='round',
                                                                            ec=(1, 1, 1),
                                                                            fc=(1.0, 1.0, 1.0))
                                                                )
                                              )

    def _edit_text_object(self, text_object, key):
        if len(key) == 1:
            if key == '$':
                if text_object.get_text() != '$':
                    text_object.set_text(text_object.get_text() + key)
            else:
                text_object.set_text(text_object.get_text() + key)
        elif key == 'backspace':
            text_object.set_text(text_object.get_text()[:-1])
        elif key == 'control':
            text_object.set_text(parseStrToLatex(text_object.get_text()))
        self.fig.canvas.draw_idle()