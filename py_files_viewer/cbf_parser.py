## There already exist packages for parsing these types of files
## But.. we can easily modify/update them if necessary!

import cbf
import os
from matplotlib import pyplot as plt

directory_in_str = str(input('Input directory file path: '))

#directory = os.fsencode(directory_in_str)

directory = directory_in_str 
   
for file in os.listdir(directory):
     filename = os.fsdecode(file)
     if filename.endswith(".cbf"): 
         print('--> Reading in file: ',os.path.join(directory, filename))
         cbf_file = os.path.join(directory, filename) 
         content = cbf.read(str(cbf_file))
         numpy_array_with_data = content.data
         header_metadata = content.metadata

# Plot image with matplot lib
         plt.imshow(numpy_array_with_data, cmap='gray', vmax=1)
         plt.show()
         continue
     else:
         continue


