type HuffmanNode = {
  char?: string;
  freq: number;
  left?: HuffmanNode;
  right?: HuffmanNode;
};

function buildHuffmanTree(frequencies: Map<string, number>): HuffmanNode {
  const nodes: HuffmanNode[] = Array.from(frequencies.entries()).map(
    ([char, freq]) => ({ char, freq })
  );

  while (nodes.length > 1) {
    nodes.sort((a, b) => a.freq - b.freq);
    const left = nodes.shift()!;
    const right = nodes.shift()!;
    nodes.push({ freq: left.freq + right.freq, left, right });
  }

  return nodes[0];
}

function generateHuffmanCodes(node: HuffmanNode, prefix = "", codes: Map<string, string> = new Map()): Map<string, string> {
  if (node.char !== undefined) {
    codes.set(node.char, prefix);
  } else {
    if (node.left) generateHuffmanCodes(node.left, prefix + "0", codes);
    if (node.right) generateHuffmanCodes(node.right, prefix + "1", codes);
  }
  return codes;
}

function huffmanEncode(text: string): { encoded: string; codes: Map<string, string> } {
  const frequencies = new Map<string, number>();
  for (const char of text) {
    frequencies.set(char, (frequencies.get(char) || 0) + 1);
  }

  const tree = buildHuffmanTree(frequencies);
  const codes = generateHuffmanCodes(tree);

  const encoded = text.split("").map(char => codes.get(char)!).join("");
  const originalSize = new TextEncoder().encode(text).length * 8; // in bits
  const encodedSize = encoded.length; // in bits
  console.log("Size before compression:", originalSize);
  console.log("Size after compression:", encodedSize);
  return { encoded, codes, tree};
}

function huffmanDecode(encoded: string, tree: HuffmanNode): string {
  let decoded = "";
  let node: HuffmanNode = tree;

  for (const bit of encoded) {
    node = bit === "0" ? node.left! : node.right!;
    if (node.char !== undefined) {
      decoded += node.char;
      node = tree;
    }
  }
  return decoded;
}

// Example usage:
const text = "This is a quick string to demonstrate how we can encode a string using Huffman encoding";
const { encoded, codes, tree } = huffmanEncode(text);
const decoded = huffmanDecode(encoded, tree);
console.log("Encoded:", encoded);
console.log("Huffman Codes:", codes);
console.log("Decoded:", decoded);
console.log("Tree size:", tree.length);
