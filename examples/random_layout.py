import sys
from pathlib import Path
PROJ_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJ_DIR))
import citygenerator


if __name__ == "__main__":
    blocks, greenery, _ = citygenerator.generate_layout(xsize=200, ysize=200, zsize=200, imax=200, jtot=200, kmax=200, pbuild=0.4, pgreen=0.1, pfrontal=0.2, order="r", layoutrandom=0.6, heightrandom=0.4, margin=5, minwidth=8, minvolume=10, savesteps=False)
    print("blocks:", blocks)
    print("green space:", greenery)
    blockstats = citygenerator.calculate_blockstats(blocks, a0=200*200)
    print("lamda_p = ", blockstats['planindex'])
    print("lambda_f = ", blockstats['frontindex'])