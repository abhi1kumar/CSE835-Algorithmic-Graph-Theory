

import plotting_params as params

def savefig(plt, path, show_message= True, tight_flag= True, newline= True):
    if show_message:
        print("=>Saving to {}".format(path))
    if tight_flag:
        plt.savefig(path, bbox_inches='tight', pad_inches=0)
    else:
        plt.savefig(path)
    if newline:
        print("")
