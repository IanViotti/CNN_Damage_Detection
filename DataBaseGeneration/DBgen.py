import cluster_aux_fun as caf

if __name__ == '__main__': # This is used to run the script from cmd.
    struct_prop = (0.0125, 4, 0.2, 0.2)
    mat_prop = (17.679E9, 27.7E9, 6.001E9, 0.159, 1670, 113.565E6, 0.23, 46.16E6, 78.1)

    caf.run_cluster(struct_prop, mat_prop, 1)