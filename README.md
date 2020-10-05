 # Urban landscape generator
 
<img src="/examples/ULG.png" align="left" width="200"> 

Procedural generation of randomised urban layouts.

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.3747476.svg)](https://doi.org/10.5281/zenodo.3747476)

The urban landscape generator is a procedural algorithm that builds fractal like street networks based on urban morpholgy parameters.
The algorithm divides building blocks into smaller blocks until a target build-up area density is reached. Building blocks are then given heights to match the target frontal area density. An optional greenery density can be defined. The layouts can be randomised by choosing a level of randomness, which influences the street widths, intersection points and building heights.

The fractal type of layout generation determines which block is chosen for subdivision. The *hierarchical* type chooses the blocks in a set order, such that all blocks on the same level of hierarchy are divided first, before going into a lower hierarchy level.
The *random* type selects a random block out of all available blocks. If the selected block is too small for further subdivision, the algorithm selects the next suitable block.
The *cascade* type selects the block for subdivision such that the largest of the most recently created blocks is further divided.

<img src="/examples/ULG-hierarchical.gif" width="250"> <img src="/examples/ULG-random.gif" width="250"> <img src="/examples/ULG-cascade.gif" width="250">

There are separate parameters for layout randomness and height randomness.
Layout randomness controlls the street intersection point and street width, height randomness controlls the building block height.
Two example layouts with a high degree of layout and height randomness (left) and a low degree of layout and height randomness (right) are shown below.

<img src="/examples/ULG-randomness.jpg" width="500">

## Requirements

- Python 3.5 or above
- Python libraries (see requirements.txt)

## How to use the Urban Landscape Generator

First make sure you have the required Python libraries installed on your system. An example case of the Urban Landscape Generator is provided in the `examples/` folder.
Run the example with e.g.:

``` sh
pip3 install -r requirements.txt
python3 examples/random_layout.py
```

The jupyter notebook [examples/generate_layouts.ipynb](https://nbviewer.jupyter.org/github/bss116/citygenerator/blob/master/examples/generate_layouts.ipynb) provides an examples on how to generate layouts, display the generation process and save the generated layouts.

## Reference

The Urban Landscape Generator is documented in:

Sützl, B.S., Rooney, G.G. & van Reeuwijk, M. Drag Distribution in Idealized Heterogeneous Urban Environments. Boundary-Layer Meteorol (2020). [https://doi.org/10.1007/s10546-020-00567-0](https://doi.org/10.1007/s10546-020-00567-0) (open access)
