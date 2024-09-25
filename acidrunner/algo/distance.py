from typing import List, Tuple

import numpy as np
# Basic cosine similarity calculation with additional distance measures
class CosineSimilarityBasic:
    @staticmethod
    def calculate(buffer1: List[float], buffer2: List[float]) -> float:
        """Calculate cosine similarity between two vectors."""
        dot_product = np.dot(buffer1, buffer2)
        norm_buffer1 = np.linalg.norm(buffer1)
        norm_buffer2 = np.linalg.norm(buffer2)
        return dot_product / (norm_buffer1 * norm_buffer2)

    @staticmethod
    def is_in_range(value: float, value_range: Tuple[float, float]) -> bool:
        """Check if the given value is within the specified range."""
        return value_range[0] <= value <= value_range[1]
