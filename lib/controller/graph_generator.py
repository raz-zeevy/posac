from lib.gui.components.shapes import Edge
from lib.utils import P_POSACSEP_DIR


def generate_posacsep_graphs(controller, item : int):
    """
        Generate graphs for the given controller
        :param controller:
        :param item: item number
        :return: list of dicts with the following keys:
                    x: list of x coordinates
                    y: list of y coordinates
                    annotations: list of annotations
                    title: title of the graph
                    legend: list of legends
                    geoms: list of shapes
        """
    from lib.posac.posac_output_parser import OutputParser
    from lib.posac.posacsep_parser import parse_output as p_posacsep
    graph_data_list = []
    output = OutputParser.parse_output(controller.pos_out)
    posacsep = p_posacsep(P_POSACSEP_DIR)
    out_coords = output["out_coords"]
    n = len(out_coords['x'])
    basic_graph = dict(
        x=out_coords['x'],
        y=out_coords['y'],
        annotations=out_coords['index'],
        title="Posac Solution",
        legend=[dict(index=out_coords['index'][i],
                     value=out_coords['profiles'][i]) for i in range(n)],
    )
    titles = posacsep['titles']
    for i, sep in enumerate(posacsep['item_edges'][item]):
        graph = basic_graph.copy()
        graph["geoms"] = [Edge(x, y) for x, y in sep]
        graph['title'] = f"Item {item}\n {titles[i]}"
        graph['annotations'] = [i['value'].split()[item-1] for i in graph[
            'legend']]
        graph['legend'] = []
        graph_data_list.append(graph)
    return graph_data_list


def generate_graphs(controller):
    """
    Generate graphs for the given controller
    :param controller:
    :return: list of dicts with the following keys:
                x: list of x coordinates
                y: list of y coordinates
                annotations: list of annotations
                title: title of the graph
                legend: list of legends
                geoms: list of shapes
    """
    from lib.posac.lsa_parser import parse_output as parse_lsa
    from lib.posac.posac_output_parser import OutputParser
    graph_data_list = []
    output = OutputParser.parse_output(controller.pos_out)
    out_coords = output["out_coords"]
    n = len(out_coords['x'])
    graph_data_list.append(dict(
        x=out_coords['x'],
        y=out_coords['y'],
        annotations=out_coords['index'],
        title="Posac Solution",
        legend=[dict(index=out_coords['index'][i],
                     value=out_coords['profiles'][i]) for i in range(n)],
    ))
    for title, output in [
        ("LSA1 Solution", parse_lsa(controller.ls1_out)),
        ("LSA2 Solution", parse_lsa(controller.ls2_out)),
    ]:
        out_coords = output["out_coords"]
        n = len(out_coords['x'])
        graph_data_list.append(
            dict(
                x=out_coords["x"],
                y=out_coords["y"],
                annotations=out_coords["index"],
                title=title,
                legend=[
                    dict(index=out_coords["index"][i], value=out_coords["labels"][i])
                    for i in range(n)
                ],
            )
        )
    return graph_data_list
