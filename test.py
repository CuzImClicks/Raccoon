
import time
for i in range(100, 0, -1):
    print(f"\r{i:3d} remaining", end="")
    time.sleep(1)

