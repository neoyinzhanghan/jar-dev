import numpy as np

from math import exp, log
from matplotlib import pyplot as plt

def gradient_fn(x, a=5, b=15, min_grad=0.2):

    # apply the logistic function to input x
    return max(1 / (1 + exp(a - (x / b))), min_grad)

def plot_grads_with_top_extended_boundaries_fixed(grads, starting_jar_dim=4, a=5, b=15):
    """
    Creates a square grid visualization with custom color gradients based on the
    inverse of a logistic function, with colors inverted so that white represents 0
    and bright blue represents 1. This version includes very thick solid black
    boundaries at the bottom, left, and right of the grid, with the left and right
    boundaries extended only above the grid to emphasize the edges. Adjusted to
    handle gradients of 0 properly.
    
    Parameters:
    - grads: List of gradient values for each cell in the grid.
    - starting_jar_dim: The dimension of the grid, determining its size as starting_jar_dim x starting_jar_dim.
    - a, b: Parameters of the logistic function used to calculate the inverse gradients.
    """

    while len(grads) >= starting_jar_dim**2:
        starting_jar_dim += 1

    while len(grads) < starting_jar_dim**2:
        grads.append(0)

    normalized_grads = grads
    
    # Create the grid for visualization
    grid = np.array(normalized_grads).reshape(starting_jar_dim, starting_jar_dim)

    # tranpose the grid
    grid = grid.T

    # flip the grid upside down
    grid = np.flip(grid, 0)

    # rotate the grid 90 degrees
    grid = np.rot90(grid)
    
    fig, ax = plt.subplots()
    # Display the grid with inverted color mapping (white for 0, bright blue for 1)
    ax.imshow(grid, cmap='Blues', vmin=0, vmax=1)  # '_r' to reverse the colormap
    
    # Hide the axes
    ax.axis('off')
    
    # Draw very thick black lines for the bottom boundary
    boundary_thickness = 20  # Very thick boundary
    ax.plot([-0.5, starting_jar_dim-0.5], [starting_jar_dim-0.5, starting_jar_dim-0.5], color='black', linewidth=boundary_thickness) # Bottom
    
    # Left and right boundaries extended only above the grid
    extension = 0.5  # Amount by which the boundaries extend above the grid
    ax.plot([-0.5, -0.5], [-0.5-extension, starting_jar_dim-0.5], color='black', linewidth=boundary_thickness) # Left
    ax.plot([starting_jar_dim-0.5, starting_jar_dim-0.5], [-0.5-extension, starting_jar_dim-0.5], color='black', linewidth=boundary_thickness) # Right
        
    return plt


def visualize(df, theme='basic', starting_jar_dim=4):

    starting_jar_dim = int(starting_jar_dim)

    # sort the df increasing order by Start Time
    df = df.sort_values(by="Start Time")

    grads = []
    # traverse through rows of the df
    for index, row in df.iterrows():
        duration = row["duration"]

        grads.append(gradient_fn(duration))

    return plot_grads_with_top_extended_boundaries_fixed(grads, starting_jar_dim=starting_jar_dim)


if __name__ == "__main__":
    plot_grads_with_top_extended_boundaries_fixed([0.3, 0.2, 0.8, 0.7, 0.8], starting_jar_dim=4)
        
