import math
import matplotlib.pyplot as plt

alphabets = {"a-z (26)": 26, "a-z, A-Z (52)": 52,
             "a-z, A-Z, 0-9 (62)": 62, "всички класове (94)": 94}
lengths = range(1, 33)

plt.figure(figsize=(8, 5))
for name, n in alphabets.items():
    plt.plot(lengths, [l * math.log2(n) for l in lengths], label=name)
for t in (45, 80, 90):
    plt.axhline(t, color="gray", linestyle=":")
plt.axvline(15, color="red", linestyle="--", label="15 символа (NIST)")
plt.xlabel("Дължина на паролата")
plt.ylabel("Ентропия, бита")
plt.legend()
plt.tight_layout()
plt.savefig("entropy.png", dpi=200)