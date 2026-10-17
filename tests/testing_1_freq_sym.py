import secrets, string, collections
import matplotlib.pyplot as plt

chars = string.ascii_letters + string.digits + string.punctuation
pool = list(set(chars))
N, L = 50000, 16

cnt = collections.Counter()
for _ in range(N):
    cnt.update("".join(secrets.choice(pool) for _ in range(L)))

exp = N * L / len(pool)
symbols = sorted(pool)

plt.figure(figsize=(12, 4))
plt.bar(range(len(symbols)), [cnt[c] for c in symbols])
plt.axhline(exp, color="red", linestyle="--", label=f"Очаквана честота ({exp:.0f})")
plt.xticks(range(len(symbols)), symbols, fontsize=7)
plt.ylim(0, exp * 1.2)
plt.xlabel("Символ")
plt.ylabel("Брой появявания")
plt.legend()
plt.tight_layout()
plt.savefig("frequency.png", dpi=200)