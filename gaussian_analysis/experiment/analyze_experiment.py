import os
import struct
import numpy as np
import matplotlib.pyplot as plt

# Folder where output files are stored
OUTPUT_DIR = "output"
FILE_EXTENSION = ".bin"
FIGURE_DIR = "figures"  # Directory to save figures

# Ensure the figures directory exists
os.makedirs(FIGURE_DIR, exist_ok=True)

# Function to read binary files containing int64_t nanosecond durations
def read_binary_file(filepath):
    with open(filepath, "rb") as f:
        data = f.read()
    # Unpack as int64_t (8 bytes per value)
    return np.array(struct.unpack(f"{len(data) // 8}q", data), dtype=np.int64)

# Function to determine automatic x-axis limits
def get_x_limits(data, method="iqr"):
    """Determine x-axis bounds using either IQR (default) or ±3σ method"""
    min_val, max_val = np.min(data), np.max(data)
    mean_val = np.mean(data)
    std_dev = np.std(data)

    if method == "std":
        # Use ±3 standard deviations (good for normal-like distributions)
        lower_bound, upper_bound = mean_val - 3 * std_dev, mean_val + 3 * std_dev
    else:
        # Use Interquartile Range (IQR) method (better for skewed data)
        q1, q3 = np.percentile(data, [25, 75])
        iqr = q3 - 1.5 * (q3 - q1)
        lower_bound, upper_bound = q1 - 1.5 * iqr, q3 + 1.5 * iqr

    # Ensure bounds are within actual min/max range
    return max(min_val, lower_bound), min(max_val, upper_bound)

# Function to plot histogram for an epoch
def plot_histogram(data, epoch):
    mean_value = np.mean(data)
    std_dev = np.std(data)

    plt.figure(figsize=(8, 6))
    
    # Automatically determine histogram bin range
    x_min, x_max = get_x_limits(data, method="iqr")
    bins = np.linspace(x_min, x_max, num=50)

    plt.hist(data, bins=bins, alpha=0.7, color="blue", edgecolor="black", density=True, label="Distribution")

    # Overlay mean and standard deviation
    plt.axvline(mean_value, color="red", linestyle="dashed", linewidth=2, label=f"Mean: {mean_value:.2f} ns")
    plt.axvline(mean_value - std_dev, color="green", linestyle="dashed", linewidth=2, label=f"1σ: {std_dev:.2f} ns")
    plt.axvline(mean_value + std_dev, color="green", linestyle="dashed", linewidth=2)

    plt.title(f"Epoch {epoch} - Execution Time Distribution")
    plt.xlabel("Execution Time (ns)")  # Keep units in nanoseconds
    plt.ylabel("Density")
    plt.legend()
    plt.grid()
    
    # Save figure in the "figures" directory
    save_path = os.path.join(FIGURE_DIR, f"epoch_{epoch}_histogram.png")
    plt.savefig(save_path)
    plt.close()  # Close plot to save memory

# Main function to process all epoch files
def process_experiment_data():
    if not os.path.exists(OUTPUT_DIR):
        print(f"Error: Directory '{OUTPUT_DIR}' not found.")
        return

    files = sorted([f for f in os.listdir(OUTPUT_DIR) if f.endswith(FILE_EXTENSION)])

    if not files:
        print(f"No binary output files found in '{OUTPUT_DIR}'")
        return

    for i, filename in enumerate(files):
        filepath = os.path.join(OUTPUT_DIR, filename)
        data = read_binary_file(filepath)
        print(f"Epoch {i}: Read {len(data)} samples from {filename}")

        # Plot histogram for each epoch
        plot_histogram(data, i)

# Run the analysis
if __name__ == "__main__":
    process_experiment_data()
