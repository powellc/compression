import heapq
import json
from collections import Counter
from typing import Dict, Tuple

class HuffmanNode:
    def __init__(self, char: str = None, freq: int = 0, left: 'HuffmanNode' = None, right: 'HuffmanNode' = None):
        self.char = char
        self.freq = freq
        self.left = left
        self.right = right

    def __lt__(self, other: 'HuffmanNode'):
        return self.freq < other.freq

class HuffmanTree:
    encoded_string: str = ""
    decoded_string: str = ""
    tree: list[HuffmanNode]
    codes: list

    def __init__(self, text: str, include_tree: bool = True):
        self.text = text
        self.include_tree = include_tree

    @classmethod
    def _serialize_tree(cls, node: HuffmanNode) -> dict:
        if node is None:
            return None
        return {
            "char": node.char,
            "freq": node.freq,
            "left": cls._serialize_tree(node.left),
            "right": cls._serialize_tree(node.right),
        }

    @classmethod
    def _deserialize_tree(cls, data: dict) -> HuffmanNode:
        if data is None:
            return None
        return HuffmanNode(
            char=data["char"],
            freq=data["freq"],
            left=cls._deserialize_tree(data["left"]),
            right=cls._deserialize_tree(data["right"])
        )

    @classmethod
    def _generate_codes(cls, node: HuffmanNode, prefix: str = "", codes: Dict[str, str] = None) -> Dict[str, str]:
        if codes is None:
            codes = {}
        if node.char is not None:
            codes[node.char] = prefix
        else:
            if node.left:
                cls._generate_codes(node.left, prefix + "0", codes)
            if node.right:
                cls._generate_codes(node.right, prefix + "1", codes)
        return codes

    def _build_tree(self) -> HuffmanNode:
        freq_counter = Counter(self.text)
        heap = [HuffmanNode(char, freq) for char, freq in freq_counter.items()]
        heapq.heapify(heap)

        while len(heap) > 1:
            left = heapq.heappop(heap)
            right = heapq.heappop(heap)
            merged = HuffmanNode(freq=left.freq + right.freq, left=left, right=right)
            heapq.heappush(heap, merged)

        return heap[0]

    def encode(self) -> Tuple[str, str]:
        self.tree = self._build_tree()
        self.codes = self._generate_codes(self.tree)
        self.encoded_string = ''.join(self.codes[char] for char in self.text)
        if self.include_tree:
            tree_json = json.dumps(self._serialize_tree(self.tree))
            self.encoded_string = tree_json + "|" + self.encoded_string
        return self.encoded_string

    def decode(self) -> str:
        if "|" not in self.encoded_string:
            return ""
        tree_json, encoded_text = self.encoded_string.split("|", 1)
        tree = self._deserialize_tree(json.loads(tree_json))
        node = tree
        for bit in encoded_text:
            node = node.left if bit == "0" else node.right
            if node.char is not None:
                self.decoded_string += node.char
                node = tree
        return self.decoded_string


# Example usage
if __name__ == '__main__':
    huff = HuffmanTree("hello world")
    print("Encoded:", huff.encode())
    print("Decoded:", huff.decode())
