import matplotlib.figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
try:
    fig = matplotlib.figure.Figure()
    fig.set_layout_engine('constrained')
    axs = fig.subplots(2, 3)
    print("Success: set_layout_engine('constrained') worked")
except Exception as e:
    print(f"Error: {e}")
    try:
        fig = matplotlib.figure.Figure()
        # Fallback for even older versions or specific setups
        fig.set_constrained_layout(True)
        axs = fig.subplots(2, 3)
        print("Success: set_constrained_layout(True) worked")
    except Exception as e2:
        print(f"Error 2: {e2}")
        fig = matplotlib.figure.Figure()
        axs = fig.subplots(2, 3)
        print("Success: subplots without constrained layout worked")
