"""Copy entry.png into /output and report its size."""
import os
import shutil

dest = "/output/entry.png"
os.makedirs("/output", exist_ok=True)
shutil.copyfile("./entry.png", dest)
print("copied to " + dest)
print(os.path.getsize(dest))
