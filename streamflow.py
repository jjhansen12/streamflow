import numpy as np
import matplotlib.pyplot as plt


def load_streamflow(filename):
    """Read the streamflow CSV. Return the dates and a 2D array of flows (cfs), one column per gauge."""
    array1 = np.genfromtxt('June-2021-Provo-River-Streamflow-Rates.csv', delimiter=',', dtype=str, skip_header=1)

    dates = array1[:, 0].astype('datetime64') 
    flows = np.column_stack((
        array1[:, 1].astype(float),
        array1[:, 2].astype(float),
        array1[:, 3].astype(float),
        array1[:, 4].astype(float),
        array1[:, 5].astype(float)
    ))
    return dates, flows


def plot_streamflow(dates, flows, sites):
    """Plot the flow at each gauge, with the same title, labels, and formatting as the Matplotlib HW."""
    plt.plot(dates, flows[:, 0], label=sites[0])
    plt.plot(dates, flows[:, 1], label=sites[1])
    plt.plot(dates, flows[:, 2], label=sites[2])
    plt.plot(dates, flows[:, 3], label=sites[3])
    plt.plot(dates, flows[:, 4], label=sites[4])
    plt.title('Provo River Streamflow Data (2021)')
    plt.xlabel('Date')
    plt.ylabel('Flowrate (cfs)')
    plt.legend(title='Site Numbers')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.legend(['10163000', '10155200', '10155500', '10154200', '10155000'], title='Site Numbers', loc='upper right')
    plt.grid(True)
    
    plt.savefig("provo_streamflow.png", dpi=150, bbox_inches="tight")
    plt.show()


# Main program
sites = ["10163000", "10155200", "10155500", "10154200", "10155000"]
dates, flows = load_streamflow("June-2021-Provo-River-Streamflow-Rates.csv")
plot_streamflow(dates, flows, sites)