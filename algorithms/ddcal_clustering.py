from clustering.ddcal import DDCAL

class DensityDistributionClusterAlgorithm():
    def __init__(self, frequencies):

        ddcal = DDCAL(n_clusters=8, feature_boundary_min=0.1, feature_boundary_max=0.49,
                  num_simulations=20, q_tolerance=0.45, q_tolerance_increase_step=0.5)
        # execute DDCAL algorithm
        ddcal.fit(frequencies)

        # the usefull arrays:
        self.sorted_data = ddcal.sorted_data
        self.labels_sorted_data = ddcal.labels_sorted_data