# ==============================================================================
#  The Geometry of the Echo: PMN-01 Model Source Code
#  ----------------------------------------------------------------------------
#  (c) 2025 Pablo Miguel Nieto Muñoz
#  License: MIT (See LICENSE file for details)
#  
#  Scientific Citation:
#  Nieto Muñoz, P. M. (2025). "The Geometry of the Echo: Observational 
#  Confirmation of the Chiral Dodecahedral Universe". 
#  Zenodo.
# ==============================================================================

library(ggplot2)
library(dplyr)
library(viridis)

# Configuration
INPUT_FILE <- "data/processed/fractal_metrics.csv"
OUTPUT_DIR <- "output/plots/"

# Ensure output directory exists
if (!dir.exists(OUTPUT_DIR)) {
  dir.create(OUTPUT_DIR, recursive = TRUE)
}

# 1. Load Data
if (!file.exists(INPUT_FILE)) {
  stop(paste("Input file not found:", INPUT_FILE))
}

df <- read.csv(INPUT_FILE)

# Data preprocessing
# Convert theta/phi to degrees or appropriate coordinates if needed
# Theta is usually 0 to Pi (colatitude), Phi is 0 to 2Pi.
# Latitude = 90 - Theta_deg
# Longitude = Phi_deg - 180 (usually)

df <- df %>%
  mutate(
    theta_deg = theta * 180 / pi,
    phi_deg = phi * 180 / pi,
    lat = 90 - theta_deg,
    lon = phi_deg - 180,
    is_anomalous = hurst_I > 0.6
  )

# Viz A: The Fingerprint (Scatter plot of Radius vs Hurst)
# Destaca en ROJO los puntos que superen el umbral de ruido aleatorio (Hurst > 0.6).
p1 <- ggplot(df, aes(x = radio, y = hurst_I)) +
  geom_jitter(aes(color = is_anomalous), alpha = 0.6, width = 0.2, height = 0) +
  geom_hline(yintercept = 0.6, linetype = "dashed", color = "red") +
  scale_color_manual(values = c("FALSE" = "grey50", "TRUE" = "red")) +
  theme_minimal(base_size = 14) +
  labs(
    title = "The Fingerprint: Scale Invariance Breakdown",
    subtitle = "Hurst Exponent vs Angular Radius",
    x = "Ring Radius (degrees)",
    y = "Hurst Exponent (Persistence)",
    color = "Anomalous (>0.6)"
  ) +
  theme(legend.position = "top")

ggsave(file.path(OUTPUT_DIR, "viz_A_fingerprint.png"), plot = p1, width = 10, height = 6, dpi = 300)

# Viz B: Phase Transformation (Density 2D Hurst vs Correlation I-P)
# Muestra si los anillos anómalos forman un clúster separado del ruido de fondo.
p2 <- ggplot(df, aes(x = corr_IP, y = hurst_I)) +
  stat_density_2d(aes(fill = ..level..), geom = "polygon", contour = TRUE) +
  geom_point(alpha = 0.2, size = 0.5) +
  scale_fill_viridis(option = "magma") +
  geom_hline(yintercept = 0.6, linetype = "dashed", color = "white") +
  theme_dark(base_size = 14) +
  labs(
    title = "Phase Transformation Signature",
    subtitle = "Fractal Structure vs Polarization Correlation",
    x = "Intensity-Polarization Correlation",
    y = "Hurst Exponent",
    fill = "Density"
  )

ggsave(file.path(OUTPUT_DIR, "viz_B_phase_transformation.png"), plot = p2, width = 8, height = 8, dpi = 300)

# Viz C: The Evidence (Heatmap polar/proyección del cielo)
# Marcando dónde están los anillos anómalos.
# We focus on the anomalous rings.
anomalous_rings <- df %>% filter(is_anomalous)

p3 <- ggplot(df, aes(x = lon, y = lat)) +
  geom_bin2d(bins = 60, aes(fill = ..count..)) +
  scale_fill_viridis(option = "inferno", name = "Ring Count") +
  geom_point(data = anomalous_rings, aes(x = lon, y = lat), color = "cyan", size = 2, shape = 1, stroke = 1) +
  coord_fixed(ratio = 1) +
  theme_minimal(base_size = 14) +
  labs(
    title = "The Evidence: Sky Distribution of Anomalies",
    subtitle = "Background: Search Density | Cyan Circles: Hurst > 0.6",
    x = "Longitude (degrees)",
    y = "Latitude (degrees)"
  ) +
  theme(
    panel.grid.major = element_line(color = "grey80", linetype = "dotted"),
    panel.background = element_rect(fill = "black", color = NA),
    plot.background = element_rect(fill = "white", color = NA)
  )

# If coord_map is available, use it for projection
if (requireNamespace("mapproj", quietly = TRUE)) {
  p3 <- p3 + coord_map("mollweide")
}

ggsave(file.path(OUTPUT_DIR, "viz_C_evidence.png"), plot = p3, width = 12, height = 7, dpi = 300)

print(paste("Plots saved to", OUTPUT_DIR))
