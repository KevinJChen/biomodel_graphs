from BioModelsDAG import extract_data, build_graph, DerivedModelParser
from BioModelsDAG.utils import timeit, yield_model_paths

from BioModelsDAG.utils import extract_model_data
from bs4 import BeautifulSoup

def extract_authorList(soup: BeautifulSoup):
    for resource in soup.find_all('div'):
        for tag in resource.find_all('bibo:authorList'):
            print('here')

@timeit
def main():
    import networkx

    # filepaths = yield_model_paths()
    # data = extract_data(filepaths, parser=DerivedModelParser(), print_fpath=False)
    # graph = build_graph(data)
    # networkx.write_graphml(graph, "graphs/derived_models.graphml")

    filepaths = yield_model_paths()

    # extracting other kinds of data from files

    # for filepath in filepaths:
    #     if '.DS_Store' in str(filepath):
    #         continue
    #     file = open(filepath, "r", encoding='utf8')
    #     soup = BeautifulSoup(file, features='lxml')
    #     #print(soup.p('class'))
    #     child_data = extract_model_data(file, soup=soup)
    #     extract_authorList(soup)

    data = extract_data(filepaths, parser=DerivedModelParser(), print_fpath=False)
    graph = build_graph(data)

    # how many models have an instance of derived from?
    num_derived_models = 0
    for node in graph.__iter__():
        if 'BIOMD' or 'MODEL' in str(node):
            num_derived_models = num_derived_models + 1

    print("There are " + str(num_derived_models) + " BIOMD of " + str(graph.number_of_nodes()) + " total nodes that have an instance of derived from.")

    # dict: node, number of degrees
    node_degrees = {}
    # dict: node with degrees over 9, number of degrees
    node_significant = {}

    #  fill out the two dicts
    for node in graph.__iter__():
        node_degrees[node] = graph.degree(node)
        if graph.degree(node) > 9:
            node_significant[node] = graph.degree(node)

    # neighbors of significant nodes
    for node in node_significant:
        for neighbor_node in graph.neighbors(node):
            print(str(neighbor_node) + " (" + str(graph.degree(neighbor_node)) + ")" + "  -- ", end='')
        print()


if __name__ == '__main__':
    main()