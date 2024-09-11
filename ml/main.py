from DKA import *
import uvicorn
from fastapi import FastAPI, HTTPException
from typing import Dict
from DKA import *



graph = Graph()

# Создаем вершины
graph.add_node(Node(id=1))

graph.add_node(Node(id=2))
graph.add_node(Node(id=3))
graph.add_node(Node(id=4))

graph.add_node(Node(id=5))

graph.add_node(Node(id=6))
graph.add_node(Node(id=7))

graph.add_node(Node(id=8))
graph.add_node(Node(id=9))
graph.add_node(Node(id=10))


# Из вевршины 1 можно попасть в вершины 2,3 и 4
graph.add_edge(from_id=1, to_id=2, key='to2node')
graph.add_edge(from_id=1, to_id=3, key='to3node')
graph.add_edge(from_id=1, to_id=4, key='to4node')

# из вершины 2 можно попасть в вершину 5, либо в саму себя
graph.add_edge(from_id=2, to_id=2, key='recursion')
graph.add_edge(from_id=2, to_id=5, key='to5node')

# из вершины 3 можно попасть в вершины 6 и 7
graph.add_edge(from_id=3, to_id=6, key='to6node')
graph.add_edge(from_id=3, to_id=7, key='to7node')

# из вершины 4 можно попасть в вершины 8, 9 и 10
graph.add_edge(from_id=4, to_id=8, key='to8node')
graph.add_edge(from_id=4, to_id=9, key='to9node')
graph.add_edge(from_id=4, to_id=10, key='to10node')


print(graph.predict(1))
# >>> {'to2node': 2, 'to3node': 3, 'to4node': 4}
# print(graph.predict(2))
# # >>> {'recursion': 2, 'to5node': 5}
# print(graph.predict(3))
# # >>> {'to6node': 6, 'to7node': 7}
# print(graph.predict(4))
# # >>> {'to8node': 8, 'to9node': 9, 'to10node': 10}



app = FastAPI()


@app.post("/nodes/")
def create_node(id: int, attachment: str = None):
    try:
        new_node = Node(id=id, attachment=attachment)
        graph.add_node(new_node)
        return {"message": "Node added successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/nodes/{id}")
def read_node(id: int):
    try:
        node = graph.get_node(id)
        return {"id": node.id, "attachment": node.attachment}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.delete("/nodes/{id}")
def delete_node(id: int):
    try:
        graph.delete_node(id)
        return {"message": "Node deleted successfully"}
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.post("/edges/")
def create_edge(from_id: int, to_id: int, key: str):
    try:
        graph.add_edge(from_id=from_id, to_id=to_id, key=key)
        return {"message": "Edge added successfully"}
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.delete("/edges/")
def delete_edge(from_id: int, key: str):
    try:
        graph.delete_edge(from_id=from_id, key=key)
        return {"message": "Edge deleted successfully"}
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.get("/predict/{id}")
def predict_edges(id: int):
    try:
        edges = graph.predict(id)
        return edges
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))


if __name__ == "__main__":
    uvicorn.run('main:app', host="0.0.0.0", port=8000, log_level="debug", reload=True)
