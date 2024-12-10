from derivative_library.graphics import Graph
from derivative_library.enums import (
    DerivativeType,
    AssetType,
    GraphType
)

graph:Graph = Graph(
    deriative_type=DerivativeType.OPTION,
    asset_type=AssetType.CALL,
    underlying_price=10,
    strike_price=10,
    days_to_maturity=10,
    domestic_rate=10,
    implied_volatility=50,
    dividend=0
)

graph.DerivativeToolSimulationGraph(
    graph_type=GraphType.DELTA,
    percentage_change=0.05
)
