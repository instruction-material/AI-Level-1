"""Run the exact published graph examples and verify graph structure and PNGs."""
from pathlib import Path
import argparse,hashlib,importlib.metadata,json,os,runpy
ROOT=Path(__file__).resolve().parent
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument("--proof-dir",type=Path,required=True)
out=parser.parse_args().proof_dir.resolve();out.mkdir(parents=True,exist_ok=True)
os.environ["MPLBACKEND"]="Agg";os.environ["MPLCONFIGDIR"]=str(out/"matplotlib-cache")
import matplotlib.pyplot as plt
import networkx as nx
from PIL import Image
PUBLISHED_HASHES={'FAI-Graphs-with-Network-Updated/main.py': 'c0d7460b9ce7b4532295c3dfc2974a6ab314804e1c05ebe87e13d4ed51c82d27', 'FAI-Special-Graphs/main.py': '5548efdfe08e538f3123fdd14665b8a31a89483c0945107a0f4d25537de7b73b'}
for name,expected in PUBLISHED_HASHES.items():
 assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==expected,name
old=Path.cwd()
try:
 os.chdir(out)
 first=runpy.run_path(str(ROOT/"FAI-Graphs-with-Network-Updated/main.py"))
 second=runpy.run_path(str(ROOT/"FAI-Special-Graphs/main.py"))
finally:
 plt.close("all");os.chdir(old)
edges={frozenset(x) for x in [("a","b"),("a","c"),("c","d"),("d","a")]}
g1,g2,g4,g5=first["G1"],first["G2"],second["G4"],second["G5"]
assert set(g1.nodes)=={"a","b","c","d"} and {frozenset(x) for x in g1.edges}==edges
assert not g1.is_directed() and len(nx.cycle_basis(g1))==1
assert nx.is_tree(g2) and set(g2.nodes)=={"a","b","c","d"} and g2.number_of_edges()==3
assert {frozenset((a,b)):v for (a,b),v in nx.get_edge_attributes(g4,"weight").items()}==dict(zip([frozenset(x) for x in [("a","b"),("a","c"),("c","d"),("d","a")]],[0,1,2,3]))
assert g5.is_directed() and set(g5.edges)=={("a","b"),("a","c"),("c","d"),("d","a")}
assert not g5.has_edge("b","a") and not g5.has_edge("d","c")
images=[]
for name in ["basic_graph.png","acyclic_graph.png","weighted_graph.png","directed_graph.png"]:
 path=out/name
 with Image.open(path) as image:
  assert image.format=="PNG" and min(image.size)>=200
  image.load();rgb=image.convert("RGB")
  nonwhite=sum(count for count,color in rgb.getcolors(rgb.width*rgb.height) if min(color)<245)
  assert nonwhite>500,(name,nonwhite)
  images.append(dict(name=name,width=rgb.width,height=rgb.height,nonwhitePixels=nonwhite,sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
proof=dict(source=os.environ.get("GITHUB_SHA"),publishedReference="b18be61c865ae45d4ab15dc1b633c1c83d50da12",sourceFiles=PUBLISHED_HASHES,exampleProgramsRun=2,graphStructuresVerified=4,renderedPNGs=images,dependencies={p:importlib.metadata.version(p) for p in ["networkx","matplotlib","pillow"]},allAssertionsPassed=True)
(out/"proof.json").write_text(json.dumps(proof,indent=2)+"\n")
print(json.dumps(proof))
