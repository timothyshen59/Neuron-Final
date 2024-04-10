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
    for key, value in the_dictionary.items():
        if(value > 120):
            x_region.append(key)
            y_val.append(value)
            final_dictionary[key] = value


    plt.figure(figsize=(10,10))
    plt.bar(x_region, y_val, tick_label = x_region, width=0.4, color=['blue'])
    plt.ylim(0, 60000)
    plt.xlabel('Standard Deviation')
    plt.ylabel('Number of data points at this Standard Deviation')
    plt.title('Standard Deviation vs Count for all ION CHANNEL '+lister[i])
    plt.savefig("STD_DEV_VS_COUNT_"+lister[i]+".png")
    y_value = []

