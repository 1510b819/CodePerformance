import cProfile
import pstats
import os
import sys
import matplotlib.pyplot as plt
import time

class CodePerformance:
    """
    CodePerformance class to profile the execution of a Python script.
    
    It measures the execution time of each function and visualizes the results.
    Additionally, it calculates some basic performance metrics to evaluate
    the script's efficiency.
    """
    
    @staticmethod
    def profile_script(script_path, time_threshold=1.0, call_threshold=100000):
        """
        Profiles the execution of a Python script and visualizes the performance.
        
        Args:
            script_path (str): Path to the Python script to profile.
            time_threshold (float): Maximum allowable execution time in seconds.
            call_threshold (int): Maximum allowable function calls to flag inefficient functions.
        
        Returns:
            None
        """
        
        # Check if the file exists
        if not os.path.exists(script_path):
            print(f"Error: The file '{script_path}' does not exist.")
            return

        print(f"Profiling script: {script_path}")

        # Start the profiler
        profiler = cProfile.Profile()
        profiler.enable()

        # Track script execution time
        start_time = time.time()

        # Execute the script
        exec(open(script_path).read())

        end_time = time.time()
        total_time = end_time - start_time
        
        # Stop profiling
        profiler.disable()

        print(f"\nTotal Execution Time: {total_time:.4f} seconds")

        # Performance check based on the time threshold
        if total_time > time_threshold:
            print(f"Warning: Execution time exceeds the threshold of {time_threshold} seconds.")
        else:
            print(f"Performance is within the acceptable time limit of {time_threshold} seconds.")
        
        # Analyzing the profile stats
        stats = pstats.Stats(profiler)
        stats.sort_stats('time')  # Sort by total time spent in each function

        stats.print_stats()  # Print detailed stats to the console

        # Extract the function names and execution times
        function_names = []
        times = []
        call_counts = []

        for func, (cc, nc, tt, ct, callers) in stats.stats.items():
            function_names.append(func[2])  # Function name
            times.append(tt)  # Total time spent in the function
            call_counts.append(cc)  # Number of calls to the function

        # Visualize the top 10 most time-consuming functions
        plt.figure(figsize=(10, 6))
        plt.barh(function_names[:10], times[:10])
        plt.xlabel('Total Time (seconds)')
        plt.title('Top 10 Most Time-Consuming Functions')
        plt.tight_layout()
        plt.show()

        # Performance metrics
        print("\nPerformance Metrics:")
        for i, func_name in enumerate(function_names[:10]):
            if call_counts[i] > call_threshold:
                print(f"  - Function '{func_name}' is called {call_counts[i]} times, which exceeds the threshold of {call_threshold} calls.")
            else:
                print(f"  - Function '{func_name}' is called {call_counts[i]} times.")
        
        if total_time > time_threshold:
            print("\nWarning: The script's execution time exceeds the recommended limit.")
        else:
            print("\nScript performed well within the time limit.")

# Example usage
if __name__ == "__main__":
    code = CodePerformance()
    script_to_profile = "example_script.py"  # Replace with the path to your script
    code.profile_script(script_to_profile)
