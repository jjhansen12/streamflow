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

import pandas as pd
def summarize(dates, flows, sites):
    """
    Excel verification for gauge 10163000:
    - Max Flow: 131.0 cfs
    - Average Flow: 56.95 cfs (57.0 cfs rounded)
    """
    summary_data = []
    
    # Print table header
    print(f"{'Gauge':<12} {'Max (cfs)':<12} {'Date of max':<22} {'Min (cfs)':<12} {'Avg (cfs)':<10}")
    
    for i, site in enumerate(sites):
        site_flows = flows[:, i]
        
        # Calculate statistics using numpy
        max_val = np.max(site_flows)
        max_idx = np.argmax(site_flows)
        max_date = dates[max_idx]
        min_val = np.min(site_flows)
        avg_val = np.mean(site_flows)
        
        # Print formatted row to terminal
        print(f"{str(site):<12} {max_val:<12.1f} {str(max_date):<22} {min_val:<12.1f} {avg_val:<10.1f}")
        
        # Collect data for DataFrame / CSV export
        summary_data.append({
            'Gauge': site,
            'Max (cfs)': max_val,
            'Date of max': max_date,
            'Min (cfs)': min_val,
            'Avg (cfs)': avg_val
        })
        
    # Save summary to CSV file
    summary_df = pd.DataFrame(summary_data)
    summary_df.to_csv('streamflow_summary.csv', index=False)

#RESULTS FROM EXCEL VERIFICATION
#Gauge number, Max (cfs), Date of max, Min (cfs), Avg (cfs)
#10163000, 131.0, 2021-06-01 08:15:00, 35.6, 56.95236111111111
#10155200, 215.0, 2021-06-27 17:00:00, 125.0, 166.4142361111111
#10155500, 259.0, 2021-06-24 20:15:00, 182.0, 213.34548611111111
#10154200, 406.0, 2021-06-02 05:15:00, 50.4, 139.61864583333335
#10155000, 754.0, 2021-06-03 05:45:00, 23.2, 187.79267361111113

# --- Step 6: Threshold Report Function ---
def report_threshold(flows, sites):
    """
    Asks the user for a flow threshold and calculates 
    how many hours each gauge stayed above that threshold.
    """
    # 1. Ask the user for a flow threshold using input()
    # We convert it to float so we can compare it against numerical streamflow values
    user_input = input("Enter a flow threshold in cfs: ")
    threshold = float(user_input)
    
    print(f"\nHours above threshold {threshold} cfs:")
    print(f"{'Gauge':<12} {'Hours Above':<10}")
    
    # 2. For each gauge, report how many hours the flow was above that threshold
    for i, site in enumerate(sites):
        site_flows = flows[:, i]
        
        # Each reading is 15 minutes (0.25 hours). 
        # np.sum counts the True values where flow > threshold.
        hours = np.sum(site_flows > threshold) * 0.25
        
        print(f"{str(site):<12} {hours:<10.2f}")

# --- Main Execution Block ---
if __name__ == "__main__":
    # Step 5 call
    summarize(dates, flows, sites)
    
    print("\n" + "="*40 + "\n")
    
    # Step 6 call
    report_threshold(flows, sites)