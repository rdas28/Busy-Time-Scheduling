import sys

def read_input(file_name):
    with open(file_name, "r") as f:
        n = int(f.readline().strip())
        jobs = []
        for _ in range(n):
            r, d, p = map(int, f.readline().strip().split())
            jobs.append((r, d, p))
    return n, jobs

def write_output(file_name, schedule):
    with open(file_name, "w") as f:
        for s in schedule:
            f.write(f"{s}\n")

def busy_time_scheduling(n, jobs):
    # Generate sorted set of interesting times T
    T = sorted(set(t for r, d, _ in jobs for t in range(r, d + 1)))
    T_len = len(T)
    time_index = {t: i for i, t in enumerate(T)}

    # Initialize DP table: dp[t1][t2] = minimum cost for [T[t1], T[t2])
    dp = [[float('inf')] * T_len for _ in range(T_len)]
    dp_start = [[-1] * T_len for _ in range(T_len)]  # To store starting times

    # Base case: No cost for zero-length intervals
    for t in range(T_len):
        dp[t][t] = 0

    # Dynamic programming to calculate minimum costs
    for length in range(1, T_len + 1):  # Interval lengths
        for t1 in range(T_len - length + 1):
            t2 = t1 + length - 1
            for j, (r, d, p) in enumerate(jobs):
                if T[t1] >= r and T[t2] <= d:
                    for t in range(max(r, T[t1]), min(d - p + 1, T[t2] - p + 1)):
                        # Calculate cost for scheduling job `j` in interval
                        t_index = time_index[t]
                        t_end_index = time_index[t + p]
                        cost = min(
                            p,
                            T[t] - T[t1],
                            T[t2] - (T[t] + p),
                            T[t2] - T[t1]
                        )
                        # Update DP table
                        new_cost = cost + dp[t1][t_index] + dp[t_end_index][t2]
                        if new_cost < dp[t1][t2]:
                            dp[t1][t2] = new_cost
                            dp_start[t1][t2] = t

    # Backtrack to construct the schedule
    schedule = [-1] * n
    for j, (r, d, p) in enumerate(jobs):
        for t in range(T_len):
            if T[t] >= r and T[t] + p <= d:
                schedule[j] = T[t]
                break

    return schedule

if __name__ == "__main__":
    input_file = sys.argv[1]  # Input file name (e.g., "instance01.txt")
    output_file = sys.argv[2]  # Output file name (e.g., "solution01.txt")

    n, jobs = read_input(input_file)
    schedule = busy_time_scheduling(n, jobs)
    write_output(output_file, schedule)
