from matplotlib import pyplot as plt
import numpy as np
import control as ct
import io


def plot_response(d: float, vin: float, inductor: float, capacitor: float, resistor: float, mode: str) -> tuple:
    global y_ss, sys, t, y
    response_functions = {
        'Buck': buck_response,
        'Boost': boost_response,
        'BuckBoost': buckboost_response
    }

    # if mode == 'Buck':
    #     t, y, sys = buck_response(d, vin, inductor, capacitor, resistor)
    #     y_ss = y[-1]
    # elif mode == 'Boost':
    #     t, y, sys = boost_response(d, vin, inductor, capacitor, resistor)
    #     y_ss = y[-1]
    # elif mode == 'BuckBoost':
    #     t, y, sys = buckboost_response(d, vin, inductor, capacitor, resistor)
    #     y_ss = y[-1]
    # else:
    #     return tuple()

    if mode in response_functions:
        t, y, sys = response_functions[mode](d, vin, inductor, capacitor, resistor)
        y_ss = y[-1]

    fig, ax = plt.subplots(dpi=200)
    ax.plot(t, y, label='Transient Response')  # Plot steady-state response
    ax.plot(t, [y_ss] * len(t), label='Steady State Value')
    ax.set_xlabel('Time(sec)')
    ax.set_ylabel('Response')
    ax.set_title(f'Transient Response: Mode-{mode}, Vin-{vin}, D-{d}')
    ax.text(t[-1], y_ss, f'Steady State Value: {y_ss:.2f}', ha='right', va='bottom')
    ax.ticklabel_format(style='sci', axis='x', scilimits=(0, 0))
    ax.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
    ax.grid()
    ax.legend()
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=300)
    plt.close(fig)
    return buf.getvalue(), str(sys)


def buck_response(d: float, vin: float, inductor: float, capacitor: float, resistor: float) -> list:
    """
    Buck Converter transfer function response.
    :param d: duty cycle.
    :param vin: input voltage of converter
    :param inductor: inductor value of converter
    :param capacitor: capacitor value of converter
    :param resistor: output resistor value
    :return: list of time vector and response of the system
    """

    num_vg = np.array([(d*vin)/(inductor*capacitor)])
    den_vg = np.array([1, 1/(resistor*capacitor), 1/(inductor*capacitor)])
    sys_ = ct.tf(num_vg, den_vg)
    # print('H(s) = ', sys)
    t_, y_ = ct.step_response(sys_)
    return [t_, y_, sys_]


def boost_response(d: float, vin: float, inductor: float, capacitor: float, resistor: float) -> list:
    """
    Boost Converter transfer function response.
    :param d: duty cycle.
    :param vin: input voltage of converter
    :param inductor: inductor value of converter
    :param capacitor: capacitor value of converter
    :param resistor: output resistor value
    :return: list of time vector and response of the system
    """

    num_vg = np.array([((1-d)*vin)/(inductor*capacitor)])
    den_vg = np.array([1, 1/(resistor*capacitor), ((1-d)**2)/(inductor*capacitor)])
    sys_ = ct.tf(num_vg, den_vg)
    # print('H(s) = ', sys)
    t_, y_ = ct.step_response(sys_)
    return [t_, y_, sys_]


def buckboost_response(d: float, vin: float, inductor: float, capacitor: float, resistor: float) -> list:
    """
    Buck Boost Converter transfer function response.
    :param d: duty cycle.
    :param vin: input voltage of converter
    :param inductor: inductor value of converter
    :param capacitor: capacitor value of converter
    :param resistor: output resistor value
    :return: list of time vector and response of the system
    """

    num_vg = np.array([-(((1-d)*d)*vin)/(inductor*capacitor)])
    den_vg = np.array([1, 1/(resistor*capacitor), ((1-d)**2)/(inductor*capacitor)])
    sys_ = ct.tf(num_vg, den_vg)
    # print('H(s) = ', sys)
    t_, y_ = ct.step_response(sys_)
    return [t_, y_, sys_]
