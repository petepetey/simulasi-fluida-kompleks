
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import plotly.graph_objects as go

st.set_page_config(layout="wide")
st.title("🌪️ Visualisasi Interaktif Fluida Kompleks di Sekitar Silinder")

st.sidebar.header("🔧 Parameter Aliran Fluida")
U = st.sidebar.slider("Kecepatan Aliran (U)", min_value=0.5, max_value=5.0, value=1.0, step=0.1)
a = st.sidebar.slider("Radius Silinder (a)", min_value=0.1, max_value=2.0, value=1.0, step=0.1)
Gamma = st.sidebar.slider("Sirkulasi (Γ)", min_value=-10.0, max_value=10.0, value=1.0, step=0.5)

# Domain lebih jarang untuk cone lebih jelas
x = np.linspace(-3, 3, 18)
y = np.linspace(-3, 3, 18)
X, Y = np.meshgrid(x, y)
Z = X + 1j * Y

# Fungsi kompleks aliran dan kecepatan
with np.errstate(divide='ignore', invalid='ignore'):
    f = U * (Z + (a**2)/Z) + (1j * Gamma / (2 * np.pi)) * np.log(Z)
    phi = np.real(f)
    psi = np.imag(f)
    dfdz = U * (1 - (a**2 / Z**2)) + 1j * Gamma / (2 * np.pi * Z)
    V = dfdz

speed = np.abs(V)
Vx = np.real(V)
Vy = -np.imag(V)

# Plot 3D
fig3d = go.Figure()

fig3d.add_trace(go.Surface(
    z=psi,
    x=X,
    y=Y,
    surfacecolor=speed,
    colorscale='Turbo',
    colorbar=dict(title="|v| (Kecepatan)"),
    showscale=True,
    opacity=0.96
))

fig3d.add_trace(go.Scatter3d(
    x=[0], y=[0], z=[0],
    mode='markers+text',
    marker=dict(size=12, color='red', symbol='circle'),
    text=["Pusat Silinder"],
    textposition="top center",
    name="Silinder"
))

# Tambahkan panah cone yang lebih besar dan kontras
fig3d.add_trace(go.Cone(
    x=X.flatten(),
    y=Y.flatten(),
    z=np.zeros_like(X.flatten()),
    u=Vx.flatten(),
    v=Vy.flatten(),
    w=np.zeros_like(X.flatten()),
    sizemode="absolute",
    sizeref=0.6,
    anchor="tail",
    colorscale="Bluered",
    showscale=False,
    name="Arah Vektor"
))

fig3d.update_layout(
    title="🌐 Permukaan ψ + Arah Vektor Lebih Jelas",
    scene=dict(
        xaxis_title='x', yaxis_title='y', zaxis_title='ψ',
        aspectratio=dict(x=1, y=1, z=0.5),
        camera=dict(eye=dict(x=2, y=2, z=1.5)),
        xaxis=dict(backgroundcolor="white"),
        yaxis=dict(backgroundcolor="white"),
        zaxis=dict(backgroundcolor="white"),
    ),
    margin=dict(l=0, r=0, t=40, b=0)
)

st.plotly_chart(fig3d, use_container_width=True)

st.markdown("### 📘 Penjelasan Visualisasi 3D")
st.markdown("""
- **ψ (psi)** menunjukkan permukaan fungsi aliran.
- **Panah cone** sekarang lebih besar, jarang, dan jelas untuk menunjukkan arah kecepatan.
- **Warna Turbo dan Bluered** membedakan kecepatan dan arah visual secara kontras.
""")

# Grafik 2D
fig2d, ax = plt.subplots(figsize=(8, 6))
heatmap = ax.contourf(X, Y, speed, cmap='plasma', levels=100)
cbar = plt.colorbar(heatmap, ax=ax)
cbar.set_label('|v| (Kecepatan)', rotation=270, labelpad=15)
ax.contour(X, Y, psi, colors='white', linewidths=0.8, alpha=0.8)
circle = plt.Circle((0, 0), a, color='black', fill=False, linewidth=2)
ax.add_artist(circle)
ax.set_aspect('equal')
ax.set_title("🌊 Kontur ψ & Peta Kecepatan |v|", fontsize=13)
ax.set_xlabel("x")
ax.set_ylabel("y")
st.pyplot(fig2d)


# Tambahan identitas pembuat
st.markdown("---")
st.markdown(
    "<div style='text-align: center; font-size: 18px; color: #333;'>"
    "<strong>Dibuat oleh:</strong><br>"
    "<span style='font-size:22px; color:#3366cc;'><strong>Peter Immanuel Sitompul</strong></span><br>"
    "NIM: <code style='color: #d63384;'>21060124130049</code>"
    "</div>",
    unsafe_allow_html=True
)
