import numpy as np
import numpy_financial as npf
import matplotlib.pyplot as plt

# --- 1. Dane wejściowe ---

PV_M = 120000  # Cena mieszkania w tym momencie [zł]
g = 0.05       # Roczny wzrost cen mieszkań [5%]
T = 5          # Okres [lata]
r_nom = 0.12   # Nominalna roczna stopa lokaty [12%]
m = 12         # Kapitalizacja/wpłaty miesięczne
N = T * m      # Całkowita liczba okresów (60 miesięcy)
i = r_nom / m  # Efektywna stopa miesięczna (1%)

# --- 2. Obliczenie orientacyjnej ceny mieszkania za 5 lat (FV_M) ---

FV_M = PV_M * (1 + g)**T

print(f"Orientacyjna cena mieszkania za {T} lat: {FV_M:.2f} zł")
print("-" * 40)

# --- 3. Obliczenie wymaganej stałej miesięcznej wpłaty (PMT) ---

# Używamy npf.pmt. FV jest ujemne, ponieważ reprezentuje przyszły cel (wpływ na konto),
# który musi być równoważony przez bieżące płatności (odpływy).
PMT = npf.pmt(rate=i, nper=N, pv=0, fv=-FV_M, type=0)

print(f"Wymagana stała miesięczna wpłata (PMT): {PMT:.2f} zł")
print("-" * 40)

# --- 4. Tworzenie danych do wykresu ---

okresy = np.arange(N + 1)
wartosc_lokaty = np.zeros(N + 1)

# Obliczenie wartości lokaty w każdym miesiącu (za pomocą npf.fv)
for t in okresy[1:]:
    wartosc_lokaty[t] = npf.fv(rate=i, nper=t, pmt=-PMT, pv=0, type=0)

# Obliczenie liniowego wzrostu ceny mieszkania
przyrost_ceny = FV_M - PV_M
miesieczny_przyrost = przyrost_ceny / N
wartosc_mieszkania = PV_M + okresy * miesieczny_przyrost

# --- 5. Wizualizacja (Wykres) ---

plt.figure(figsize=(12, 6))

plt.plot(okresy, wartosc_lokaty, label='Wartość lokaty (Kapitalizacja złożona)', color='blue', linewidth=2)
plt.plot(okresy, wartosc_mieszkania, label='Cena mieszkania (Liniowy wzrost)', color='red', linestyle='--')

plt.plot(N, FV_M, 'go', markersize=8, label=f'Cel: {FV_M:.0f} zł (po {N} m-cach)')

plt.title(f'Wartość lokaty vs. Cena mieszkania w ciągu {T} lat', fontsize=14)
plt.xlabel('Miesiąc', fontsize=12)
plt.ylabel('Wartość [zł]', fontsize=12)
plt.grid(True, linestyle=':', alpha=0.7)
plt.legend(fontsize=10)
plt.ticklabel_format(style='plain', axis='y')
plt.xlim(0, N)
plt.ylim(bottom=0)
plt.tight_layout()

plt.show()
