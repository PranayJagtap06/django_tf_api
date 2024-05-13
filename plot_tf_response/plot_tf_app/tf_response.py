from matplotlib import pyplot as plt
import numpy as np
import control as ct
import plotly.express as px
import plotly.graph_objects as go
from plotly.offline import plot
import plotly.io as pio
from PIL import Image
import io


def plot_response(d: float, vin: float, inductor: float, capacitor: float, resistor: float, mode: str):
    if mode == 'Buck':
        t, y, sys = buck_response(d, vin, inductor, capacitor, resistor)
        y_ss = y[-1]
    elif mode == 'Boost':
        t, y, sys = boost_response(d, vin, inductor, capacitor, resistor)
        y_ss = y[-1]
    elif mode == 'BuckBoost':
        t, y, sys = buckboost_response(d, vin, inductor, capacitor, resistor)
        y_ss = y[-1]
    else:
        print("Invalid mode. Please choose 'Buck', 'Boost', or 'BuckBoost'.")
        return None

    fig, ax = plt.subplots(dpi=200)
    ax.plot(t, y, label='Response')  # Plot steady-state response
    ax.plot(t, [y_ss] * len(t), label='Steady State Value')
    ax.set_xlabel('Time(sec)')
    ax.set_ylabel('Response')
    ax.set_title(f'Transient Response: Mode-{mode}, Vin-{vin}, D-{d}')
    ax.text(t[-1], y_ss, f'Steady State Value: {y_ss:.2f}', ha='right', va='bottom')
    ax.ticklabel_format(style='sci', axis='x', scilimits=(0, 0))
    ax.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
    ax.grid()
    ax.legend()
    plt.show()
    # buf = io.BytesIO()
    # plt.savefig(buf, format='png', dpi=300)
    # plt.close(fig)
    # return buf.getvalue()

    # y_ = [y_ss for i in t]
    # fig = px.line(x=t, y=[y, y_], title=f'Transient Response: Mode-{mode}, Vin-{vin}, D-{d}', width=745, height=445, labels={'x': 'Time(sec)', 'y': 'Response'},
    #               line_shape="spline",  # Add this line to get smooth lines
    #               render_mode="svg")
    # # fig.add_hline(y=y_ss, annotation_text=f"Steady State Value: {y_ss:.2f}", annotation_position="top right")
    # fig.data[0].name = 'Transient Response'
    # fig.data[1].name = "Steady State Value"
    # fig.update_xaxes(title_text='Time(sec)')
    # fig.update_yaxes(title_text='Response')
    # fig.update_layout(legend_title_text='Legend')
    # fig.add_annotation(text=f"Steady State Value: {y_ss:.2f}", xref="x", yref="y", x=max(t), y=y_ss+0.1, showarrow=False, font=dict(size=12), bgcolor="white")

    # pio.renderers.default = 'png'
    # pio.templates.default = 'seaborn'
    # img_bytes = fig.to_image(format="png", width=1920, height=1080)
    # img = Image.open(io.BytesIO(img_bytes))
    # img.show()
    # fig.show()

    """
    Renderers configuration
    -----------------------
    Default renderer: 'browser'
    Available renderers:
        ['plotly_mimetype', 'jupyterlab', 'nteract', 'vscode',
         'notebook', 'notebook_connected', 'kaggle', 'azure', 'colab',
         'cocalc', 'databricks', 'json', 'png', 'jpeg', 'jpg', 'svg',
         'pdf', 'browser', 'firefox', 'chrome', 'chromium', 'iframe',
         'iframe_connected', 'sphinx_gallery', 'sphinx_gallery_png']"""

def buck_response(d: float, vin: float, inductor: float, capacitor: float, resistor: float):
    """
    Buck Converter transfer function response.
    :param d: duty cycle.
    :param vin: input voltage of converter
    :param inductor: inductor value of converter
    :param capacitor: capacitor value of converter
    :param resistor: output resistor value
    :return: list of time vector and response of the system
    """
    # num_vd = np.array([vin/d])
    # den_vd = np.array([(np.sqrt(inductor*capacitor))**2, np.sqrt(inductor*capacitor)/(resistor*np.sqrt(capacitor/inductor)), 1])
    # num_vd = np.array([vin/(d*inductor*capacitor)])
    # den_vd = np.array([1, 1/(resistor*capacitor), 1/(inductor*capacitor)])

    num_vg = np.array([(d*vin)/(inductor*capacitor)])
    den_vg = np.array([1, 1/(resistor*capacitor), 1/(inductor*capacitor)])
    sys = ct.tf(num_vg, den_vg)
    # print('H(s) = ', sys)
    t, y = ct.step_response(sys)
    return [t, y, sys]


def boost_response(d: float, vin: float, inductor: float, capacitor: float, resistor: float):
    """
    Boost Converter transfer function response.
    :param d: duty cycle.
    :param vin: input voltage of converter
    :param inductor: inductor value of converter
    :param capacitor: capacitor value of converter
    :param resistor: output resistor value
    :return: list of time vector and response of the system
    """
    # num_vd = np.array([-(vin/(1-d))*(inductor/((1-d)**2)*resistor), vin/(1-d)])
    # den_vd = np.array([(np.sqrt(inductor*capacitor)/(1-d))**2, np.sqrt(inductor*capacitor)/((1-d)**2*resistor*np.sqrt(capacitor/inductor)), 1])
    # num_vd = np.array([-vin/((1-d)*resistor*capacitor), (vin*(1-d))/(inductor*capacitor)])
    # den_vd = np.array([1, 1/(resistor*capacitor), (1-d)**2/(inductor*capacitor)])

    num_vg = np.array([((1-d)*vin)/(inductor*capacitor)])
    den_vg = np.array([1, 1/(resistor*capacitor), ((1-d)**2)/(inductor*capacitor)])
    sys = ct.tf(num_vg, den_vg)
    # print('H(s) = ', sys)
    t, y = ct.step_response(sys)
    return [t, y, sys]


def buckboost_response(d: float, vin: float, inductor: float, capacitor: float, resistor: float):
    """
    Buck Boost Converter transfer function response.
    :param d: duty cycle.
    :param vin: input voltage of converter
    :param inductor: inductor value of converter
    :param capacitor: capacitor value of converter
    :param resistor: output resistor value
    :return: list of time vector and response of the system
    """
    # num_vd = np.array([-(vin/(d*(1-d)**2))*(inductor*d/((1-d)**2)*resistor), vin/(d*(1-d)**2)])
    # den_vd = np.array([(np.sqrt(inductor*capacitor)/(1-d))**2, np.sqrt(inductor*capacitor)/((1-d)**2*resistor*np.sqrt(capacitor/inductor)), 1])
    # num_vd = np.array([-1/((1-d)**2*resistor*capacitor), 1/(d*inductor*capacitor)])
    # den_vd = np.array([1, 1/(resistor*capacitor), (1-d)**2/(inductor*capacitor)])

    num_vg = np.array([-(((1-d)*d)*vin)/(inductor*capacitor)])
    den_vg = np.array([1, 1/(resistor*capacitor), ((1-d)**2)/(inductor*capacitor)])
    sys = ct.tf(num_vg, den_vg)
    # print('H(s) = ', sys)
    t, y = ct.step_response(sys)
    return [t, y, sys]


# if __name__ == "__main__":
#     d: float = float(input('Enter duty cycle: '))
#     vin: float = float(input('Enter input voltage: '))
#     ind: float = float(input('Enter inductor value: '))
#     cap: float = float(input('Enter capacitor value: '))
#     rs: float = float(input('Enter resistor value: '))
#     mode: str = str(input("Enter mode ('buck', 'boost' or 'buckboost'): "))
#     img = plot_response(d, vin, ind, cap, rs, mode)
#     with open('plot.png', 'wb') as f:
#         f.write(img)
