import ast
import matplotlib.pyplot as plt

with open('histogram_data.txt') as f:
    data = f.read()

the_dictionary = ast.literal_eval(data)
final_dictionary = {}
print(the_dictionary)
x_region = []
y_val = []


for key, value in the_dictionary.items():
    if(value > 5):
        x_region.append(key)
        y_val.append(value)
        final_dictionary[key] = value


plt.figure(figsize=(20,40))
plt.yscale("log")
plt.bar(x_region, y_val, tick_label = x_region, width=0.4, color=['blue'])
plt.xlabel('Standard Deviation')
plt.ylabel('Number of data points at this Standard Deviation')
plt.title('Standard Deviation vs Count for all ION CHANNELS COMBINED ')
plt.savefig("STD_DEV_VS_COUNT.png")
y_value = []


plt.savefig("STD_DEV_VS_COUNT.png")
    

