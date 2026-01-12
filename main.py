import numpy as np
import numpy_financial as npf
import matplotlib.pyplot as plt

# --- PARAMETRY ZADANIA ---
PV_M = 120000  # Cena mieszkania obecnie [zł]
g = 0.05       # Roczny wzrost cen mieszkań [5%]
T = 5          # Okres [lata]
r_nom = 0.12   # Nominalna roczna stopa lokaty [12%]
m = 12         # Kapitalizacja/wpłaty miesięczne
N = T * m      # Całkowita liczba okresów (60 miesięcy)
i = r_nom / m  # Efektywna stopa miesięczna (1%)

# --- 1. Orientacyjna cena mieszkania za 5 lat (FV_M) ---
FV_M = PV_M * (1 + g)**T

print("### Orientacyjna cena mieszkania za 5 lat ###")
print(f"Cena mieszkania (FV_M): {FV_M:.2f} zł")
print("-" * 50)

# --- 2. Wymagana stała miesięczna wpłata (PMT) ---
PMT = npf.pmt(rate=i, nper=N, pv=0, fv=-FV_M)

print("### Wymagana stała miesięczna wpłata ###")
print(f"Wpłata miesięczna (PMT): {PMT:.2f} zł")
print("-" * 50)

# --- 3. PRZYGOTOWANIE DANYCH DO WYKRESU ---
okresy = np.arange(N + 1)

# a) Wartość lokaty (kapitalizacja złożona) - WEKTORYZACJA
wartosc_lokaty = npf.fv(rate=i, nper=okresy, pmt=-PMT, pv=0)

# b) Cena mieszkania (liniowy wzrost)
przyrost_ceny = FV_M - PV_M
miesieczny_przyrost = przyrost_ceny / N
wartosc_mieszkania = PV_M + okresy * miesieczny_przyrost

# --- 4. WIZUALIZACJA ---
plt.figure(figsize=(12, 6))

plt.plot(okresy, wartosc_lokaty, label='Wartość lokaty', color='blue', linewidth=2)
plt.plot(okresy, wartosc_mieszkania, label='Cena mieszkania (Liniowy wzrost)', 
         color='red', linestyle='--', linewidth=2)

plt.plot(N, FV_M, 'go', markersize=10, label=f'Cel: {FV_M:.0f} zł (po {N} m-cach)')

plt.title(f'Wartość lokaty vs. Cena mieszkania w ciągu {T} lat', fontsize=14, fontweight='bold')
plt.xlabel('Miesiąc', fontsize=12)
plt.ylabel('Wartość [zł]', fontsize=12)
plt.grid(True, linestyle=':', alpha=0.7)
plt.legend(fontsize=10, loc='upper left')
plt.ticklabel_format(style='plain', axis='y')
plt.xlim(0, N)
plt.ylim(bottom=0)
plt.tight_layout()

plt.show()

# --- 5. DODATKOWE STATYSTYKI ---
print("\n### Podsumowanie ###")
print(f"Całkowita suma wpłat: {PMT * N:.2f} zł")
print(f"Całkowity zysk z odsetek: {FV_M - (PMT * N):.2f} zł")
print(f"Procent zysku: {((FV_M - (PMT * N)) / (PMT * N) * 100):.2f}%")
