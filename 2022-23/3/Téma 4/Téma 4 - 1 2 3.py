import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

def main():
    plt.style.use("seaborn-poster")

    # ======== Úloha 1 ==========
    plt.figure(1)
    plt.xlabel("t")
    plt.ylabel("$x' = r \\cdot x \\left(1 - \\frac{x}{K}\\right)$")

    t_eval = np.arange(0, 8, 0.01)
    for K in [3, 7, 10]:
        for r in [2, 3, 10]:
            F = lambda t, s: r * s * (1 - s/K)
            sol = solve_ivp(F, [0, 8], [0.01], t_eval=t_eval)
            plt.plot(sol.t, sol.y[0], label="$K = {K}, r = {r}$".format(K=K, r=r))

    plt.legend(loc="upper right")


    # ======== Úloha 2 ==========
    plt.figure(2)
    plt.xlabel("x")
    plt.ylabel("y")

    # Původní řešení pomocí goniometrických funkcí
    # F = lambda t, s: np.array([
    #     v_v * np.sin(np.arctan((v_z*t-s[0])/s[1])),
    #     - v_v * np.cos(np.arctan((v_z*t-s[0])/s[1]))
    # ])

    F = lambda t, s: np.array([
        v_v * (v_z * t - s[0]) / np.sqrt(np.power(v_z*t - s[0], 2) + np.power(s[1], 2)),
        - v_v * s[1] / np.sqrt(np.power(v_z*t - s[0], 2) + np.power(s[1], 2))
    ])

    stop_event = lambda t, y: y[1]
    stop_event.terminal = True

    t_eval = np.arange(0, 3, 0.001)

    x_min = 10e20

    for v_v in [0.8, 1, 1.5]:
        v_z = 1
        sol = solve_ivp(F, [0, 3], [0, 1], t_eval=t_eval, events=stop_event)
        plt.plot(sol.y.T[:, 0], sol.y.T[:, 1], label='$v_z = {v_z}, v_v = {v_v}$'.format(v_z=v_z, v_v=v_v))
        x_min = min(x_min, sol.y.T[:,0][-1])

    plt.axhline(0, color="gray", alpha=0.3)
    plt.axvline(0, color="gray", alpha=0.3)
    plt.xlim(-0.1, x_min + 0.1)
    plt.legend(loc="best")


    # ======== Úloha 3 ==========
    plt.figure(3, figsize=(8,8))
    plt.xlabel("x")
    plt.ylabel("y")

    v = 1
    F = lambda t, s: np.array([
        (s[2]-s[0])/np.sqrt(np.power(s[2]-s[0], 2) + np.power(s[3] - s[1], 2)),
        (s[3]-s[1])/np.sqrt(np.power(s[2]-s[0], 2) + np.power(s[3] - s[1], 2)),
        (s[4]-s[2])/np.sqrt(np.power(s[4]-s[2], 2) + np.power(s[5] - s[3], 2)),
        (s[5]-s[3])/np.sqrt(np.power(s[4]-s[2], 2) + np.power(s[5] - s[3], 2)),
        (s[6]-s[4])/np.sqrt(np.power(s[6]-s[4], 2) + np.power(s[7] - s[5], 2)),
        (s[7]-s[5])/np.sqrt(np.power(s[6]-s[4], 2) + np.power(s[7] - s[5], 2)),
        (s[0]-s[6])/np.sqrt(np.power(s[0]-s[6], 2) + np.power(s[1] - s[7], 2)),
        (s[1]-s[7])/np.sqrt(np.power(s[0]-s[6], 2) + np.power(s[1] - s[7], 2)),
    ]) * v

    t_eval = np.arange(0, 1, 0.001)
    sol = solve_ivp(
        F,
        [0, 1],
        [
            0, 0,
            1, 0,
            1, 1,
            0, 1,
        ],
        t_eval=t_eval
    )
    for i in range(0,4):
        plt.plot(sol.y.T[:, i*2], sol.y.T[:,i*2+1], label="{x}. raketa".format(x=i+1))
    plt.legend(title="$v={v}$".format(v=v), loc="best", title_fontsize="xx-large")
    plt.show()


if __name__ == "__main__":
    main()
