from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

from heatmap import Heatmap

def plot_gradient_series(color_dict, pointsize=100):
    ''' Take a dictionary containing the color
      gradient in RBG and hex form and plot
      it to a 3D matplotlib device '''

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    xcol = color_dict["r"]
    ycol = color_dict["g"]
    zcol = color_dict["b"]

    # We can pass a vector of colors
    # corresponding to each point
    ax.scatter(xcol, ycol, zcol, c=color_dict["hex"], s=pointsize)

    # If bezier control points passed to function,
    # plot along with curve


    ax.set_xlabel('Red Value')
    ax.set_ylabel('Green Value')
    ax.set_zlabel('Blue Value')
    ax.set_zlim3d(0, 255)
    plt.ylim(0, 255)
    plt.xlim(0, 255)

    # # Save two views of each plot
    # ax.view_init(elev=15, azim=68)
    # plt.savefig(filename + ".svg")
    # ax.view_init(elev=15, azim=28)
    # plt.savefig(filename + "_view_2.svg")

    # Show plot for testing
    plt.show()

if __name__ == "__main__":
    start_hex = "#596147"
    end_hex = "#f0e247"
    mid_2 = "#f01221"
    mid_3 = "#ab8a47"
    mid_hex = [2, 1]

    percentiles = [100, 40, 10, 0]

    colour_list = [start_hex, mid_2, mid_3]
    hm = Heatmap()
    colour_dict = hm._poly_linear_gradient(colour_list, 100)
    print(colour_dict)
    plot_gradient_series(colour_dict, pointsize=100)