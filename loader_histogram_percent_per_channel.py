import ast
import matplotlib.pyplot as plt

NUM_ION_CHANNELS = 19

lister = ["gNaTs2_tbar_NaTs2_t_apical", "gSKv3_1bar_SKv3_1_apical","gImbar_Im_apical","gIhbar_Ih_dend", "gNaTa_tbar_NaTa_t_axonal", "gK_Tstbar_K_Tst_axonal", "gNap_Et2bar_Nap_Et2_axonal", "gSK_E2bar_SK_E2_axonal", "gCa_HVAbar_Ca_HVA_axonal", "gK_Pstbar_K_Pst_axonal","gCa_LVAstbar_Ca_LVAst_axonal", "g_pas_axonal", "cm_axonal", "gSKv3_1bar_SKv3_1_somatic","gNaTs2_tbar_NaTs2_t_somatic", "gCa_LVAstbar_Ca_LVAst_somatic", "g_pas_somatic", "cm_somatic", "e_pas_all"]
for i in range(NUM_ION_CHANNELS):
    with open('histogram_data'+str(i)+'.txt') as f:
        data = f.read()

    the_dictionary = ast.literal_eval(data)
    final_dictionary = {}
    x_region = []
    y_val = []

    counter = 0
    the_total = 0
    for key, value in the_dictionary.items():
        if(counter == 0):
            the_total += value
            counter += 1
            continue

        x_region.append(key+"percent left")
        y_val.append(the_total)
        the_total += value

    
    print("----------i------", i)
    for iq in range(len(y_val)):
        print(y_val[iq])
        y_val[iq] = (float(y_val[iq])/float(the_total))*float(100)
        print(the_total)
    print("----------i------", i)

    plt.figure(figsize=(20,25))
    plt.bar(x_region, y_val, tick_label = x_region, width=0.5, color=['blue'])
    plt.ylim(0, 100)
    plt.xlabel('std dev threshold')
    plt.ylabel('percent to the left of each std dev threshold')
    plt.title('Standard Deviation vs % of points to left of threshold '+lister[i])
    plt.savefig("STD_DEV_VS_Threshold_Percent"+lister[i]+".png")
    y_value = []

