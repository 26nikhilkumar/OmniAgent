import re
from typing import Iterable

from neo4j import GraphDatabase


class CoOccurrenceGraph:
    def __init__(self, uri: str = "bolt://localhost:7687", user: str = "neo4j", password: str = "neo4jpassword") -> None:
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    @staticmethod
    def _extract_entities(text: str) -> list[str]:
        entities = re.findall(r"\b[A-Z][a-zA-Z]{2,}\b", text)
        return list(dict.fromkeys(entities))

    def build_from_chunks(self, chunks: Iterable[str]) -> None:
        with self.driver.session() as session:
            for chunk in chunks:
                entities = self._extract_entities(chunk)
                for entity in entities:
                    session.run("MERGE (:Entity {name: $name})", name=entity)
                for i in range(len(entities) - 1):
                    session.run(
                        """
                        MATCH (a:Entity {name: $a}), (b:Entity {name: $b})
                        MERGE (a)-[r:RELATED_TO]-(b)
                        ON CREATE SET r.weight = 1
                        ON MATCH SET r.weight = r.weight + 1
                        """,
                        a=entities[i],
                        b=entities[i + 1],
                    )

    def retrieve_related(self, entity: str, depth: int = 2) -> list[str]:
        query = """
        MATCH (e:Entity {name: $entity})-[*1..$depth]-(related:Entity)
        RETURN DISTINCT related.name AS name
        LIMIT 20
        """
        with self.driver.session() as session:
            result = session.run(query, entity=entity, depth=depth)
            return [record["name"] for record in result]
