import pandas as pd
import matplotlib.pyplot as plt

# Carregar os dois arquivos CSV
data_in = pd.read_csv('../inside-tee-execution/pipe-in-experiment-result.csv')
data_out = pd.read_csv('../outside-tee-execution/pipe-out-experiment-result.csv')

# Determinar o intervalo de tempo máximo para os eixos Y em ambos os gráficos
max_time = max(data_in[['Write Time (ms)', 'Read Time (ms)']].max().max(),
               data_out[['Write Time (ms)', 'Read Time (ms)']].max().max())

# Criar uma figura com duas subplots lado a lado (um gráfico para cada arquivo)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

# Gráfico para pipe-in-experiment-result.csv
ax1.plot(data_in['Test'], data_in['Write Time (ms)'], label='Write Time (ms)', color='blue', marker='o')
ax1.plot(data_in['Test'], data_in['Read Time (ms)'], label='Read Time (ms)', color='green', marker='x')
ax1.set_title('Write and Read Time for Each Test (in Compartment)')
ax1.set_xlabel('Test')
ax1.set_ylabel('Time (ms)')
ax1.legend()
ax1.grid(True)
ax1.set_ylim(0, max_time)  # Definir o mesmo intervalo de tempo

# Gráfico para pipe-out-experiment-result.csv
ax2.plot(data_out['Test'], data_out['Write Time (ms)'], label='Write Time (ms)', color='blue', marker='o')
ax2.plot(data_out['Test'], data_out['Read Time (ms)'], label='Read Time (ms)', color='green', marker='x')
ax2.set_title('Write and Read Time for Each Test (out Compartment)')
ax2.set_xlabel('Test')
ax2.set_ylabel('Time (ms)')
ax2.legend()
ax2.grid(True)
ax2.set_ylim(0, max_time)  # Definir o mesmo intervalo de tempo

# Ajustar layout
plt.tight_layout()
plt.show()
