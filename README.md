<img src="/examples/ULG.png" align="left" width="200"> 
 # Urban landscape generator
Procedural generation of randomised urban layouts. 

The urban landscape generator is a procedural algorithm that builds fractal like street networks based on urban morpholgy parameters.
The algorithm divides building blocks into smaller blocks until a target build-up area density $\lambda_p$ is reached. Building blocks are then given heights to match the target frontal area density $\lambda_f$. An optional greenery density $\lambda_g$ can be defined.
Randomness $r$ influences the street widths, intersection points and building heights. 

The fractal type of layout generation determines which block is chosen for subdivision. The *hierarchical* type chooses the blocks in a set order, such that all blocks on the same level of hierarchy are divided first, before going into a lower hierarchy level. 
The *random* type selects a random block out of all available blocks. If the selected block is too small for further subdivision, the algorithm selects the next suitable block.
The *cascade* type selects the block for subdivision such that the largest of the most recently created blocks is further divided. 

<img src="/examples/ULG-hierarchical.gif" width="250"> <img src="/examples/ULG-random.gif" width="250"> <img src="/examples/ULG-cascade.gif" width="250"> 

There are separate parameters for layout randomness (*lrandom*) and height randomness (*hrandom*).
Layout randomness controlls the street intersection point and street width, height randomness controlls the building block height.
Two example layouts with a high degree of layout and height randomness (left) and a low degree of layout and height randomness (right) are shown below.

<img src="/examples/ULG-randomness.jpg" width="500"> 

The jupyter notebook `generate_layouts.ipynb` provides an interface to generate layouts, display the generation process and save the generated layouts.
